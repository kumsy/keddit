from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import (UserMixin, LoginManager, login_required, login_user, 
                        logout_user)


db = SQLAlchemy()

# ______________________________________________________________________________

# Model definitions

class User(db.Model, UserMixin):
    """Users of Keddit"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(500), nullable=True, default='default.jpg')

    # Define relationship to communities
    communities_subbed = db.relationship('Community', 
                                  secondary='community_members', 
                                  backref='subscribers')

    communities_created = db.relationship('Community', backref='creator')
    # Define relationship to posts
    posts_created = db.relationship('Post', backref='creator') 

    posts_rated = db.relationship('Post', 
                                    secondary= 'post_ratings',
                                    backref= 'user_ratings')

    # Define relationship to comments
    comments_created = db.relationship('Comment', backref='creator')

    comments_rated = db.relationship('Comment', 
                                    secondary= 'comment_ratings',
                                    backref= 'user_ratings')


    def __repr__(self):
        return "<user_id={}, username={}, email={}, pw={}, image={}>\n".format(
                self.id, self.username, self.email, self.password,
                self.image_file)

class Community(db.Model):
    """Communites of Keddit"""

    __tablename__ = 'communities'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # Created By
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                                                        nullable=False)
    community_name = db.Column(db.String(20), nullable=False, unique=True)

    # subscribers (communities.subscribers): list of users that are part of this community
    # Ex: GameofThrones.subscribers will get all users objs who joined GameOfThrones

    def __repr__(self):
        return "<community_id={}, user_id={}, community_name={}>\n".format(
                self.id, self.user_id, self.community_name)

class CommunityMembers(db.Model):
    """Community Members of Users"""

    # Association Table between Users and Communities

    __tablename__ = 'community_members'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'),
                                                        nullable=False)

    def __repr__(self):
        return "<community_member_id={}, user_id={}, community_id={}>\n".format(
                self.id, self.user_id, self.community_id)



class Post(db.Model):
    """Posts of Keddit"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    community_id = db.Column(db.Integer, db.ForeignKey('communities.id'),
                                                            nullable=False)
    title = db.Column(db.String(30), nullable=False)
    body = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)

    # Author (post.creator) is an User Object

    def __repr__(self):
        return "<post_id={}, user_id={}, community_id={}, title={}, date={}>\n".format(
                self.id, self.user_id, self.community_id, self.title, self.date)


class PostRatings(db.Model):
    """Upvotes and Downvotes on Posts"""

    # Assoication Table between Posts and Users

    __tablename__ = 'post_ratings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                                                        nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), 
                                                        nullable=False)
  
    vote = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return "<rating_id={}, user_id={}, post_id={}, votes={}>\n".format(
                self.id, self.user_id, self.post_id, self.vote)


class Comment(db.Model):
    """User Comments on Posts"""

    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), 
                                                    nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), 
                                                        nullable=False)
    body = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)

    def __repr__(self):
        return "<comment_id={}, user_id={}, post_id={}, date={}\n".format(
                self.id, self.user_id, self.post_id, self.date)

    # comment.author is getting the user obj assoicated with the comment

class CommentRatings(db.Model):
    """Upvotes and Downvotes on Comments"""
    # Assoication Table between Comments and Users

    __tablename__ = 'comment_ratings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), 
                                                        nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'),
                                                        nullable=False)
    vote = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return "<rating_id={}, user_id={}, comment_id={}, date={}\n".format(
                self.id, self.user_id, self.comment_id, self.date)







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

