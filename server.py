"""    """

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session, url_for
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, Users, Community, CommunityMembers, Threads, ThreadRatings, Comments, CommentRatings
from forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/registration', methods=['GET', 'POST'])
def register_form():
    """Show form for user signup."""
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(username=form.username.data, email=form.email.data,
                    password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! Please log in.', 'sucess')
        return redirect('/login')
    return render_template("registration.html", form=form)



# @app.route('/registration', methods=['POST'])
# def register_process():
#     """Test database."""

#     # Process registration forms

#     # Get form variables

#     email = request.form['email']
#     username = request.form['username']
#     username = username.lower()
#     password = request.form['password']

#     new_user = Users(username=username, email=email, password=password)
#     print('NEED TO ERROR CHECK IF USERNAME AND EMAIL ALREADY EXISTS')


#     db.session.add(new_user)
#     db.session.commit()


#     flash(f"Success! Welcome {username}!")
#     return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Show form for user signup."""
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data:
            # put my code here
            flash('You have been logged in!', 'success')
            return redirect('/')
        else:
            flash('Login Unsucessful. Please check username and password.',
                                                                    'danger')
    return render_template("login.html", form=form)

# @app.route('/login', methods=['POST'])
# def login_process():
#     """Process login"""

#     # Get form variables
#     email = request.form['email']
#     password = request.form['password']

#     user = Users.query.filter_by(email=email).first()


#     if not user:
#         flash("User does not exist")
#         return redirect("/login")

#     if user.password != password:
#         flash("Incorrect password. Please try again.")
#         return redirect("/login")

#     username = user.username

#     session['user_id'] = user.user_id
#     flash("Logged in")
#     # return redirect(f"/users/{user.username}")
#     return render_template("frontpage.html")


@app.route('/logout')
def logout():
    """Log out."""

    del session['user_id']
    flash("Logged Out. Hope to see you again!")
    return redirect("/")




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

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")