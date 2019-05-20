# Seed our Database
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from model import (User, Community, CommunityMembers,  Post, PostRatings,
                    Comment, CommentRatings, connect_to_db, db)
from server import app, bcrypt


def load_users():
    """ Load users into our database """

    a = User(username="kumsy", email="kristenpincampbell@gmail.com",
            password=bcrypt.generate_password_hash('12').decode('utf-8'))
    b = User(username="ropers", email="riddle@gmail.com",
            password=bcrypt.generate_password_hash('ou812').decode('utf-8'),
            image_file='TK.png')
    c = User(username="kbr22", email="kbr@msn.com",
            password=bcrypt.generate_password_hash('kbr').decode('utf-8'),
            image_file='rex.jpg')
    d = User(username="jedimaster2019", email="jedi@icloud.com",
            password=bcrypt.generate_password_hash('jedi').decode('utf-8'),
            image_file='luke-skywalker.jpg')
    e = User(username="pizzapizza", email="pjane@hotmail.com",
            password=bcrypt.generate_password_hash('pj').decode('utf-8'),
            image_file='ww_nubia.jpg')
    
    db.session.add_all([a, b, c, d, e])
    db.session.commit()
    print('Users 😚')

def load_communities():
    """ Load communities into our database """

    a = Community(user_id=1, community_name="guitar")
    b = Community(user_id=2, community_name="finalfantasy")
    c = Community(user_id=3, community_name="gameofthrones")
    d = Community(user_id=4, community_name="starwars")
    e = Community(user_id=5, community_name="python")
    f = Community(user_id=1, community_name="cplusplus")
    g = Community(user_id=1, community_name="marvel")

    db.session.add_all([a, b, c, d, e, f, g])
    db.session.commit()
    print("Communities 😚")

def load_posts():
    """ Load communities into our database """
    
    a = Post(user_id=1, community_id=1, title="Fender vs Ibanez?",
                body="I'm loving my new Fender Strat. Thoughts on Ibanez?")
    b = Post(user_id=2, community_id=2, title="Looking for group members!",
                body="Hi kedditors, I'm forming a new group, who wants to join?")
    c = Post(user_id=3, community_id=3, title="Season 8 is....",
                body="Excited for the new season, but I don't know what to think anymore.")
    d = Post(user_id=4, community_id=4, title="New Star Wars Actor",
                body="New actor Jane Doe was hired as the new Jedi for the upcoming movie.")
    e = Post(user_id=5, community_id=5, title="Best way to learn Python?",
                body="One great resource is an Software Engineering Fellowing called Hackbright Academy in San Francisco, CA. Any others?")

    db.session.add_all([a, b, c, d, e])
    db.session.commit()
    print("Posts 😚")


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_users()
    load_communities()
    load_posts()
    set_val_user_id()