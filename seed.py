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
    h = Community(user_id=1, community_name="sanfrancisco")

    db.session.add_all([a, b, c, d, e, f, g, h])
    db.session.commit()
    print("Communities 😚")

def load_posts():
    """ Load communities into our database """
    
    a = Post(user_id=1, community_id=1, title="Fender vs Ibanez?",
                body="Lorem ipsum dolor sit amet, consectetur adipiscin elit. Donec a porttitor elit, et scelerisque massa. Sed vitae ligula tempus, facilisis sem eget, suscipit mi. Sed imperdiet tempor volutpat. Aliquam eleifend rutrum sem, vel molestie nulla tincidunt a. Donec cursus id quam sed dictum. Nulla facilisi. Sed vel sem nec ligula ultricies vulputate eget scelerisque turpis. Nam eget sodales ante. Nunc vitae rhoncus odio. Curabitur molestie libero id mauris tempus blandit. Donec aliquam quam vitae gravida hendrerit. In rhoncus a enim id facilisis. Aliquam gravida viverra nulla, eu mollis velit venenatis a.")
    b = Post(user_id=2, community_id=2, title="Greatest Zelda game?",
                body="Phasellus fermentum tellus nunc, in egestas lectus posuere non. Nulla imperdiet arcu sit amet dui euismod vulputate. Fusce non sagittis nisl. Cras sit amet viverra turpis, nec pulvinar diam. Vivamus pharetra porttitor tempor. Morbi quis placerat lectus, sit amet venenatis justo. Integer venenatis quam non sapien sagittis, feugiat ornare libero faucibus. Phasellus porttitor nisl maximus leo vestibulum molestie.")
    c = Post(user_id=3, community_id=3, title="Season 8 has been...",
                body="Vestibulum et ullamcorper ante. Nunc quis metus sem. Etiam vestibulum consectetur semper. Aliquam mattis nulla eros, placerat fermentum neque lobortis et. Aliquam vel lorem dui. Mauris rutrum massa efficitur, interdum ex vitae, viverra enim. Nam et facilisis elit, vitae imperdiet nibh. Proin eleifend dui eget eleifend pellentesque. Nam mattis turpis sed laoreet varius.")
    d = Post(user_id=4, community_id=4, title="The Rise of Skywalker",
                body="Duis mauris urna, rhoncus quis luctus faucibus, porttitor nec diam. Vestibulum porta tincidunt varius. Vestibulum vel orci a libero tristique tempor. Aliquam sit amet justo ipsum. Cras vehicula tincidunt feugiat. Sed eu molestie massa. Nunc interdum neque ac suscipit molestie. Nullam sodales auctor magna ac dignissim. Donec sollicitudin elit a viverra pulvinar. Maecenas dictum tortor sed nunc scelerisque, quis aliquet libero luctus. Ut egestas dictum leo, convallis aliquam erat. Proin quis blandit libero, a rutrum eros. Proin velit ex, sagittis vitae tellus quis, tristique eleifend eros. Duis condimentum blandit orci et tempor. Interdum et malesuada fames ac ante ipsum primis in faucibus.")
    e = Post(user_id=5, community_id=5, title="Best way to learn Python?",
                body="Duis sodales nibh nec erat luctus ullamcorper. Pellentesque vitae purus venenatis, suscipit sapien eget, mattis ante. Sed non tincidunt neque. Aenean at mauris commodo, porttitor magna sed, rutrum odio. Aliquam ornare nibh vitae interdum tristique. Morbi vestibulum id nisi laoreet tincidunt. Sed at rutrum lacus. Vestibulum ultrices lectus orci, vel malesuada arcu vehicula a. Cras mattis, quam sodales fringilla porta, nisi ligula sollicitudin mauris, ac cursus tortor nibh eu nunc.")
    f = Post(user_id=1, community_id=8, title="What if there's snow...",
                body="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam sed varius turpis. Cras placerat ultricies neque, laoreet condimentum nunc viverra nec. Mauris tempus, orci et viverra euismod, metus urna finibus tortor, eget maximus dui odio eget massa. Nulla facilisi. Nam interdum eleifend dui, ac volutpat mauris. Etiam elementum, leo et faucibus dapibus, nulla elit posuere mauris, ut interdum quam quam interdum nulla. Cras vel malesuada magna.")
    g = Post(user_id=2, community_id=8, title="Coding Meet Up",
                body="Duis vitae metus neque. Maecenas eget ex ex. Donec efficitur erat libero, ac luctus mauris consequat in. Cras bibendum ante est, sit amet rhoncus arcu rhoncus ac. Curabitur sollicitudin consequat eros vel cursus. Aliquam nunc mi, maximus id dapibus id, pulvinar nec dolor. ")
    h = Post(user_id=3, community_id=8, title="Pride Parade 2019!",
                body="Curabitur lectus sapien, condimentum euismod fermentum egestas, fermentum et metus. Vestibulum in tempor augue.")
    i = Post(user_id=4, community_id=8, title="Best Local Eats?",
                body="Nullam molestie, risus ut sodales suscipit, risus odio commodo odio, vitae pretium erat tortor nec justo. Integer eget luctus ipsum, sit amet eleifend orci. Praesent sollicitudin sit amet ex sit amet tincidunt. Aenean suscipit lacus nunc, quis interdum erat mattis id. Nullam sit amet nunc velit.")
    j = Post(user_id=5, community_id=8, title="Can tech solve homelessness?",
                body="Donec facilisis massa augue, et rutrum dolor rutrum sit amet. Vestibulum faucibus fermentum tellus, a faucibus lacus ultricies non. Ut a massa at nunc pharetra accumsan. Aliquam erat volutpat. Fusce a est quam. Curabitur condimentum nulla a nulla eleifend dictum. Aenean porta blandit condimentum. Nam in placerat urna. Suspendisse aliquet sagittis arcu, id tincidunt massa scelerisque id. Nunc sapien felis, molestie non lacus in, tempor feugiat tortor. Nullam pulvinar elit id arcu consectetur, in molestie lorem laoreet. Nunc et massa ex. Nulla facilisi.")
    k = Post(user_id=1, community_id=8, title="Photography Spots",
                body=" Donec feugiat finibus dolor, et aliquam ligula pretium ut. Ut varius urna eu purus scelerisque efficitur. Proin malesuada sem quis nisl euismod blandit. Maecenas eget nibh scelerisque nisi egestas pretium. Donec et ultricies turpis, sed finibus massa. Proin at mauris tellus.")
    l = Post(user_id=1, community_id=8, title="Top Tech Companies 2019",
                body="Phasellus scelerisque fermentum turpis, id accumsan ex sagittis vestibulum. Nulla sed ex quis metus scelerisque luctus sed a elit. Pellentesque at dui in urna tempor volutpat. Aenean ornare id purus ut condimentum. Curabitur venenatis tincidunt dictum.")
    m = Post(user_id=3, community_id=8, title="Giants vs Dodgers",
                body="Nulla aliquam ligula ac leo tincidunt mattis. Proin ullamcorper eget urna non semper. Donec purus velit, gravida vel elit a, tincidunt ultricies nulla. Phasellus nec diam malesuada, mattis tortor ut, tempus velit.")
    n = Post(user_id=1, community_id=8, title="A Three-Eyed Raven",
                body="Vivamus cursus, velit vel dignissim pretium, leo orci elementum leo, et hendrerit eros ante non nunc. Phasellus finibus eros eu dapibus varius. Phasellus fringilla purus ut condimentum gravida. Etiam quis sagittis lacus. Praesent cursus ante mauris, et aliquet velit pulvinar sed. Integer pretium blandit justo, id fringilla ex convallis et. Vestibulum feugiat convallis est, quis semper metus fringilla non. Sed sollicitudin tempor dictum. Phasellus in aliquam sem. Nullam dictum et lectus ut dapibus.")
    o = Post(user_id=2, community_id=8, title="Hackbright, thoughts?",
                body="Donec purus velit, gravida vel elit a, tincidunt ultricies nulla. Phasellus nec diam malesuada, mattis tortor ut, tempus velit. Proin euismod leo eu euismod volutpat. Aenean rutrum velit nunc, sit amet dictum diam pellentesque eu. Curabitur in lacus urna. Nam vitae magna sapien. Suspendisse luctus vestibulum nisi sit amet imperdiet. In condimentum dignissim ex, sollicitudin pretium enim ultricies ac. Praesent ut suscipit tortor.")
    p = Post(user_id=3, community_id=8, title="So I saw a coyote and...",
                body="Vivamus cursus, velit vel dignissim pretium, leo orci elementum leo, et hendrerit eros ante non nunc. Phasellus finibus eros eu dapibus varius. Phasellus fringilla purus ut condimentum gravida. Etiam quis sagittis lacus.")
    q = Post(user_id=4, community_id=8, title="Apartment View",
                body="Praesent cursus ante mauris, et aliquet velit pulvinar sed. Integer pretium blandit justo, id fringilla ex convallis et. ")
    r = Post(user_id=5, community_id=8, title="Warriors vs Lakers",
                body="Vestibulum feugiat convallis est, quis semper metus fringilla non. Sed sollicitudin tempor dictum. Phasellus in aliquam sem. Nullam dictum et lectus ut dapibus.")
    s = Post(user_id=1, community_id=8, title="Can anyone read Lorem Ipsum?",
                body="Ut faucibus, elit ut iaculis interdum, metus felis tristique justo, vel sagittis tortor eros ac ante. Aliquam tempus porttitor vulputate. Proin sed justo non elit dignissim consectetur. Mauris commodo turpis eget elit facilisis eleifend. Sed tristique leo ut nisl rhoncus, vitae mollis neque lacinia. Interdum et malesuada fames ac ante ipsum primis in faucibus. In non nulla quis nisl rutrum fringilla.")
    t = Post(user_id=1, community_id=8, title="Ipsum Lorem",
                body="Vestibulum lorem ligula, commodo vitae magna nec, dictum dignissim felis. Donec a lacus nisl. Nam molestie euismod luctus. Cras mi purus, consequat aliquet laoreet id, sodales vel odio.")
    u = Post(user_id=1, community_id=8, title="I did it!",
                body="Vestibulum sit amet aliquet risus. Nullam eu fringilla nisi. Phasellus eget ornare neque. Mauris placerat turpis fringilla, congue ligula et, rhoncus eros. Sed id ultrices est, non dapibus sem. Vivamus congue placerat sem. Nunc ut quam ornare, lacinia tortor id, condimentum mi. Pellentesque congue enim eu fermentum interdum.")


    db.session.add_all([a, b, c, d, e, f, g, h, i , j, k, l, m, n, o, p, q, r, s, t, u])
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
    m = Comment(user_id=1, post_id=6, body="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi lobortis venenatis velit et condimentum. In hac habitasse platea dictumst. Phasellus eget finibus purus, ac dictum augue. Phasellus ultricies augue quis quam condimentum auctor. Praesent posuere lorem ut augue egestas tristique. Nam ac libero mi. Suspendisse potenti. Donec eleifend fermentum efficitur. Aliquam venenatis tincidunt ultrices.")
    n = Comment(user_id=2, post_id=6, body="Sed suscipit ex neque, sed consectetur justo fermentum dictum.")
    o = Comment(user_id=3, post_id=6, body="In magna ex, consequat at ipsum quis, ullamcorper dictum urna. Phasellus et suscipit elit, tincidunt pretium ex. Fusce non aliquet dui.")
    p = Comment(user_id=4, post_id=7, body="Nullam a enim commodo, eleifend ante eget, elementum tortor. Praesent posuere nunc nunc, eu egestas tortor porta vel. Mauris iaculis auctor orci.")
    q = Comment(user_id=5, post_id=7, body="Phasellus mi libero, egestas in ipsum ut, iaculis tempus velit. Vivamus quis ex convallis, condimentum leo a, volutpat orci.")
    r = Comment(user_id=1, post_id=7, body="Curabitur fringilla enim sed sollicitudin semper. Maecenas ac sodales ante. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.")
    s = Comment(user_id=1, post_id=8, body="Donec finibus vel neque in consequat. Etiam sit amet lacinia turpis. Donec mollis quam nibh, at feugiat sem faucibus ac.")
    t = Comment(user_id=1, post_id=8, body="Aliquam erat volutpat. Vestibulum sagittis quis sem quis lobortis. Vestibulum rhoncus magna tortor. Sed euismod nisi mauris, sit amet cursus lorem facilisis nec. Cras dui nisi, laoreet et commodo non, consectetur in magna.")
    u = Comment(user_id=2, post_id=9, body="Donec nulla orci, bibendum quis massa eget, maximus condimentum nunc. Curabitur cursus metus non sapien pretium ullamcorper.")
    v = Comment(user_id=3, post_id=9, body="Morbi iaculis ullamcorper luctus. Donec odio mi, pellentesque non laoreet eget, mattis sed orci. Integer diam turpis, lobortis eu elit vestibulum, congue aliquam metus. Ut egestas, leo in dapibus bibendum, enim lacus interdum tellus, facilisis porta mauris tortor sed nibh. In hac habitasse platea dictumst.")
    w = Comment(user_id=4, post_id=7, body="Quisque magna libero, pretium sit amet consectetur vel, egestas non nulla. Nullam at sodales velit. Nam maximus magna et turpis faucibus iaculis.")
    x = Comment(user_id=5, post_id=6, body="Duis fermentum quam sed augue varius vehicula. Fusce molestie molestie magna quis tincidunt. Nullam fringilla laoreet sapien ut auctor. Donec malesuada vel augue eleifend molestie. ")
    y = Comment(user_id=1, post_id=6, body="Curabitur sodales turpis in tempus malesuada. Aenean non dolor venenatis, consectetur leo et, vehicula nunc. Donec malesuada sodales ex vel sollicitudin.")
    z = Comment(user_id=1, post_id=9, body="Phasellus facilisis pretium enim, vitae porttitor tortor dapibus vel.")
    aa = Comment(user_id=1, post_id=9, body="Sed augue lacus, luctus a turpis eget, convallis efficitur quam.")
    bb = Comment(user_id=1, post_id=6, body="Donec nulla est, fringilla nec elit in, egestas laoreet quam. Integer pretium nulla ac convallis rhoncus. In tempor ut tellus id posuere. In id blandit felis.")
    db.session.add_all([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z, aa, bb])
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