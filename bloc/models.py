
from datetime import datetime
from bloc import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'


    id_user = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),  nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Post(db.Model):
     
    __tablename__ = 'article8'


    abstract = db.Column(db.Text, nullable=False)
    authors = db.Column(db.Text(100), nullable=False)
    id = db.Column(db.Text(50),primary_key=True )
    n_citation = db.Column(db.Integer, nullable=False)
    references = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    venue = db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.year}')"
