import os, secrets, pprint, json, urllib
from jinja2 import StrictUndefined

from flask import (Flask, render_template, request, flash, redirect, 
                    session, url_for, abort, jsonify)
from sqlalchemy import desc
from flask_debugtoolbar import DebugToolbarExtension

from model import (connect_to_db, db, User, Community, CommunityMembers, 
                    Post, PostRatings, Comment, CommentRatings)
from forms import (RegistrationForm, LoginForm, CommunityForm, 
                    AccountForm, PostForm, CommentForm, GiphyForm, SendTextForm)
from flask_bcrypt import Bcrypt
from flask_login import (LoginManager, login_user, logout_user, 
                        login_required, current_user)

# API SET UP
# User config file (API Keys and Tokens)
with open('config/config.json', 'r') as f:
    config = json.load(f)

# Twilio API
from twilio.rest import Client
TWILIO_ACCOUNT_SID = config['twilio']['account_sid']
TWILIO_AUTH_TOKEN = config['twilio']['auth_token']
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Cloudinary API
import cloudinary, cloudinary.uploader, cloudinary.api
cloudinary.config(
  cloud_name = config['cloudinary']['name'],
  api_key = config['cloudinary']['api_key'],  
  api_secret = config['cloudinary']['api_secret']  
)
cloudinary_prefix = 'https://res.cloudinary.com/' + config["cloudinary"]["name"] + '/image/upload/v' 

# Giphy API
GIPHY_API_KEY = config['giphy']['api_key']

# SERVER SETUP
app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
app.secret_key = config["secret_key"]["keddit"]
app.jinja_env.undefined = StrictUndefined

# Flask login - User Login Management
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# ************************
#                        *
#          App           *
#                        *
# ************************

@app.route('/')
def home():
    """ Landing Page.
    
    Application overview, user registration, user login.
    """
    form =  LoginForm()
    signup = RegistrationForm()
    return render_template("landing_page.html", form = form, signup=signup)


