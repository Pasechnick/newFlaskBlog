
from datetime import datetime
from flaskblog import db, login_manager # imports that login_manager class from the init file
from flask_login import UserMixin # class that provides us with attributes and methods for login

# we also need to create a function with a decoretor userloader - 
# for reloading user from the user id stored in the session 
# so we need a user id from the db

# also the extention will expect to have the user model a surtain attributes and methods - 4 to be excact: "is authenticated", "is active", "is anonimus", "get id" 
# of course we could add all 4 methods by ourself, but the extention privides us with the class UserMixin that we need to import   
@login_manager.user_loader # we decorete this function  with the name convention this way so the extention knows that this is that "user id"
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin): 
    id=db.Column(db.Integer, primary_key = True)
   
    username = db.Column(db.String(20), unique=True, nullable=False) 
    email = db.Column(db.String(120), unique=True, nullable=False) 
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False) 
    posts = db.relationship('Post', backref='author', lazy=True) 
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"



class Post(db.Model):
    id=db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow) 
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    
    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted}')"

