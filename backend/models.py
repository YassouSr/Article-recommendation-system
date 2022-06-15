''' Configuration des tables de la base de données '''

from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer
from backend import db, login_manager,app
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import ARRAY  #import database


# Créer un objet de connexion à la base de données
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    # Postgresql n'autorise pas les noms de table "user".
    __tablename__ = "admin" 

    # id type is serial on postgre
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('ArticleBook', backref='author', cascade="all, delete", lazy='dynamic')

    def get_reset_token(self):
        s = Serializer(app.config['SECRET_KEY'],)
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token, expires_sec)['user_id']
        except:  
            return None
        return User.query.get(user_id)
        
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    def get_id(self):
        return self.id


class Article(db.Model):

    __tablename__ = "article"
      
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    link = db.Column(db.Text)
    authors = db.Column(db.Text)
    references = db.Column(ARRAY(db.Integer))
    year = db.Column(db.Integer)
    #Comment notre objet est imprimé
    def __repr__(self):
        return f"Article('{self.id}', '{self.title}')"


class ArticleBook(db.Model):

    __tablename__ = "articlebook"
      
      #Ajouter des colonnes pour la table
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text)
    date_seen = db.Column(db.TIMESTAMP, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    
    def __repr__(self):
        return f"Articlebook('{self.id}', '{self.title}', '{self.date_seen}')"
    
    def get_id(self):
        return self.id