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
    print("Users")

    a = User(username="kumy", email="sunnywithclouds@gmail.com",
            password=bcrypt.generate_password_hash('12').decode('utf-8'))
    b = User(username="ropers", email="triddle26@gmail.com",
            password=bcrypt.generate_password_hash('ou812').decode('utf-8'))
    c = User(username="kbr22", email="kbrballer22@msn.com",
            password=bcrypt.generate_password_hash('kbr').decode('utf-8'))
    d = User(username="jedimaster2019", email="jedimaster19@icloud.com",
            password=bcrypt.generate_password_hash('jedi').decode('utf-8'))
    e = User(username="pizzapizza", email="pizzajane@hotmail.com",
            password=bcrypt.generate_password_hash('pj').decode('utf-8'))
    
    db.session.add_all([a, b, c, d, e])
    db.session.commit()

# def load_communities():
#     """ Load communities into our database """
#     print("communitites")
#     a = Community()


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
    # load_movies()
    # load_ratings()
    set_val_user_id()