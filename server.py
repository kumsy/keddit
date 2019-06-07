"""keddit! The second to the frontpage of the internet."""
import os
import secrets
from jinja2 import StrictUndefined

from flask import (Flask, render_template, request, flash, redirect, 
                    session, url_for, abort, jsonify)
from sqlalchemy import desc
from flask_debugtoolbar import DebugToolbarExtension

from model import (connect_to_db, db, User, Community, CommunityMembers, 
                    Post, PostRatings, Comment, CommentRatings)
from forms import (RegistrationForm, LoginForm, CommunityForm, 
                    AccountForm, PostForm, CommentForm, GiphyForm)
from flask_bcrypt import Bcrypt
from flask_login import (LoginManager, login_user, logout_user, 
                        login_required, current_user)
import pprint
# ========================================================
# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client

# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACf3bae2605bab0efbacb4041fec3d4607'
auth_token = 'a82c75c523f72070f23d4f5140aa5fcd'
client = Client(account_sid, auth_token)
# ====================================================

# Cloudinary settings using python code. Run before pycloudinary is used.
import cloudinary
import cloudinary.uploader
import cloudinary.api
cloudinary.config(
  cloud_name = 'kumy',  
  api_key = '566847115659738',  
  api_secret = 'l71iJ_LJuwMuNC0AXvKczB5_rJU'  
)
# print(dir(cloudinary))

# ====================================================
# GIPHY API

# python
import urllib,json
GIPHY_API_KEY = 'MJ8oCijRkr4DSVxOeJtomQ8zAGDlHeYo'


#=====================================================
app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC123"

# Raises an error in Jinja2 for to debug
app.jinja_env.undefined = StrictUndefined

# Handle User Logins
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


#==========================
cloudinary_prefix = 'https://res.cloudinary.com/kumy/image/upload/v' 


# Landing Page route
@app.route('/')
def home():
    """Homepage."""

    form =  LoginForm()
    signup = RegistrationForm()

    return render_template("landing_page.html", form = form, signup=signup)

