"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

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
