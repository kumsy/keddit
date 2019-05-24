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
    b = User(username="kmasterc", email="kc@msn.com",
            password=bcrypt.generate_password_hash('23').decode('utf-8'),
            image_file='eevee.gif')
    c = User(username="kbr22", email="kbr@msn.com",
            password=bcrypt.generate_password_hash('kbr').decode('utf-8'),
            image_file='rex.jpg')
    d = User(username="lukeskywalker", email="jedi@icloud.com",
            password=bcrypt.generate_password_hash('jedi').decode('utf-8'),
            image_file='luke-skywalker.jpg')
    e = User(username="yoshi", email="yoshi@nintendo.com",
            password=bcrypt.generate_password_hash('n64').decode('utf-8'),
            image_file='yoshi.png')
    
    db.session.add_all([a, b, c, d, e])
    db.session.commit()
    print('Users 😚')

def load_communities():
    """ Load communities into our database """

    a = Community(user_id=1, community_name="guitar")
    b = Community(user_id=2, community_name="nintendo")
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
                body="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec a porttitor elit, et scelerisque massa. Sed vitae ligula tempus, facilisis sem eget, suscipit mi. Sed imperdiet tempor volutpat. Aliquam eleifend rutrum sem, vel molestie nulla tincidunt a. Donec cursus id quam sed dictum. Nulla facilisi. Sed vel sem nec ligula ultricies vulputate eget scelerisque turpis. Nam eget sodales ante. Nunc vitae rhoncus odio. Curabitur molestie libero id mauris tempus blandit. Donec aliquam quam vitae gravida hendrerit. In rhoncus a enim id facilisis. Aliquam gravida viverra nulla, eu mollis velit venenatis a.")
    b = Post(user_id=2, community_id=2, title="Greatest Zelda game?",
                body="Phasellus fermentum tellus nunc, in egestas lectus posuere non. Nulla imperdiet arcu sit amet dui euismod vulputate. Fusce non sagittis nisl. Cras sit amet viverra turpis, nec pulvinar diam. Vivamus pharetra porttitor tempor. Morbi quis placerat lectus, sit amet venenatis justo. Integer venenatis quam non sapien sagittis, feugiat ornare libero faucibus. Phasellus porttitor nisl maximus leo vestibulum molestie.")
    c = Post(user_id=3, community_id=3, title="Season 8 has been...",
                body="Vestibulum et ullamcorper ante. Nunc quis metus sem. Etiam vestibulum consectetur semper. Aliquam mattis nulla eros, placerat fermentum neque lobortis et. Aliquam vel lorem dui. Mauris rutrum massa efficitur, interdum ex vitae, viverra enim. Nam et facilisis elit, vitae imperdiet nibh. Proin eleifend dui eget eleifend pellentesque. Nam mattis turpis sed laoreet varius.")
    d = Post(user_id=4, community_id=4, title="The Rise of Skywalker",
                body="Duis mauris urna, rhoncus quis luctus faucibus, porttitor nec diam. Vestibulum porta tincidunt varius. Vestibulum vel orci a libero tristique tempor. Aliquam sit amet justo ipsum. Cras vehicula tincidunt feugiat. Sed eu molestie massa. Nunc interdum neque ac suscipit molestie. Nullam sodales auctor magna ac dignissim. Donec sollicitudin elit a viverra pulvinar. Maecenas dictum tortor sed nunc scelerisque, quis aliquet libero luctus. Ut egestas dictum leo, convallis aliquam erat. Proin quis blandit libero, a rutrum eros. Proin velit ex, sagittis vitae tellus quis, tristique eleifend eros. Duis condimentum blandit orci et tempor. Interdum et malesuada fames ac ante ipsum primis in faucibus.")
    e = Post(user_id=5, community_id=5, title="Best way to learn Python?",
                body="Duis sodales nibh nec erat luctus ullamcorper. Pellentesque vitae purus venenatis, suscipit sapien eget, mattis ante. Sed non tincidunt neque. Aenean at mauris commodo, porttitor magna sed, rutrum odio. Aliquam ornare nibh vitae interdum tristique. Morbi vestibulum id nisi laoreet tincidunt. Sed at rutrum lacus. Vestibulum ultrices lectus orci, vel malesuada arcu vehicula a. Cras mattis, quam sodales fringilla porta, nisi ligula sollicitudin mauris, ac cursus tortor nibh eu nunc.")

    db.session.add_all([a, b, c, d, e])
    db.session.commit()
    print("Posts 😚")