# Registration Page Route
@app.route('/registration', methods=['GET', 'POST'])
def register_form():
    """Show form for user signup."""

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

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Show login form."""
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

# Logout route
@app.route('/logout')
def logout():
    """Log out."""
    image_file = url_for('static', filename='images/' + current_user.image_file)
    logout_user()
    flash("Logged Out. Hope to see you again!", 'success')
    return redirect("/")

# User Profile picture
def save_picture(form_picture):
    # Hash filename to not error with other similar file names
    random_hex = secrets.token_hex(8)
    # Get extenstion of picture being uploaded
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/images', picture_fn)
    
    form_picture.save(picture_path)

    return picture_fn

# User Account route page
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
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

# ******************************
# Keddit's main frontpage route
# ******************************
@app.route('/home')
def frontpage():

    posts = Post.query.order_by(desc(Post.votecount)).all()
    # community = Community.query.filter_by(id=Post.community_id).all()

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

        if post.cloud_version != None and post.cloud_version != None and post.cloud_public_id != None and post.cloud_format != None:
            cloudinary_url = cloudinary_prefix + post.cloud_version + "/" + post.cloud_public_id + post.cloud_format
            print(cloudinary_url)
        else:
            cloudinary_url = None

    return render_template('frontpage.html', posts=posts, votes=votes, comments=comments,
                            communities=communities, cloudinary_image=cloudinary_url)

# Create Community route
@app.route('/community/new', methods=['GET', 'POST'])
@login_required
def new_community():
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
            return redirect(url_for('frontpage'))


    return render_template('create_community.html', form=form)

@app.route("/communities")
def community_list():
    """Show list of communities"""

    communities = Community.query.order_by('community_name').all()
    return render_template("community_list.html", communities=communities)

# Display communitys with posts
@app.route("/k/<community_name>")
def view_community(community_name):

    # Object community
    community = Community.query.filter_by(community_name=community_name).first()
    # Get all posts for the community
    # posts = Post.query.filter_by(community_id=community.id).all() # from community object
    posts = Post.query.filter_by(community_id=community.id).order_by(Post.date.desc()).all()
    # Get total number of members in the community
    members_count = CommunityMembers.query.filter_by(community_id=community.id).count()
    # comments_count = Comment.query.filter_by(post_id=posts.id).count()

    

    # if post.cloud_version != None and post.cloud_version != None and post.cloud_public_id != None and post.cloud_format != None:
    #     cloudinary_url = cloudinary_prefix + post.cloud_version + "/" + post.cloud_public_id + post.cloud_format
    #     print(cloudinary_url)
    # else:
    #     cloudinary_url = None

    
    votes = []
    comments = []
    cloudinary_image=[]
    # For each post in Posts(Post query above), get the upvotes and downvotes for each post_id
    # Then append them to a list after subtracting.
    for post in posts:
        upvote = PostRatings.query.filter(PostRatings.post_id==post.id, PostRatings.upvote>=1).count()
        downvote = PostRatings.query.filter(PostRatings.post_id==post.id, PostRatings.downvote>=1).count()
        votes.append(upvote - downvote)
        comments_count = Comment.query.filter_by(post_id=post.id).count()
        comments.append(comments_count)

        #cloud the prefixes and other things then add together then append
        if post.cloud_version != None and post.cloud_version != None and post.cloud_public_id != None and post.cloud_format != None:
            Post.query.filter_by(cloud_version).first()
            cloudinary_url = cloudinary_prefix + post.cloud_version + "/" + post.cloud_public_id + post.cloud_format
            cloudinary_image.append(cloudinary_url)
            print(cloudinary_image)
        else:
            cloudinary_image.append(None)
            cloudinary_url = None
    print(comments, "**********************")

        

    return render_template('community.html', community=community, posts=posts, 
                        members_count=members_count, votes = votes, comments=comments,
                        cloudinary_image=cloudinary_url)

# Join Communities
@app.route("/k/<community_name>/join")
@login_required
def join_community(community_name):
    '''Users can join communities'''

    community = Community.query.filter_by(community_name=community_name).first()
    member = CommunityMembers.query.filter(CommunityMembers.user_id==current_user.id, CommunityMembers.community_id==community.id).first()
    print(member)
    if member == None:
       new_member = CommunityMembers(user_id=current_user.id, community_id=community.id)
       db.session.add(new_member)
       db.session.commit()
       flash('You have successfully joined ' + community_name + '!', 'success')
       return redirect('/k/'+community_name)
    else:
        flash('There was an error in joining.', 'danger')
        return redirect('/k/'+community_name)



# CREATE A NEW POST
@app.route("/k/<community_name>/post/new", methods=['GET', 'POST'])
@login_required
def new_post(community_name):

    community = Community.query.filter_by(community_name=community_name).first()

    form = PostForm()
    if form.validate_on_submit():
        # Put data into our database here
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            #Upload Picture to Cloudinary
            # cloudinary.uploader.upload("./static/images/" + picture_file)

            cloudinary_response = cloudinary.uploader.upload("./static/images/" + picture_file)
            print(cloudinary_response)
            print(dir(cloudinary_response))
            print(cloudinary_response['public_id'])
            #cloudinary_response.public_idj example to get items
            post = Post(user_id=current_user.id, community_id=community.id, title=form.title.data,
                        body=form.content.data, image_url=picture_file, cloud_version=cloudinary_response['version'],
                        cloud_public_id=cloudinary_response['public_id'], cloud_format= "." + cloudinary_response['format'])

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
            # How to route user back to the community's page efficiently?
            return redirect('/k/'+community_name)
    return render_template('create_post.html', form=form, community=community, 
                                                            legend='New Post')


# Create GIPHY
@app.route("/k/<community_name>/giphy/new", methods=['GET', 'POST'])
@login_required
def create_giphy(community_name):

    community = Community.query.filter_by(community_name=community_name).first()

    form = GiphyForm()

    if form.validate_on_submit():
        if form.giphy_url.data:
            #Upload Picture to Cloudinary
            # cloudinary.uploader.upload(form.giphy_url.data)

            cloudinary_response = cloudinary.uploader.upload(form.giphy_url.data)
            print(cloudinary_response)
            print(dir(cloudinary_response))
            print(cloudinary_response['public_id'])
            #cloudinary_response.public_idj example to get items
            post = Post(user_id=current_user.id, community_id=community.id, title=form.title.data,
                        body=form.content.data, image_url=form.giphy_url.data, cloud_version=cloudinary_response['version'],
                        cloud_public_id=cloudinary_response['public_id'], cloud_format= "." + cloudinary_response['format'])

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
            # How to route user back to the community's page efficiently?
            return redirect('/k/'+community_name)



        # return jsonify({'giphy_results': data_list})

    return render_template('create_giphy.html', form=form, community=community,
                                            legend='New Post')


# GIHPY API
@app.route("/giphy/<query>")
@login_required
def giphy(query):
    print(query)
    query = urllib.parse.quote(query)
    print(query)
    giphy_prefix = 'https://i.giphy.com/media/'
    giphy_reponse = json.loads(urllib.request.urlopen("http://api.giphy.com/v1/gifs/search?q=" + query + "&api_key=" + GIPHY_API_KEY + "&limit=5").read())
    data = giphy_reponse['data'][0]['images']['original']['url']
    data2 = giphy_reponse['data'][1]['images']['original']['url']
    data3 = giphy_reponse['data'][2]['images']['original']['url']
    data4 = giphy_reponse['data'][3]['images']['original']['url']
    data5 = giphy_reponse['data'][4]['images']['original']['url']
    print("*****************************************************************")
    # print(giphy_reponse)
    # print(data)
    # print(data2)
    # print(data3)
    # print(data4)
    # print(data5)

    # Creating the giphy url with only the image results directly
    data_id = giphy_reponse['data'][0]['id']
    giphy_url1 = giphy_prefix + data_id + "/giphy.webp"
    # print(giphy_url)
    data_id = giphy_reponse['data'][1]['id']
    giphy_url2 = giphy_prefix + data_id + "/giphy.webp"

    data_id = giphy_reponse['data'][2]['id']
    giphy_url3 = giphy_prefix + data_id + "/giphy.webp"

    data_id = giphy_reponse['data'][3]['id']
    giphy_url4 = giphy_prefix + data_id + "/giphy.webp"

    data_id = giphy_reponse['data'][4]['id']
    giphy_url5 = giphy_prefix + data_id + "/giphy.webp"

    # data_list = [data, data2, data3, data4, data5]
    data_list = [giphy_url1, giphy_url2, giphy_url3, giphy_url4, giphy_url5]


    # What will my route or return json object look like
    # In a GIPHY object, we need an array of original url's. Element of 5 items and return it's urls.
    # In the front end, display these urls as images.
    # Put the giphy url in the Post table instead of the image url
    # When I choose on the front end the giphy I want, 

    return json.dumps(data_list, sort_keys=True, indent=4)




# VIEW SINGLE POST
@app.route("/k/<community_name>/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id, community_name):
    post = Post.query.get_or_404(post_id)

    if post.cloud_version != None and post.cloud_version != None and post.cloud_public_id != None and post.cloud_format != None:
        cloudinary_url = cloudinary_prefix + post.cloud_version + "/" + post.cloud_public_id + post.cloud_format
        print(cloudinary_url)
    else:
        cloudinary_url = None


    community = Community.query.filter_by(community_name=community_name).first()

    comments = Comment.query.filter_by(post_id=post_id).all()
    comments_count = Comment.query.filter_by(post_id=post_id).count()
    # filter by post id and upvote count, get total, do same for downvote. then subtract.
    upvote = PostRatings.query.filter(PostRatings.post_id==post_id, PostRatings.upvote>=1).count()
    downvote = PostRatings.query.filter(PostRatings.post_id==post_id, PostRatings.downvote>=1).count()
    rating_count = upvote - downvote

    # print (post.ratings)

    #comment upvote and downvotes
    votes = []
    # For each post in Posts(Post query above), get the upvotes and downvotes for each post_id
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
                                        cloudinary_image=cloudinary_url)

# UPDATE POST
@app.route("/k/<community_name>/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id, community_name):
    post = Post.query.get_or_404(post_id)
    community = Community.query.filter_by(community_name=community_name).first()
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
                                                        legend='Update Post')
# DELETE POST
@app.route("/k/<community_name>/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id, community_name):
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


# CREATE COMMENT
@app.route("/k/<community_name>/post/<int:post_id>/comment/new", 
                                                        methods=['GET','POST'])
@login_required
def create_comment(post_id, community_name):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(user_id=current_user.id, post_id=post_id,
                            body=form.content.data)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been created!', 'success')
        return redirect("/k/"+community_name+"/post/"+str(post_id))
    return render_template('create_comment.html', form=form)



# VIEW SINGLE COMMENT
@app.route("/k/<community_name>/post/<int:post_id>/comment/<int:comment_id>", methods=['GET', 'POST'])
def comment(post_id, community_name, comment_id):
    post = Post.query.get_or_404(post_id)
    community = Community.query.filter_by(community_name=community_name).first()
    comment = Comment.query.get(comment_id)


    # filter by comment id and upvote count, get total, do same for downvote. then subtract.
    upvote = CommentRatings.query.filter(CommentRatings.comment_id==comment_id, CommentRatings.upvote>=1).count()
    downvote = CommentRatings.query.filter(CommentRatings.comment_id==comment_id, CommentRatings.downvote>=1).count()
    rating_count = upvote - downvote


    return render_template('comment.html', post=post, community=community, 
                                    comment=comment, rating_count=rating_count)




# UPDATE COMMENT
@app.route("/k/<community_name>/post/<int:post_id>/comment/<int:comment_id>/update", 
                                                        methods=['GET', 'POST'])
@login_required
def update_comment(post_id, community_name, comment_id):
    post = Post.query.get_or_404(post_id)
    community = Community.query.filter_by(community_name=community_name).first()
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
                                                        legend='Update Post')
# DELETE COMMENT
@app.route("/k/<community_name>/post/<int:post_id>/comment/<int:comment_id>/delete",
                                                    methods=['POST'])
@login_required
def delete_comment(post_id, community_name, comment_id):
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


# UPVOTE POST
@app.route("/k/<community_name>/posts/<int:post_id>/upvote")
@login_required
def upvote(community_name, post_id):
    # Post.query.filter_by(post_id=post_id).votecount+=1

    post_rating=PostRatings(user_id=current_user.id,post_id=post_id,upvote=1)
    db.session.add(post_rating)
    db.session.commit()

    # Increment votecount in our Post table, commit to save changes
    rating = Post.query.get_or_404(post_id)
    rating.votecount += 1
    db.session.add(rating)
    db.session.commit()

    # rating_count = PostRatings.query.filter_by(post_id=post_id).count()
    downvote_count = PostRatings.query.filter_by(post_id=post_id, downvote=1).count()
    upvote_count = PostRatings.query.filter_by(post_id=post_id, upvote=1).count()

    vote_count = upvote_count - downvote_count


    """ Upvote steps (single)
    check if downvote exists, if it exists, delete it

    Check if a row in post ratings exists for the current user post id and upvote via .count and seeing if it's greater than zero,
    and if it's greater than zero, don't do anything and return the jsonfiy vote count, etc.

    if false:

        do line 499 - 507 (put user upvotes in our db, etc)



    """

    return jsonify({'vote_count': vote_count, 'post_id': post_id})

# DOWNVOTE POST
@app.route("/k/<community_name>/posts/<int:post_id>/downvote")
@login_required
def downvote(community_name, post_id):

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

# UPVOTE COMMENT
@app.route("/k/<community_name>/post/<int:post_id>/comment/<int:comment_id>/upvote")
@login_required
def upvote_comment(community_name, post_id, comment_id):
    comment_rating=CommentRatings(user_id=current_user.id, post_id=post_id, comment_id=comment_id,upvote=1)
    db.session.add(comment_rating)
    db.session.commit()

    upvote = CommentRatings.query.filter(CommentRatings.comment_id==comment_id, CommentRatings.upvote>=1).count()
    downvote = CommentRatings.query.filter(CommentRatings.comment_id==comment_id, CommentRatings.downvote>=1).count()

    vote_count = upvote - downvote


    return jsonify({'vote_count_comment': vote_count, 'comment_id': comment_id})

# DOWNVOTE COMMENT
@app.route("/k/<community_name>/post/<int:post_id>/comment/<int:comment_id>/downvote")
@login_required
def downvote_comment(community_name, post_id, comment_id):
    comment_rating=CommentRatings(user_id=current_user.id, post_id=post_id, comment_id=comment_id,downvote=1)
    db.session.add(comment_rating)
    db.session.commit()
    upvote = CommentRatings.query.filter(CommentRatings.comment_id==comment_id, CommentRatings.upvote>=1).count()
    downvote = CommentRatings.query.filter(CommentRatings.comment_id==comment_id, CommentRatings.downvote>=1).count()

    vote_count = upvote - downvote


    return jsonify({'vote_count_comment': vote_count, 'comment_id': comment_id})


# User Page
@app.route("/user/<string:username>")
def user_account(username):
    user= User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(creator=user).order_by(Post.date.desc()).all()
    # posts = Post.query.order_by(desc(Post.votecount)).all()
    

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

@app.route("/k/<community_name>/post/<int:post_id>/send_sms")
def send_twilio_sms(community_name, post_id):

    post = Post.query.get_or_404(post_id)
    if post.image_url != None and post.body != None:
        message = client.messages \
                    .create(
                         body="\n\n Sent from Keddit! \n\n" + \
                         "Posted by u/" + post.creator.username + "\n\n" +\
                         "**************" +"\n"+\
                         "k/" + community_name + "\n" +\
                         "**************\n" +\
                         post.title + "\n\n" + post.body + "\n\n" + post.image_url,
                         from_='+14154668578',
                         to='+14153100618'
                     )
    elif post.body == None and post.image_url == None:
         message = client.messages \
                .create(
                     body="\n\n Sent from Keddit k/" + community_name + " posted by user u/" + post.creator.username + "\n\n" + post.title,
                     from_='+14154668578',
                     to='+14153100618'
                 )
    elif post.body != None and post.image_url == None:

            message = client.messages \
                    .create(
                         body="\n\n Sent from Keddit k/" + community_name + " posted by user u/" + post.creator.username + "\n\n" + post.title + "\n*********"+ "\n\n" + post.body,
                         from_='+14154668578',
                         to='+14153100618'
                     )
    elif post.body == None and post.image_url != None:
            message = client.messages \
                    .create(
                        body="\n\n Sent from Keddit k/" + community_name + " posted by user u/" + post.creator.username + "\n\n" + post.title + "\n*********"+ "\n\n" + post.image_url,
                        from_='+14154668578',
                        to='+14153100618'
                     )

    print(message.sid)

    # Make Ajax call, can do an input form to get the user "number" also

    return jsonify({'message_sid': message.sid})

#____________________________________________________________

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)
    login_manager.init_app(app)
    login_manager.login_view = "/login"
    login_manager.login_message_category = 'info'

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")