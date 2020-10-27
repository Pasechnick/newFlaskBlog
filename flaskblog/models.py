
from datetime import datetime
from flaskblog import db, login_manager # imports that "login_manager" instance from the init file
from flask_login import UserMixin # class that provides us with attributes and methods for login

# after we import login_manager, we also need to create a function with a decorator userloader
# for reloading user from the user_id stored in the session, so the extention needs to find the user by it's id to stay logged in for some time (session)
# so we need a user id from the db

# also the extention will expect to have the user model a curtain attributes and methods - 4 to be excact: "is authenticated", "is active", "is anonimus", "get id" 
# of course we could add all 4 methods by ourself, but the extention privides us with the class "UserMixin" that already has all that so we import this class. This class is part of "flask_login"

@login_manager.user_loader # we decorate this function with the name convention this way so the extention knows that this is that "user_id" it needs so the user can stay logged in for a session
def load_user(user_id): # so we need to get the user by it's id and we use ".get" methode
    return User.query.get(int(user_id))

# right after we import UserMixin class, we can use it in our Model
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

