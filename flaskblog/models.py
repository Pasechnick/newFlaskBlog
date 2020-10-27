
from datetime import datetime
from flaskblog import db # python knows that initialized "db" should be in "__init__.py" file, so we do not need specify the location (just the name of the our app "flaskblog")

# here how we create "User" model (class) for DB. So the class itself is like a table, and the arguments like "id", "email" and ect. are columns where we specify it's type and other components  
# "User" and "Post" classes inherit from "db.Model" that is a class from SQLAlchemy 

class User(db.Model): # Integer is a type of the id, primary_key - unique ID for the user 
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

    # the method "__repr__(self)" shows how the object (user model) is printed whenever we print it out
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"  # so whenever the "user" object will be printed out it will show those arguments (we need this to be printed out in the python shell whenever we retrieve information)
    
    


# "post" class to hold our posts
class Post(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    # The type of this column should be "db.DateTime" and we need to create a default argument 
    # if there is no time filled in, 
    # so we need to import daytime class from flask and utcnow specific to show the time it was posted (time right now )
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow) # to hold the date when the post was made 
    content = db.Column(db.Text, nullable=False) # the content 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # id of the user who has posted the post. db.ForeignKey('user.id') specifies that the key has a relationship with the user model

    # what will be shown:
    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted}')"

# ! we also need to keep in mind that the relationship between the post and user models are "one to many",
# since the users will be the authors of the posts. So one user can have many posts and the post can have only one author - user  
# that is why we need to create an attribute in our user model and set it to db.relationship: posts = db.relationship('Post', backref='author', lazy=True)