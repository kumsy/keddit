from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# ______________________________________________________________________________

# Model definitions

class Users(db.Model):
    """Users of Keddit"""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    img_url = db.Column(db.String(500), nullable=True)

    # Define relationship to communities
    communities = db.relationship('Community', 
                                  secondary='community_members', 
                                  backref='subscribers')
    # Define relationship to threads
    threads = db.relationship('Threads',
                                secondary='thread_ratings',
                                backref='author') 
    # Define relationship to comments
    comments = db.relationship('Comments',
                                secondary='comment_ratings',
                                backref='author')


    def __repr__(self):
        return "<user_id={}, username={}, email={}, pw={}, image={}>\n".format(
                self.user_id, self.username, self.email, self.password,
                self.img_url)

class Community(db.Model):
    """Communites of Keddit"""

    __tablename__ = 'communities'

    community_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Creator of the community
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                                                        nullable=False)
    community_name = db.Column(db.String(20), nullable=False, unique=True)

    # subscribers (communities.subscribers): list of users that are part of this community
    # Ex: GameofThrones.subscribers will get all users objs who joined GameOfThrones

    def __repr__(self):
        return "<community_id={}, user_id={}, community_name={}>\n".format(
                self.community_id, self.user_id, self.community_name)

class CommunityMembers(db.Model):
    """Community Members of Users"""

    # Association Table between Users and Communities

    __tablename__ = 'community_members'

    community_member_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.community_id'),
                                                        nullable=False)

    def __repr__(self):
        return "<community_member_id={}, user_id={}, community_id={}>\n".format(
                self.community_member_id, self.user_id, self.community_id)



class Threads(db.Model):
    """Threads of Keddit"""

    __tablename__ = 'threads'

    thread_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.community_id'),
                                                            nullable=False)
    title = db.Column(db.String(30), nullable=False)
    post = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)

    # Author (threads.author) is an User Object

    def __repr__(self):
        return "<thread_id={}, user_id={}, community_id={}, title={}, date={}>\n".format(
                self.thread_id, self.user_id, self.community_id, self.title, self.date)


class ThreadRatings(db.Model):
    """Upvotes and Downvotes on Threads"""

    # Assoication Table between Threads and Users

    __tablename__ = 'thread_ratings'

    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
                                                        nullable=False)
    thread_id = db.Column(db.Integer, db.ForeignKey('threads.thread_id'), 
                                                        nullable=False)
  
    votes = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return "<rating_id={}, user_id={}, thread_id={}, votes={}>\n".format(
                self.rating_id, self.user_id, self.thread_id, self.votes)


class Comments(db.Model):
    """User Comments on threads"""

    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), 
                                                    nullable=False)
    thread_id = db.Column(db.Integer, db.ForeignKey('threads.thread_id'), 
                                                        nullable=False)
    post = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return "<comment_id={}, user_id={}, thread_id={}, date={}\n".format(
                self.comment_id, self.user_id, self.thread_id, self.date)

    # comments.author is getting the user obj assoicated with the comment

class CommentRatings(db.Model):
    """Upvotes and Downvotes on Comments"""
    # Assoication Table between Comments and Users

    __tablename__ = 'comment_ratings'

    rating_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), 
                                                        nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.comment_id'),
                                                        nullable=False)
    votes = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return "<comment_id={}, user_id={}, thread_id={}, date={}\n".format(
                self.comment_id, self.user_id, self.thread_id, self.date)







# ______________________________________________________________________________

# Helper functions

def init_app():
    # So that we can use Flask-SQLAlchemy, we'll make a Flask app.
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    print("Connected to DB 💘")

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///keddit'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    init_app()
    db.create_all()

