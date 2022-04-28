from flask import render_template, url_for, flash, redirect, request
from backend import app, db, bcrypt
from backend.forms import RegistrationForm, LoginForm, UpdateAccountForm, SearchForm
from backend.models import User, Article
from flask_login import login_user, current_user, logout_user, login_required
from backend.recommendation import recommender


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get("page", 1, type=int)
    articles = Article.query.order_by(Article.year.desc()).paginate(page=page, per_page=10)
    return render_template("home.html", posts=articles)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


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


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template("account.html", title="Account", form=form)


@app.route("/post/<post_id>")
def post(post_id):
    article = Article.query.get_or_404(post_id)

    # get index of similar articles
    obj = recommender.Recommender(article.id)
    results = obj.get_similar_articles()

    # fetch similar articles from database
    related_articles = []
    for i in results:
        tmp = Article.query.filter_by(id=int(i)).first()
        related_articles.append(tmp)

    return render_template(
        "post.html",
        title=article.title,
        post=article,
        related_articles=related_articles
    )


# Search
@app.route("/search", methods=["POST"])
def search():
    form = SearchForm()
    articles = Article.query
    page = request.args.get("page", 1, type=int)

    if form.validate_on_submit:
        post.searched = form.searched.data

        articles = articles.filter(
            Article.title.like("%" + post.searched + "%")
        )
        articles = articles.order_by(Article.year.desc()).paginate(page=page, per_page=10)

        return render_template(
            "search.html", 
            form=form, 
            searched=post.searched, 
            posts=articles
        )
