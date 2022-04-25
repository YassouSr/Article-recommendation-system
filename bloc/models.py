from datetime import datetime
from bloc import db, login_manager
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


class Post(db.Model):

    __tablename__ = "aminer"

    abstract = db.Column(db.Text, nullable=False)
    authors = db.Column(ARRAY(db.String()))
    id = db.Column(db.String(), primary_key=True, nullable=False)
    n_citation = db.Column(db.Integer)
    references = db.Column(ARRAY(db.String()))
    title = db.Column(db.String(), nullable=False)
    venue = db.Column(db.String())
    year = db.Column(db.Integer)

    def __repr__(self):
        return f"Post('{self.title}', '{self.year}')"
