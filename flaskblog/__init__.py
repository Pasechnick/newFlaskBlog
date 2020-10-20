
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager 
from flask_mail import Mail # the extention we need for password reset procedure
from flaskblog.config import Config

 
# extention objects we will not move to create_app 
db = SQLAlchemy()

bcrypt = Bcrypt() # creates that class to initialize through the app
login_manager = LoginManager() # login class 
login_manager.login_view = 'users.login' # function name of our route
login_manager.login_message_category = 'info' # how would be the "Please log in to access this page." message looks like

mail = Mail() 



# this function will take an argument for what configuration object we want to use for our app
# so we set right now the argument as our config class we have just created in config.py 
def create_app(config_class=Config):
    # we move the creation of application inside of this create_app function
    app = Flask(__name__)
    app.config.from_object(Config)
    # here we import the new instances and register blueprints 
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app