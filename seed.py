from models import Users, Posts, Tags, PostTags, db
from app import app

with app.app_context():
    db.drop_all()
    db.create_all()

    Users.query.delete()

    user_1 = Users(first_name='John', last_name='Egbert', image_url='https://i.redd.it/twdd6jj3eis41.gif')
    user_2 = Users(first_name='Rose', last_name='Lalonde')

    db.session.add(user_1)
    db.session.add(user_2)
    
    db.session.commit()



    Posts.query.delete()

    post_1 = Posts(title='man, little monsters is SUCH a good movie!!!', content='i got a little monsters poster, it\'s so awesome. i''m going to watch it again today, the applejuice scene was so funny.', user_id=user_1.id)
    post_2 = Posts(title='Title text', content='Lorem Ipsum', user_id=user_1.id)
    post_3 = Posts(title='rose post', content='ross lanlone', user_id=user_2.id)

    db.session.add(post_1)
    db.session.add(post_2)
    db.session.add(post_3)

    db.session.commit()



    Tags.query.delete()
    PostTags.query.delete()

    tag_1 = Tags(name='movie')
    tag_2 = Tags(name='test')

    #assign tags to posts
    tag_1.posts.append(post_1)
    tag_1.posts.append(post_2)
    tag_2.posts.append(post_1)
    tag_2.posts.append(post_2)
    tag_2.posts.append(post_3)

    db.session.add(tag_1)
    db.session.add(tag_2)

    db.session.commit()

    #print(tag_1.posts)
    #print(post_1.tags)