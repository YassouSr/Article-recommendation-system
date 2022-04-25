from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
username = "postgres"
port = "5432"
db_name = "recommendation"
db_password = "amina"
secret_key = "1478df-dfsefdfs-dsfeffdf"

app.config["SECRET_KEY"] = secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://{}:{}@localhost:{}/{}".format(
    username, db_password, port, db_name
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

# don't delete this line otherwise it won't run the application
# because import statements are causing cyclic import (loop) and this line stops it
from bloc import routes