@app.route('/registration', methods=['GET', 'POST'])
def register_form():
    """Registration form route where users may sign-up for an account.
    
    Users submit a unqiue custom username and password.
    """

    # Set form to our RegistrationForm() class from forms.py
    form = RegistrationForm()
    # When form submitted, add user to our database from our model.py classes
    if form.validate_on_submit():
        # Convert username to lower and remove spaces
        username = (form.username.data).lower()
        username = username.replace(" ", "")
        # Hash password
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Add our user to our database
        user = User(username=username, email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! Please log in.', 'success')
        return redirect('/login')
    return render_template("registration.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""

    # LoginForm from forms.py
    form = LoginForm()

    # When user submits login. Query for email data, validate, and check password.
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Validation Check before logging in
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash("You are now logged in!", 'success')
            # Redirect to Front Page after logging in
            return redirect("/home") 
        else:
            flash('Login Unsucessful. Please check email and password.',
                                                                    'danger')
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    """Log out route."""

    image_file = url_for('static', filename='images/' + current_user.image_file)
    logout_user()
    flash("Logged Out. Hope to see you again!", 'success')
    return redirect("/")


def save_picture(form_picture):
    '''
    Function that saves a user's profile picture.
    '''
    # Hash filename to not error with other similar file names
    random_hex = secrets.token_hex(8)
    # Get extenstion of picture being uploaded
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    
    form_picture.save(picture_path)
    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    '''
    User's account page route
    '''
    form = AccountForm()

    if form.validate_on_submit():
        # Update user picture
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        # Update user info
        current_user.username= form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        # Prepopulate field with user info
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='images/' + current_user.image_file)
    return render_template('account.html', image_file=image_file, 
                                                            form=form)


@app.route('/home')
def frontpage():
    '''
    Main page route (Home, Frontpage). Displays top popular comments from
    all communities (Subkeddits) with votes.
    '''
    # Posts from all communities in db
    posts = Post.query.order_by(desc(Post.votecount)).all()

    votes = []
    comments = []
    communities= []

    # For each post in Posts(Post query above), get the upvotes and downvotes... 
    # ...for each post_id
    # Then append them to a list after subtracting.
    for post in posts:
        upvote = PostRatings.query.filter(PostRatings.post_id==post.id, PostRatings.upvote>=1).count()
        downvote = PostRatings.query.filter(PostRatings.post_id==post.id, PostRatings.downvote>=1).count()
        votes.append(upvote - downvote)
        comments_count = Comment.query.filter_by(post_id=post.id).count()
        comments.append(comments_count)
        communities.append(post.community.community_name)

    return render_template('frontpage.html', posts=posts, votes=votes, comments=comments,
                            communities=communities)


@app.route('/community/new', methods=['GET', 'POST'])
@login_required
def new_community():
    '''
    Create a new community subkeddit route.
    '''
    # from forms.py
    form = CommunityForm()

    if form.validate_on_submit():
        name = (form.community_name.data).lower()
        name = name.replace(" ", "")

        # Check if Commmunity name exists. Redirect if it does. Otherwise, process.
        if Community.query.filter_by(community_name=name).first():
            flash('Community name taken. Please try again.', 'danger')
            redirect('/community/new')
        else:
            community = Community(user_id=current_user.id, community_name=name)
            db.session.add(community)
            db.session.commit()
            flash('Your community has been created!', 'success')
            return redirect(url_for('community_list'))
    return render_template('create_community.html', form=form)


@app.route("/communities")
def community_list():
    """Community list route which displays all subkeddits on Keddit."""
    communities = Community.query.order_by('community_name').all()
    return render_template("community_list.html", communities=communities)


@app.route("/k/<community_name>")
def view_community(community_name):
    '''
    Community subkeddit view route. Displays the subkeddit's main page where 
    the collection of highest voted content posts are displayed at the top.
    '''

    # Object community
    community = Community.query.filter_by(community_name=community_name).first()
    # Get all posts for the community in descending order
    posts = Post.query.filter_by(community_id=community.id).order_by(Post.date.desc()).all()
    # Total member count
    members_count = CommunityMembers.query.filter_by(community_id=community.id).count()

    votes = []
    comments = []
    cloudinary_image=[]
    # For each post in Posts(Post query above), get the upvotes and downvotes... 
    # ...for each post_id
    # Then append them to a list after subtracting.
    for post in posts:
        upvote = PostRatings.query.filter(PostRatings.post_id==post.id, PostRatings.upvote>=1).count()
        downvote = PostRatings.query.filter(PostRatings.post_id==post.id, PostRatings.downvote>=1).count()
        votes.append(upvote - downvote)
        comments_count = Comment.query.filter_by(post_id=post.id).count()
        comments.append(comments_count)

        #cloud the prefixes and other things then add together then append
        if post.cloud_version != None and post.cloud_version != None and post.cloud_public_id != None and post.cloud_format != None:
        
            cloudinary_image.append(post.cloudinary_url)

    return render_template('community.html', community=community, posts=posts, 
                        members_count=members_count, votes = votes, comments=comments,
                        cloudinary_image=cloudinary_image)


@app.route("/k/<community_name>/join")
@login_required
def join_community(community_name):
    '''Community join route. Allows users to join a community subkeddit.'''

    # Query objects
    community = Community.query.filter_by(community_name=community_name).first()
    member = CommunityMembers.query.filter(CommunityMembers.user_id==current_user.id, CommunityMembers.community_id==community.id).first()

    # Add member to subkeddit if they do not currently belong
    if member == None:
       new_member = CommunityMembers(user_id=current_user.id, community_id=community.id)
       db.session.add(new_member)
       db.session.commit()
       flash('You have successfully joined ' + community_name + '!', 'success')
       return redirect('/k/'+community_name)
    else:
        flash('There was an error in joining.', 'danger')
        return redirect('/k/'+community_name)


@app.route("/k/<community_name>/post/new", methods=['GET', 'POST'])
@login_required
def new_post(community_name):
    '''
    Create new post route. Allows users to create a new post in it's specific
    community. Registered user login required.
    '''
    # Queries
    community = Community.query.filter_by(community_name=community_name).first()
    members_count = CommunityMembers.query.filter_by(community_id=community.id).count()

    form = PostForm()
    if form.validate_on_submit():
        # If a picture is uploaded:
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            # Upload Picture to Cloudinary
            cloudinary_response = cloudinary.uploader.upload("./static/images/" + picture_file)
            # Performing debug print statement to see options:
            # print(dir(cloudinary_response))
            # Create picture's cloudinary url
            # Cloudinary_response.public_id example to get items
            cloudinary_url = cloudinary_prefix + str(cloudinary_response['version']) + "/" + str(cloudinary_response['public_id']) + "." + str(cloudinary_response['format']) 
    
            post = Post(user_id=current_user.id, community_id=community.id, title=form.title.data,
                        body=form.content.data, image_url=picture_file, cloud_version=cloudinary_response['version'],
                        cloud_public_id=cloudinary_response['public_id'], cloud_format= cloudinary_response['format'],
                        cloudinary_url=cloudinary_url)

            db.session.add(post)
            db.session.commit()
            flash('Your post has been created!', 'success')
            # How to route user back to the community's page efficiently?
            return redirect('/k/'+community_name)

        else:
            post = Post(user_id=current_user.id, community_id=community.id, title=form.title.data,
                        body=form.content.data)
            db.session.add(post)
            db.session.commit()
            flash('Your post has been created!', 'success')
            return redirect('/k/'+community_name)
    return render_template('create_post.html', form=form, community=community, 
                                legend='New Post', members_count=members_count)


@app.route("/k/<community_name>/giphy/new", methods=['GET', 'POST'])
@login_required
def create_giphy(community_name):
    '''
    Create GIPHY post route. Allows users to use Giphy's API to create posts
    with gif images.
    '''

    community = Community.query.filter_by(community_name=community_name).first()
    members_count = CommunityMembers.query.filter_by(community_id=community.id).count()

    form = GiphyForm()
    if form.validate_on_submit():
        if form.giphy_url.data:
            # Upload Picture to Cloudinary
            cloudinary_response = cloudinary.uploader.upload(form.giphy_url.data)
            # Performing debug print statement to see options:
            # print(dir(cloudinary_response))
            # Create picture's cloudinary url
            # Cloudinary_response.public_id example to get items
            cloudinary_url = cloudinary_prefix + str(cloudinary_response['version']) + "/" + str(cloudinary_response['public_id']) + "." + str(cloudinary_response['format'])
            
            post = Post(user_id=current_user.id, community_id=community.id, title=form.title.data,
                        body=form.content.data, image_url=form.giphy_url.data, cloud_version=cloudinary_response['version'],
                        cloud_public_id=cloudinary_response['public_id'], cloud_format= "." + cloudinary_response['format'],
                        cloudinary_url=cloudinary_url)

            db.session.add(post)
            db.session.commit()
            flash('Your post has been created!', 'success')
            return redirect('/k/'+community_name)

        else:
            post = Post(user_id=current_user.id, community_id=community.id, title=form.title.data,
                        body=form.content.data)
            db.session.add(post)
            db.session.commit()

            flash('Your post has been created!', 'success')
            return redirect('/k/'+community_name)
    return render_template('create_giphy.html', form=form, community=community,
                                            legend='New Post', members_count=members_count)


# GIHPY API
@app.route("/giphy/<query>")
@login_required
def giphy(query):
    '''
    Searches Giphy's API for gif's based on user search input. Returns a json
    of the first five images.
    '''
    query = urllib.parse.quote(query)
    giphy_prefix = 'https://i.giphy.com/media/'
    giphy_reponse = json.loads(urllib.request.urlopen("http://api.giphy.com/v1/gifs/search?q=" + query + "&api_key=" + GIPHY_API_KEY + "&limit=5").read())
    # Grab the first 5 gif images
    data = giphy_reponse['data'][0]['images']['original']['url']
    data2 = giphy_reponse['data'][1]['images']['original']['url']
    data3 = giphy_reponse['data'][2]['images']['original']['url']
    data4 = giphy_reponse['data'][3]['images']['original']['url']
    data5 = giphy_reponse['data'][4]['images']['original']['url']


    # Creating the giphy url with only the image results directly
    data_id = giphy_reponse['data'][0]['id']
    giphy_url1 = giphy_prefix + data_id + "/giphy.gif"
   
    data_id = giphy_reponse['data'][1]['id']
    giphy_url2 = giphy_prefix + data_id + "/giphy.gif"

    data_id = giphy_reponse['data'][2]['id']
    giphy_url3 = giphy_prefix + data_id + "/giphy.gif"

    data_id = giphy_reponse['data'][3]['id']
    giphy_url4 = giphy_prefix + data_id + "/giphy.gif"

    data_id = giphy_reponse['data'][4]['id']
    giphy_url5 = giphy_prefix + data_id + "/giphy.gif"

    # data_list = [data, data2, data3, data4, data5]
    data_list = [giphy_url1, giphy_url2, giphy_url3, giphy_url4, giphy_url5] 

    return json.dumps(data_list, sort_keys=True, indent=4)



@app.route("/k/<community_name>/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id, community_name):
    '''
    Single post view route. Displays the selected post and comments.
    '''
    post = Post.query.get_or_404(post_id)
    form = SendTextForm()

    # Object Queries
    community = Community.query.filter_by(community_name=community_name).first()
    members_count = CommunityMembers.query.filter_by(community_id=community.id).count()
    comments = Comment.query.filter_by(post_id=post_id).all()
    comments_count = Comment.query.filter_by(post_id=post_id).count()

    # Filter by post id and upvote count, get total, do same for downvote. then subtract.
    upvote = PostRatings.query.filter(PostRatings.post_id==post_id, PostRatings.upvote>=1).count()
    downvote = PostRatings.query.filter(PostRatings.post_id==post_id, PostRatings.downvote>=1).count()
    rating_count = upvote - downvote

    
    votes = []
    # For each comment in comments (comment query above), get the upvotes and downvotes for each post_id
    # Then append them to a list after subtracting.
    for comment in comments:
        # filter by comment id and upvote count, get total, do same for downvote. then subtract.
        upvote = CommentRatings.query.filter(CommentRatings.comment_id==comment.id, CommentRatings.upvote>=1).count()
        downvote = CommentRatings.query.filter(CommentRatings.comment_id==comment.id, CommentRatings.downvote>=1).count()
        votes.append(upvote - downvote)

    return render_template('post.html', post=post, community=community, 
                                        comments=comments, 
                                        comments_count=comments_count, 
                                        rating_count=rating_count,
                                        upvote_count=upvote,
                                        downvote_count=downvote, votes=votes,
                                        members_count=members_count,
                                        form=form)


@app.route("/k/<community_name>/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id, community_name):
    '''
    Update Edit Post route. Allows users to edit their previously made post.
    '''
    post = Post.query.get_or_404(post_id)
    community = Community.query.filter_by(community_name=community_name).first()
    members_count = CommunityMembers.query.filter_by(community_id=community.id).count()
    if post.creator != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.body=form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect('/k/'+community_name+'/post/'+str(post.id))
    elif request.method == 'GET':    
        form.title.data=post.title
        form.content.data=post.body
    return render_template('create_post.html', form=form, post=post,community=community, 
                                     legend='Update Post', members_count=members_count)


@app.route("/k/<community_name>/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id, community_name):
    '''
    Delete Post route. Allows users to delete their previously made post.
    '''
    post = Post.query.get_or_404(post_id)
    ratings_query = PostRatings.query.filter_by(post_id=post_id).delete(synchronize_session=False)
    comment_rating_query= CommentRatings.query.filter_by(post_id=post_id).delete(synchronize_session=False)
    comment_query = Comment.query.filter_by(post_id=post_id).delete(synchronize_session=False)

    # Redirect user
    community = Community.query.filter_by(community_name=community_name).first()
    if post.creator != current_user:
        abort(403)
    
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect('/k/'+community_name)



@app.route("/k/<community_name>/post/<int:post_id>/comment/new", 
                                                        methods=['GET','POST'])
@login_required
def create_comment(post_id, community_name):
    ''' Create comment route. Allows users to write comments on posts.'''

    community = Community.query.filter_by(community_name=community_name).first()
    members_count = CommunityMembers.query.filter_by(community_id=community.id).count()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(user_id=current_user.id, post_id=post_id,
                            body=form.content.data)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been created!', 'success')
        return redirect("/k/"+community_name+"/post/"+str(post_id))
    return render_template('create_comment.html', form=form, members_count=members_count,
                                community=community)




@app.route("/k/<community_name>/post/<int:post_id>/comment/<int:comment_id>", methods=['GET', 'POST'])
def comment(post_id, community_name, comment_id):
    ''' View single comment route. Allows users to view a single comment'''

    post = Post.query.get_or_404(post_id)
    community = Community.query.filter_by(community_name=community_name).first()
    members_count = CommunityMembers.query.filter_by(community_id=community.id).count()
    comment = Comment.query.get(comment_id)


    # filter by comment id and upvote count, get total, do same for downvote. then subtract.
    upvote = CommentRatings.query.filter(CommentRatings.comment_id==comment_id, CommentRatings.upvote>=1).count()
    downvote = CommentRatings.query.filter(CommentRatings.comment_id==comment_id, CommentRatings.downvote>=1).count()
    rating_count = upvote - downvote


    return render_template('comment.html', post=post, community=community, 
                                    comment=comment, rating_count=rating_count,
                                    members_count=members_count)



@app.route("/k/<community_name>/post/<int:post_id>/comment/<int:comment_id>/update", 
                                                        methods=['GET', 'POST'])
@login_required
def update_comment(post_id, community_name, comment_id):
    ''' Update Edit comment route. Allows users to edit their comments.'''

    post = Post.query.get_or_404(post_id)
    community = Community.query.filter_by(community_name=community_name).first()
    members_count = CommunityMembers.query.filter_by(community_id=community.id).count()
    comment = Comment.query.get(comment_id)
    if comment.creator != current_user:
        abort(403)
    form = CommentForm()
    if form.validate_on_submit():
        comment.body=form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect('/k/'+community_name+'/post/'+str(post.id))
    elif request.method == 'GET':    
        form.content.data=comment.body
    return render_template('create_comment.html', form=form, post=post,community=community, 
                                legend='Update Post', members_count=members_count)


@app.route("/k/<community_name>/post/<int:post_id>/comment/<int:comment_id>/delete",
                                                    methods=['POST'])
@login_required
def delete_comment(post_id, community_name, comment_id):
    ''' Delete comment route. Allows users to delete their comments.'''

    post = Post.query.get_or_404(post_id)
    community = Community.query.filter_by(community_name=community_name).first()
    comment_rating_query= CommentRatings.query.filter_by(post_id=post_id).delete(synchronize_session=False)
    comment = Comment.query.get(comment_id)
    if comment.creator != current_user:
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash('Your comment has been deleted!', 'success')
    return redirect('/k/'+community_name+'/post/'+str(post.id))



@app.route("/k/<community_name>/posts/<int:post_id>/upvote")
@login_required
def upvote(community_name, post_id):
    ''' Upvote post route. Allows upvotes on posts.'''

    post_rating=PostRatings(user_id=current_user.id,post_id=post_id,upvote=1)
    db.session.add(post_rating)
    db.session.commit()

    # Increment votecount in our Post table, commit to save changes
    rating = Post.query.get_or_404(post_id)
    rating.votecount += 1
    db.session.add(rating)
    db.session.commit()

    downvote_count = PostRatings.query.filter_by(post_id=post_id, downvote=1).count()
    upvote_count = PostRatings.query.filter_by(post_id=post_id, upvote=1).count()
    vote_count = upvote_count - downvote_count

    return jsonify({'vote_count': vote_count, 'post_id': post_id})


@app.route("/k/<community_name>/posts/<int:post_id>/downvote")
@login_required
def downvote(community_name, post_id):
    ''' Downvote post route. Allows downvotes on posts.'''

    post_rating=PostRatings(user_id=current_user.id,post_id=post_id,downvote=1)
    db.session.add(post_rating)
    db.session.commit()

    # Decrement votecount in our Post table, commit to save changes
    rating = Post.query.get_or_404(post_id)
    rating.votecount -= 1
    db.session.add(rating)
    db.session.commit()

    downvote_count = PostRatings.query.filter_by(post_id=post_id, downvote=1).count()
    upvote_count = PostRatings.query.filter_by(post_id=post_id, upvote=1).count()
    vote_count = upvote_count - downvote_count

    return jsonify({'vote_count': vote_count, 'post_id': post_id})



@app.route("/k/<community_name>/post/<int:post_id>/comment/<int:comment_id>/upvote")
@login_required
def upvote_comment(community_name, post_id, comment_id):
    ''' Upvote comment route. Allows upvotes on comments.'''

    comment_rating=CommentRatings(user_id=current_user.id, post_id=post_id, comment_id=comment_id,upvote=1)
    db.session.add(comment_rating)
    db.session.commit()

    upvote = CommentRatings.query.filter(CommentRatings.comment_id==comment_id, CommentRatings.upvote>=1).count()
    downvote = CommentRatings.query.filter(CommentRatings.comment_id==comment_id, CommentRatings.downvote>=1).count()
    vote_count = upvote - downvote

    return jsonify({'vote_count_comment': vote_count, 'comment_id': comment_id})


@app.route("/k/<community_name>/post/<int:post_id>/comment/<int:comment_id>/downvote")
@login_required
def downvote_comment(community_name, post_id, comment_id):
    ''' Downvote comment route. Allows downvotes on comments.'''

    comment_rating=CommentRatings(user_id=current_user.id, post_id=post_id, comment_id=comment_id,downvote=1)
    db.session.add(comment_rating)
    db.session.commit()

    upvote = CommentRatings.query.filter(CommentRatings.comment_id==comment_id, CommentRatings.upvote>=1).count()
    downvote = CommentRatings.query.filter(CommentRatings.comment_id==comment_id, CommentRatings.downvote>=1).count()
    vote_count = upvote - downvote

    return jsonify({'vote_count_comment': vote_count, 'comment_id': comment_id})


@app.route("/user/<string:username>")
def user_account(username):
    ''' User page where all user posts are displayed.'''

    user= User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(creator=user).order_by(Post.date.desc()).all()
    
    votes = []
    comments = []
    communities= []
    # For each post in Posts(Post query above), get the upvotes and downvotes for each post_id
    # Then append them to a list after subtracting.
    for post in posts:
        upvote = PostRatings.query.filter(PostRatings.post_id==post.id, PostRatings.upvote>=1).count()
        downvote = PostRatings.query.filter(PostRatings.post_id==post.id, PostRatings.downvote>=1).count()
        votes.append(upvote - downvote)
        comments_count = Comment.query.filter_by(post_id=post.id).count()
        comments.append(comments_count)
        communities.append(post.community.community_name)

    return render_template('user_account.html', posts=posts, user=user, 
        votes=votes, comments=comments, communities=communities)


@app.route("/k/<community_name>/post/<int:post_id>/send_sms", methods=['GET', 'POST'])
def send_twilio_sms(community_name, post_id):
    ''' Twilio SMS route. Allows users to send posts via Twilio SMS to phone
    numbers. Due to free account, a default number exists.'''

    form = SendTextForm()

    if form.validate_on_submit():
        post = Post.query.get_or_404(post_id)
        if post.image_url != None and post.body != None:
            flash('Your post has been shared!', 'success')
            message = twilio_client.messages \
                        .create(
                             body="\n\n Sent from Keddit! \n\n" + \
                             "Posted by u/" + post.creator.username + "\n\n" +\
                             "**************" +"\n"+\
                             "k/" + community_name + "\n" +\
                             "**************\n" +\
                             post.title + "\n\n" + post.body,
                             media_url=post.cloudinary_url,
                             from_=config['twilio']['twilio_number'],
                             to=config['twilio']['register_number']
                         )
        elif post.body == None and post.image_url == None:
             flash('Your post has been shared!', 'success')
             message = twilio_client.messages \
                    .create(
                         # body="\n\n Sent from Keddit k/" + community_name + " posted by user u/" + post.creator.username + "\n\n" + post.title,
                         # from_='+14154668578',
                         # to='+14153100618'

                          body="\n\n Sent from Keddit! \n\n" + \
                             "Posted by u/" + post.creator.username + "\n\n" +\
                             "**************" +"\n"+\
                             "k/" + community_name + "\n" +\
                             "**************\n" +\
                             post.title ,
                             from_=config['twilio']['twilio_number'],
                             to=config['twilio']['register_number']
                     )
        elif post.body != None and post.image_url == None:
                flash('Your post has been shared!', 'success')
                message = twilio_client.messages \
                        .create(
                             # body="\n\n Sent from Keddit k/" + community_name + " posted by user u/" + post.creator.username + "\n\n" + post.title + "\n*********"+ "\n\n" + post.body,
                             # from_='+14154668578',
                             # to='+14153100618'

                              body="\n\n Sent from Keddit! \n\n" + \
                             "Posted by u/" + post.creator.username + "\n\n" +\
                             "**************" +"\n"+\
                             "k/" + community_name + "\n" +\
                             "**************\n" +\
                             post.title + "\n\n" + post.body,
                             from_=config['twilio']['twilio_number'],
                             to=config['twilio']['register_number']
                         )
        elif post.body == None and post.image_url != None:
                flash('Your post has been shared!', 'success')
                message = twilio_client.messages \
                        .create(
                            # body="\n\n Sent from Keddit k/" + community_name + " posted by user u/" + post.creator.username + "\n\n" + post.title + "\n*********"+ "\n\n" + post.image_url,
                            # from_='+14154668578',
                            # to='+14153100618'

                             body="\n\n Sent from Keddit! \n\n" + \
                             "Posted by u/" + post.creator.username + "\n\n" +\
                             "**************" +"\n"+\
                             "k/" + community_name + "\n" +\
                             "**************\n" +\
                             post.title,
                             media_url= post.cloudinary_url,
                             from_=config['twilio']['twilio_number'],
                             to=config['twilio']['register_number']
                         )

    print(message.sid)
    return redirect('/k/'+community_name+'/post/'+str(post_id))

#____________________________________________________________

if __name__ == "__main__":
    app.debug = False

    connect_to_db(app)
    login_manager.init_app(app)
    login_manager.login_view = "/login"
    login_manager.login_message_category = 'info'

    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")