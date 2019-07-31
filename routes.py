from flask import render_template, redirect, url_for
from nzalawgroupapp import app 
from nzalawgroupapp.forms import SignupForm, LoginForm, RegisterForm, ReviewForm, ContactForm

from nzalawgroupapp.models import db, User 

from flask_login import login_user, current_user, logout_user, login_required

from nzalawgroupapp.models import User, check_password_hash 


@app.route('/')
def hello_world():
    return render_template("home.html")

@app.route('/register', methods = ["GET", "POST"])
def createUser():
    form = SignUpForm()
    if form.validate_on_submit():
        print("The user is {}".format(form.username.data))
        user = User(form.username.data, form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    else:
        print("Form not valid") 


@app.route("/login", methods =["GET", "POST"])
def login():
    form = LoginForm()
    user_email = form.email.data 
    password = form.password.data 
    user = User.query.filter(User.email == form.email.data).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        print(current_user.username)
        return redirect(url_for('hello_world'))
    print(form.email.data, form.password.data)
    return render_template("login.html", form=form)


@app.route("/review", methods = ["GET", "POST"])
@login_required
def post():
    form = ReviewForm()
    title = form.title.data
    content = form.content.data
    user_id = current_user.id 
    review = Review(title = title, content = content, user_id = user_id)
    db.session.add(review)
    db.session.commit()

    return render_template("contact.html", form =form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('hello_world'))

@app.route("/post/<id>")
def post_detail(id):
    test_id = id 
    if current_user.is_authenticated:
        print("User can see this stuff")
        post = Post.query.get(id)

