"""    """

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Users, Community, CommunityMembers, Threads, ThreadRatings, Comments, CommentRatings


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/registration', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("registration.html")


@app.route('/registration', methods=['POST'])
def register_process():
    """Test database."""

    # Process registration forms

    # Get form variables

    email = request.form['email']
    username = request.form['username']
    password = request.form['username']

    new_user = Users(username=username, email=email, password=password)

    db.session.add(new_user)
    db.session.commit()


    flash(f"Success! Welcome {username}!")
    return redirect("/")


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form"""

    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_process():
    """Process login"""

    # Get form variables
    email = request.form['email']
    password = request.form['password']

    user = Users.query.filter_by(email=email).first()

    if not user:
        flash("User does not exist")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password. Please try again.")
        return redirect("/login")

    session['user_id'] = user.user_id
    flash("Logged in")
    return redirect(f"/users/{user.user_id}")















#____________________________________________________________

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")