"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class Users(db.Model):
    """A user."""

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   nullable=False)
    
    first_name = db.Column(db.String(32),
                           nullable=False)

    last_name = db.Column(db.String(32),
                          nullable=False)

    image_url = db.Column(db.Text,
                          default='https://upload.wikimedia.org/wikipedia/commons/thumb/d/d9/Icon-round-Question_mark.svg/200px-Icon-round-Question_mark.svg.png?20120912110201')

class Posts(db.Model):
    """A table for blog posts."""

    __tablename__ = 'posts'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True,
                   nullable=False)
    
    title = db.Column(db.String(50))

    content = db.Column(db.Text,
                        nullable=False,
                        default='Lorem Ipsum')
    
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.now())
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    author = db.relationship('Users', backref='posts', cascade="all,delete")


class Tags(db.Model):
    """Tags for posts"""

    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    
    name = db.Column(db.String(30),
                     unique=True,
                     nullable=False)
    
    posts = db.relationship('Posts', secondary='post_tags', backref='tags', cascade="all,delete")


class PostTags(db.Model):
    """Posts that are associated with tags and vice-versa."""

    __tablename__ = 'post_tags'

    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)

