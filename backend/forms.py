''' Formulaires de site '''

from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from backend.models import User


# Formulaire de création d'un compte d'utilisateur sur la page Register
class RegistrationForm(FlaskForm):  
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):  # Validation d'username 
        user = User.query.filter_by(username=username.data).first() # Vérifier si l'utilisateur existe
        if user:
            raise ValidationError("That username is taken. Please choose a different one.")  # Afficher un message d'erreur

    def validate_email(self, email): # Validation d'email
        user = User.query.filter_by(email=email.data).first() # Vérifier si l'email existe
        if user:
            raise ValidationError("That email is taken. Please choose a different one.") # Afficher un message d'erreur


# Formulaire de login
class LoginForm(FlaskForm): 
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


# Formulaire de mis à jour du compte d'utilisateur
class UpdateAccountForm(FlaskForm):  
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", validators=[DataRequired(), Email()])

    submit = SubmitField("Update")

    def validate_username(self, username): # Validation d'username 
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first() # Vérifier si l'utilisateur existe
            if user:
                raise ValidationError("That username is taken. Please choose a different one.")

    def validate_email(self, email):    # Validation d'email
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()   # Vérifier si l'email existe
            if user:
                raise ValidationError("That email is taken. Please choose a different one.")


# Barre de recherche
class SearchForm(FlaskForm):   
    searched = StringField("Searched", validators=[DataRequired()])
    submit = SubmitField("Search")


# Formulaire d'envoie l'email de ré-initialisation de PSW
class RequestResetForm(FlaskForm):  
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()  # Vérifier si l'email existe
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


# Formulaire de ré-initialisation de PSW
class ResetPasswordForm(FlaskForm):   # creation de la classe de réinitialisation de PSW
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
