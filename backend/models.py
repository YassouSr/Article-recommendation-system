from datetime import datetime
from backend import db, login_manager
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import ARRAY


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Article(db.Model):

    __tablename__ = "article"

    index = db.Column(db.Integer)
    id = db.Column(db.Text, primary_key=True)
    title = db.Column(db.Text)
    abstract = db.Column(db.Text)
    authors = db.Column(ARRAY(db.Text))
    n_citation = db.Column(db.Integer)
    references = db.Column(ARRAY(db.Text))
    venue = db.Column(db.Text)
    year = db.Column(db.Integer)

    def __repr__(self):
        return f"Article('{self.id}', '{self.title}')"
