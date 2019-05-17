"""keddit! The second to the frontpage of the internet."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, url_for
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Users, Community, CommunityMembers, Threads, ThreadRatings, Comments, CommentRatings
from forms import RegistrationForm, LoginForm, CommunityForm
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

# Handle User Logins
@login_manager.user_loader
def load_user(user_id):
    print("LOAD USER")
    print(user_id)
    return Users.query.get(user_id)

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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(username=form.username.data, email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! Please log in.', 'sucess')
        return redirect('/login')
    
    return render_template("registration.html", form=form)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Show login form."""
    form = LoginForm()

    # When user submits login. Query for email data, validate, and check password.
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        # Validation Check before logging in
        if user and bcrypt.check_password_hash(user.password, form.password.data):

            login_user(user, remember=form.remember.data)
            flash("You are now logged in!")

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
    flash("Logged Out. Hope to see you again!")
    return redirect("/")

# User Account route page
@app.route('/account')
@login_required
def account():
    return render_template('account.html')

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
        # Check if Commmunity name exists. Redirect if it does. Otherwise, process.
        if Community.query.filter_by(community_name=form.community_name.data):
            flash('Community name taken. Please try again.')
            redirect('/community/new')
        else:
            community = Community(user_id=current_user.id, community_name=form.community_name.data)
            db.session.add(community)
            db.session.commit()
            flash('Your community has been created!', 'sucess')
            return redirect(url_for('frontpage'))


    return render_template('create_community.html', form=form)

@app.route("/communities")
def community_list():
    """Show list of communities"""

    communities = Community.query.order_by('community_name').all()
    return render_template("community_list.html", communities=communities)

@app.route("/communities/<community_name>")
def view_community(community_name):

    # Passes the string from parameter
    # Use that string to query the database for community (filter_by)
    print(community_name)
    return community_name
















# When you make account page add this orignally from login route.
# username = user.username

#     session['user_id'] = user.user_id
#     flash("Logged in")
#     return redirect(f"/u/{user.username}")










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