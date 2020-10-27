from flask import render_template, url_for, flash, redirect, request # "request" needed so we can use query parameters for login route 
from flaskblog import app, db, bcrypt # we import "db" and "bcrypt" for the register route
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required # imports that class so we can check the user email and password validation with the db data


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

@app.route("/register", methods =['GET', 'POST'])
def register():
    if current_user.is_authenticated: # current user check, so when we try to log in and we are already logged in
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # so if the form valid to submit (all length and signs are correct) we can hash the password and do the authentication procedure 
        hashed_pasword = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # "form.password.data" is the password that user has entered and ".decode('utf-8')" is needed to decde from bytes to a regular string
        user = User(username = form.username.data, email = form.email.data, password = hashed_pasword) # getting the data from user into the db, where we get allready hashed password with "password = hashed_pasword"
        # saving the entered data to the db
        db.session.add(user)
        db.session.commit()
        # creating the message for successfull sign up with the flash message
        flash(f'Your account has been created ! You are now able to log in', 'success') # with the help of format methode (f string) - f'text text {form.username.data}!' we can use placeholder inside of a text
        return redirect(url_for('login')) # so after the form is sended we redirect the user at the login form
    return render_template('register.html', title = 'Register', form = form)


@app.route("/login", methods =['GET', 'POST'])
def login():
    if current_user.is_authenticated: # current user check
        return redirect(url_for('home'))
    form = LoginForm()
    #  creating some dummy data to check the login form 
    if form.validate_on_submit():
        # before we were simply checking the hardcoded data, and now we need to check the database for valid data 
        # firstly the user will be logged in with an email, so we need to write a check for the email in the db:
        user = User.query.filter_by(email = form.email.data).first() # finds user with the submitted email
        if user and bcrypt.check_password_hash(user.password, form.password.data): # so if the user exist and the password, the user entered, is valid, we want to login the user and we also need to import the login user function 
            login_user(user, remember = form.remember.data) # "user" - what we want to login, "remember" - remember me form (boolean) we have created
            next_page = request.args.get('next') # this line will get the "next" parameter (from url line)
            return redirect(next_page) if next_page else redirect(url_for('home')) # use of ternary conditional. redirect to "next_page" if next_page exists, when non, then return to homepage
        else:
            flash("login unsuccessful. Pls check ur email  and password", "danger")
    return render_template('login.html', title = 'Login', form = form)


# logout route we need when we log out, will redirect to home page
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

# the account route will be "seen" when the user is logged in and can access it's account -> account template
@app.route("/account")
@login_required # "login_required" decorator is extention tht knows that we need to be logged in to access this route, so it prevent showing user account information for non logged users (if they try to access from url)
def account():
    return render_template('account.html', title = 'Account')