def load_comments():
    """ Load comments into our database """

    a = Comment(user_id=1, post_id=2, body="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin magna risus, accumsan vitae tellus vel, dignissim posuere turpis. Ut a consectetur elit. Aenean venenatis placerat metus faucibus aliquam. In rhoncus accumsan imperdiet. Nunc rhoncus ante massa, ac imperdiet magna rutrum id. Cras vel diam purus.")
    b = Comment(user_id=1, post_id=3, body="Praesent metus nisi, ullamcorper eu dolor quis, viverra cursus odio. Phasellus id purus sed enim aliquet consequat. Nam sagittis luctus ullamcorper. Donec imperdiet metus nec nunc mollis vehicula. Nunc ex justo, sodales in cursus eu, commodo non metus. ")
    c = Comment(user_id=2, post_id=1, body="Integer efficitur dui vel faucibus vulputate.")
    d = Comment(user_id=2, post_id=3, body="Maecenas vel velit malesuada, pellentesque augue ac, porttitor ligula. Suspendisse dolor enim, feugiat ut dignissim eget, lobortis quis augue. Mauris porttitor interdum blandit. Duis dignissim vitae justo sed posuere. Duis blandit dui turpis, a suscipit diam dictum et. Integer eu lorem in tortor ullamcorper consequat. Aliquam placerat felis a tempus sollicitudin. Nam tempor nunc gravida magna faucibus varius.")
    e = Comment(user_id=3, post_id=1, body="In vel pretium sem. Fusce ac urna ornare, viverra tellus ac, tempor nunc. Maecenas pellentesque sem ullamcorper dapibus accumsan. Ut ornare metus vitae viverra ornare.")
    f = Comment(user_id=3, post_id=4, body="Nulla facilisi. Aliquam gravida aliquam elit a ultricies. Curabitur mattis ligula eu eros faucibus auctor. Pellentesque at aliquet lacus. Proin sodales, ex laoreet tristique dapibus, orci quam fringilla sem, vitae pretium eros dui non lectus. Aliquam sodales ligula vitae ipsum ultrices porttitor. Donec lacus sem, placerat ac libero in, commodo ultrices arcu. Nunc fringilla velit urna, eu vehicula purus tincidunt id. Integer malesuada laoreet tristique.")
    g = Comment(user_id=4, post_id=2, body="Nunc aliquet sapien id mi fermentum, vel tempor erat efficitur. Curabitur ornare sem sapien, non laoreet velit egestas quis. Praesent mollis mauris ut orci eleifend pretium.")
    h = Comment(user_id=4, post_id=5, body=" Nunc ut est malesuada lacus vestibulum ullamcorper vel non justo. Aliquam enim quam, posuere id sapien sed, semper auctor nunc. Etiam venenatis arcu quis aliquam congue. Duis ut pharetra mi.")
    i = Comment(user_id=5, post_id=1, body="Sed ornare justo non nibh varius pellentesque.")
    j = Comment(user_id=5, post_id=5, body="Vestibulum ut commodo ex. Mauris nec posuere mauris, vel sollicitudin nisi. In non vestibulum mauris. Donec non condimentum dolor. Aliquam eleifend eros maximus elit laoreet, eget hendrerit lectus aliquam. Sed convallis tellus et tortor pretium, at ultricies enim faucibus. Aenean at elit diam. Vestibulum aliquam sapien a hendrerit consequat.")
    k = Comment(user_id=1, post_id=4, body="Proin egestas sodales eros sit amet imperdiet.")
    l = Comment(user_id=1, post_id=5, body="Aenean suscipit justo lectus, at sollicitudin turpis vestibulum semper. Nam in sagittis ante. Curabitur maximus, leo ac molestie congue, augue ipsum vulputate sem, et tincidunt tortor felis nec purus. Nam tempor eget neque non laoreet. Proin eget sapien at quam interdum pretium in non dui.")

    db.session.add_all([a, b, c, d, e, f, g, h, i, j, k, l])
    db.session.commit()
    print("Comments 😚")


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
    load_comments()
    set_val_user_id()