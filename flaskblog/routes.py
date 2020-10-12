from flask import render_template, url_for, flash, redirect
from flaskblog import app
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post


# !! AFTER THE DB.MODELS ARE CREATED WE GO TO THE PYTHON3 CONSOLE AND ACTUALLY CREATE THE DATABASE WITH OUR MODELS !! 


posts = [
    {
        'author': 'corey schafer',
        'title': 'blog post 1',
        'content': 'First post content',
        'date_posted': 'april 20, 2002'
    },

    {
        'author': 'alex mitu',
        'title': 'blog post 2',
        'content': 'second post content',
        'date_posted': 'april 23, 2012'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html")

#  methods =['GET', 'POST'] list of allowed methods when we press sign up button 
@app.route("/register", methods =['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # creating the message for successfull sign up with the flash message
        flash(f'Account created for {form.username.data}!', 'success') # with the help of format methode (f string) - f'text text {form.username.data}!' we can use placeholder inside of a text
        return redirect(url_for('home')) # so after the form is sended we redirect the user at the home function -> @app.route("/home") def home(): return render_template("home.html", posts = posts) 
    return render_template('register.html', title = 'Register', form = form)


@app.route("/login", methods =['GET', 'POST'])
def login():
    form = LoginForm()
    #  creating some dummy data to check the login form 
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "password":
            flash("You have been logged in !", "success")
            return redirect(url_for('home'))
        else:
            flash("login unsuccessful. Pls check ur username and password", "danger")
    return render_template('login.html', title = 'Login', form = form)
