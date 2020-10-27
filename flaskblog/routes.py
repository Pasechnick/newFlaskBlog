from flask import render_template, url_for, flash, redirect
from flaskblog import app
# we import RegistrationForm, LoginForm classes from "forms", so we can use it within registration route, login route. 
# so we can make an instance inside of "register" and "login" routes
# in register route: form = RegistrationForm(), in login route: form = LoginForm() 
# and then using those instances we access formfields like username, email and ect. inside of "forms.py" file, so that those fields can be used by "register.html" and "login.html"
from flaskblog.forms import RegistrationForm, LoginForm 
from flaskblog.models import User, Post


# !! AFTER THE DB.MODELS ARE CREATED WE GO TO THE PYTHON3 CONSOLE AND ACTUALLY CREATE THE DATABASE WITH OUR MODELS !! 


posts = [  # just by adding this data to the return statement of the route function, we can get the data in our templates 
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
def home():                           # posts-variable will be equal posts-data
    return render_template("home.html", posts=posts) # we add posts as argument, so we can access "posts" in home template 

@app.route("/about")
def about():
    return render_template("about.html")

# methods =['GET', 'POST'] we should include them so those methods are allowed when we press sign up button 
@app.route("/register", methods =['GET', 'POST'])
def register():
    form = RegistrationForm() # after we create the route and the function we also need to create an instance of the form that we will send to the application
    # so basically after we create the instance of that form, we can paste it as argument in return statement so we can access it from our registration template 
    if form.validate_on_submit(): # this will tell us if our form was validated when submitted
        # creating the message for successfull sign up with the flash message (since the data was validated)
        flash(f'Account created for {form.username.data}!', 'success') # with the help of format methode (f string) - f'text text {form.username.data}!' we can use placeholder {form.username.data} inside of a text
        return redirect(url_for('home')) # so after the form is sended we redirect the user at the home function -> @app.route("/home") def home(): return render_template("home.html", posts = posts) 
    return render_template('register.html', title = 'Register', form = form) # after the instance of the form is created we can paste "form"-instance into the template as argument "form"


# same here: we create the route, the function, then we make instance of the login form, so we can access it from the login template
@app.route("/login", methods =['GET', 'POST'])
def login():
    form = LoginForm()
    #  creating some dummy data to check the login form. Just a simulation
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "password":
            flash("You have been logged in !", "success")
            return redirect(url_for('home'))
        else:
            flash("login unsuccessful. Pls check ur username and password", "danger")
    return render_template('login.html', title = 'Login', form = form)
