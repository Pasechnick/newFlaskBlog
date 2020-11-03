from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager 
from flask_mail import Mail
from flaskblog.config import Config # the "Config" class that we paste in "app.config.from_object()" method so we can configurate the app using this configurations

 
# extention objects we will not move to create_app function, cuz we want them to be created outside of the function, but initialized them inside 
# this is design pattern of flask. so we initialize them at the top of the file without ".app" and inside of the "create_app()" we use the ".init_app" method to pass the application to all this extentions 
db = SQLAlchemy()
bcrypt = Bcrypt() # creates that class to initialize through the app
login_manager = LoginManager() # login class 
login_manager.login_view = 'users.login' # function name of our route
login_manager.login_message_category = 'info' # how would be the "Please log in to access this page." message look like
mail = Mail() 


# we would like to move creation of the app into a function, so we could make different instances of the app with different configurations
 
# this function will take an argument for what configuration object we want to use for our app
# so we set right now the argument as our config class we have just created in config.py as DEFAULT configuration
# now we move the creation of the app inside of this function:
# the extention we use will remain outside of this function 
def create_app(config_class=Config):

    # we move the creation of application inside of this create_app function
    app = Flask(__name__)

    # here goes method for configuration values to set up, where as argument goes the configuration class we have crated in "config.py"
    app.config.from_object(Config)

    # here we import the new instances of blueprints and register blueprints:
    # imports of blueprints
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main

    # we use the ".init_app" method to pass the application to all of those extentions. So for each of the extentions we run ".init_app()" method where we pass in the "app" instance 
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    # registration of blueprints
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    # after that we return the application 
    return app

# after all that, we have to replace the "app" instance for "current_app" in the entire application

