''' Fonctions pour chaque page web et son URL '''

import time
from flask import render_template, url_for, flash, redirect, request #import toutes les fonctions flask nécessaires
from backend import app, db, bcrypt, mail
from backend.forms import RegistrationForm, LoginForm, UpdateAccountForm, SearchForm, RequestResetForm, ResetPasswordForm
from backend.models import User, Article, ArticleBook
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from backend.recommendation import recommender 


# Page d'accueil
@app.route("/") # URL par défaut
@app.route("/home") 
def home():
    page = request.args.get("page", 1, type=int)
    articles = Article.query.order_by(Article.year.desc()).paginate(page=page, per_page=10) # Afficher 10 articles / page
    
    # Retourner la page web avec la liste des articles 
    return render_template("home.html", posts=articles) 


# Page About
@app.route("/about")
def about():  
    return render_template("about.html", title="About") 


# Page Register pour enregistrer un compte d'utilisateur
@app.route("/register", methods=["GET", "POST"])  
def register():   
    if current_user.is_authenticated:
        return redirect(url_for("home")) # Retourner à la page home

    form = RegistrationForm()
    if form.validate_on_submit(): # Vérifier les informations saisie par l'utilisateur
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8") # Obtenir la version hachée
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user) # Ajouter l'utilisateur a la BD
        db.session.commit()   # Sauvegarder les changements au niveau de la BD
        flash("Your account has been created! You are now able to log in", "success") # Affichier un message
        return redirect(url_for("login")) # retourne la page login
    return render_template("register.html", title="Register", form=form)


# Page Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", title="Login", form=form)


# Page Logout
@app.route("/logout") 
def logout():  
    logout_user() # Déconnecter l'utilisateur
    return redirect(url_for("home")) # Retourner à la page home


# Page Account 
@app.route("/account/<string:username>", methods=["GET", "POST"])  
@login_required
def account(username):
    form = UpdateAccountForm()
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = ArticleBook.query.filter_by(user_id=current_user.id).order_by(ArticleBook.id.desc()).paginate(page=page, per_page=10)
     
    if form.validate_on_submit():  # Pour que l'utilisateur peut modifier son username et l'email 
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()   #sauvegarde les changements
        flash("Your account has been updated!", "success")
        return redirect(url_for("account", username=current_user.username))

    elif request.method == "GET":  # L'utilisateur charge la page
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template("account.html", posts=posts, user=user, form=form, title="Account") 


# Page Description de l'article et qui retourne les recommandations 
@app.route("/post/<post_id>")
def post(post_id): 
    article = Article.query.get_or_404(post_id)

    if current_user.is_authenticated: 
        art = ArticleBook(title=article.title,user_id=current_user.id,post_id=article.id)
        db.session.add(art)
        db.session.commit() 

    # Obtenir l'index des articles similaires
    obj = recommender.Recommender(article.id)
    results = obj.get_similar_articles()
    
    # Récupérer les articles similaires dans la base de données
    related_articles = []
    for i in results:
        tmp = Article.query.filter_by(id=int(i)).first()  # Vérifier si l'article existe 
        related_articles.append(tmp)

    return render_template(
        "post.html",
        title=article.title,
        post=article,
        related_articles=related_articles
    )   


# Page Search
@app.route("/search", methods=["POST"]) 
def search(): 
    form = SearchForm()
    articles = Article.query
    page = request.args.get("page", 1, type=int)

    if form.validate_on_submit:
        post.searched = form.searched.data

        articles = articles.filter(
            Article.title.like("%" + post.searched + "%") # Chercher selon le titre des articles
        )
        articles = articles.order_by(Article.year.desc()).paginate(page=page, per_page=10) # Afficher 10 articles / page

        return render_template(
            "search.html", 
            form=form, 
            searched=post.searched, 
            posts=articles
        ) 


# Envoyer un email pour ré-initialiser le mot de pass 
def send_reset_email(user): 
    # Générer un lien reset_password_link
    token = user.get_reset_token()

    # Le message envoyer a l' utilisateur 
    msg = Message('Password Reset Request',   
                  sender='srcscholar8011@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link: {url_for('reset_token', token=token, _external=True)} 
                If you did not make this request then simply ignore this email and no changes will be made.
                '''
    mail.send(msg)


# Page de la demande de ré-initialisation de mot de pass
@app.route("/reset_password", methods=['GET', 'POST']) 
def reset_request(): 
    if current_user.is_authenticated:
        return redirect(url_for('home'))  # Retourner à la page home

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() # Vérifier si l'email existe 
        send_reset_email(user) # Envoyer um mail à l'utilisateur 
        flash('An email has been sent with instructions to reset your password.', 'info') # Le message à afficher
        return redirect(url_for('login'))  # Ré-orienter vers la page login
    return render_template('reset_request.html', title='Reset Password', form=form) # Charger la page de ré-initialisation de mot de pass


# Page de création de nouveau mot de pass
@app.route("/reset_password/<token>", methods=['GET', 'POST']) 
def reset_token(token): 
    if current_user.is_authenticated:
        return redirect(url_for('home'))   # Réorienter vers la page home

    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning') # Le message à afficher
        return redirect(url_for('reset_request')) # Réorienter vers la page de ré-initialisation de PSW

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()  #sauvegarde les changements
        flash('Your password has been updated! You are now able to log in', 'success') # Le message de success à afficher 
        return redirect(url_for('login')) #réorienter vers la page login
    return render_template('reset_token.html', title='Reset Password', form=form) 
