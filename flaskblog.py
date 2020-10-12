from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy 
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '5e5b968d2e77c6d37d2b17ee2bc819de' # secret key variable for secure staying logged in
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'

#by adding /// wee giving the relative path, so the site.db should created in this file directory where we are doing our project

db = SQLAlchemy(app) # we need to create a datbase instance


# !! AFTER THE DB.MODELS ARE CREATED WE GO TO THE PYTHON3 CONSOLE AND ACTUALLY CREATE THE DATABASE WITH OUR MODELS !! 

class User(db.Model): # Integer is a type of the id
    id=db.Column(db.Integer, primary_key = True)
    # nullable = False - means this argument should exist (should be filled in)
    username = db.Column(db.String(20), unique=True, nullable=False) # in the validation the max length is 20 characters, it should be unique, we have to have a username so it could not be null 
    email = db.Column(db.String(120), unique=True, nullable=False) 
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg") # profile pic with a default pic if not given
    password = db.Column(db.String(60), nullable=False) # those will be hashed (encoded) 60 characters long 
    posts = db.relationship('Post', backref='author', lazy=True) # the posts attribute has a relationship to the "Post Model", backref='author' means adding another column to the Post model,
    # ! so when we have a post we can simply use this author attribute to get the user who created the post. 
    # the lazy arg justifies when sqlalchemy loads the data from the db, true means the sql alchemy will load the data as necessary in one go -
    # this is convenient cuz with this relationship we will be able to simply use this post attribute to get all of the posts created by an individual user
    # we made "posts" as a relationship not the column 
    # so that when we look at rhe database structure (with an sql client) we would not see this relationship - 
    # it will be an additional quarry at the background that will get all the posts that the user got created

    # the method does - how the object (user model) is printed whenever we print it out
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


# create a post class to hold our posts
class Post(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    # The type of this column should be "db.DateTime" and we need to create a default argument 
    # if there is no time filled in, 
    # so we need to import daytime class from flask and utcnow specific to show the time it was posted (time right now )
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow) #to hold the date when the post was made 
    content = db.Column(db.Text, nullable=False) # the content 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # id of the user who has posted the post. db.ForeignKey('user.id') specifies that the key has a relationship with the user model

    # what will be shown:
    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted}')"

# ! we also need to keep in mind that the relationship between the post and user models are "one to many",
# since the users will be the authors of the posts. So one user can have many posts and the post can have only one author - user  
# that is why we need to create an attribute in our user model and set it to db.relationship: posts = db.relationship('Post', backref='author', lazy=True)



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



# allows us to run the script using "python3 flaskblog.py" command, but we can use also "flask run"
if __name__ == '__main__': 
    app.run(debug=True)

