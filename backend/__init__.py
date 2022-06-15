#importation des bibliothèques
import os   # pour manipuler des chemins
from flask import Flask #import toutes les fonctions flask nécessaires
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import secrets

#Création d'un site web
app = Flask(__name__, template_folder='template') #configuration de flask
username = "postgres" #nom de compte
port = "5432"    #num de port de compte
db_name = "recommendationV2"  #nom de la BDD
db_password = "amina" #PSW de compte
# Pour générer une nouvelle clé secrète qui permet de générer toutes les données chiffrées comme (session, cookies)
app.config["SECRET_KEY"] = secrets.token_hex(16)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://{}:{}@localhost:{}/{}".format( #adresse de l'hôte de la base de données
    username, db_password, port, db_name
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # désactiver le système de suivi des modifications.
#création d'une instance de la base de données
db = SQLAlchemy(app)
bcrypt = Bcrypt(app) 
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"


#Configuration du courrier
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  #utiliser gmail
app.config['MAIL_PORT'] = 465 #mail port
app.config['MAIL_USE_SSL'] = True #type de sécurité
app.config['MAIL_USERNAME'] = 'srcscholar8011@gmail.com' #mail utilisé 
app.config['MAIL_PASSWORD'] = 'blvqvcxwgpyorhgs'  #MDP utilisé pour l'application donnée par Google 
mail = Mail(app) #include système de mailing

# Nécessaire pour les importations circulaires
from backend import views
