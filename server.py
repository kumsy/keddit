"""keddit! The second to the frontpage of the internet."""
import os
import secrets
from jinja2 import StrictUndefined

from flask import (Flask, render_template, request, flash, redirect, 
                    session, url_for, abort)
from flask_debugtoolbar import DebugToolbarExtension

from model import (connect_to_db, db, User, Community, CommunityMembers, 
                    Post, PostRatings, Comment, CommentRatings)
from forms import (RegistrationForm, LoginForm, CommunityForm, 
                    AccountForm, PostForm, CommentForm)
from flask_bcrypt import Bcrypt
from flask_login import (LoginManager, login_user, logout_user, 
                        login_required, current_user)

app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC123"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

# Handle User Logins
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Landing Page route
@app.route('/')
def home():
    """Homepage."""
    return render_template("homepage.html")

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
    return render_template('frontpage.html')

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

    # Passes the string from parameter
    # Use that string to query the database for community (filter_by)

    # Object community
    community = Community.query.filter_by(community_name=community_name).first()
    # Get all posts for the community
    posts = Post.query.filter_by(community_id=community.id).all() # from community object
    # Get total number of members in the community
    members_count = CommunityMembers.query.filter_by(community_id=community.id).count()
    # comments_count = Comment.query.filter_by(post_id=posts.id).count()

    # filter by post id and upvote count, get total, do same for downvote. then subtract.
    # upvote = PostRatings.query.filter(PostRatings.post_id==post_id, PostRatings.upvote>=1).count()
    # downvote = PostRatings.query.filter(PostRatings.post_id==post_id, PostRatings.downvote>=1).count()
    # rating_count = upvote - downvote
    
    return render_template('community.html', community=community, posts=posts, 
                     members_count=members_count)

# CREATE A NEW POST
@app.route("/k/<community_name>/post/new", methods=['GET', 'POST'])
@login_required
def new_post(community_name):

    community = Community.query.filter_by(community_name=community_name).first()

    form = PostForm()
    if form.validate_on_submit():
        # Put data into our database here
        post = Post(user_id=current_user.id, community_id=community.id, title=form.title.data,
                    body=form.content.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        # How to route user back to the community's page efficiently?
        return redirect('/k/'+community_name)
    return render_template('create_post.html', form=form, community=community, 
                                                            legend='New Post')

# VIEW SINGLE POST
@app.route("/k/<community_name>/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id, community_name):
    post = Post.query.get_or_404(post_id)
    community = Community.query.filter_by(community_name=community_name).first()

    comments = Comment.query.filter_by(post_id=post_id).all()
    comments_count = Comment.query.filter_by(post_id=post_id).count()
    # filter by post id and upvote count, get total, do same for downvote. then subtract.
    upvote = PostRatings.query.filter(PostRatings.post_id==post_id, PostRatings.upvote>=1).count()
    downvote = PostRatings.query.filter(PostRatings.post_id==post_id, PostRatings.downvote>=1).count()
    rating_count = upvote - downvote
    return render_template('post.html', post=post, community=community, 
                                        comments=comments, 
                                        comments_count=comments_count, 
                                        rating_count=rating_count,
                                        upvote_count=upvote,
                                        downvote_count=downvote)

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

    return render_template('comment.html', post=post, community=community, comment=comment)

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
    post_rating=PostRatings(user_id=current_user.id,post_id=post_id,upvote=1)
    db.session.add(post_rating)
    db.session.commit()
    # rating_count = PostRatings.query.filter_by(post_id=post_id).count()
    return redirect('/k/'+community_name+'/post/'+str(post_id))
# DOWNVOTE POST
@app.route("/k/<community_name>/posts/<int:post_id>/downvote")
@login_required
def downvote(community_name, post_id):
    post_rating=PostRatings(user_id=current_user.id,post_id=post_id,downvote=1)
    db.session.add(post_rating)
    db.session.commit()
    return redirect('/k/'+community_name+'/post/'+str(post_id))




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