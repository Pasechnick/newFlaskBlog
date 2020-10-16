from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt # getting that bcrypt class so we can hash the password 
from flask_login import LoginManager # get the login extention so we can login

 
app = Flask(__name__)
app.config['SECRET_KEY'] = '5e5b968d2e77c6d37d2b17ee2bc819de'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app) # creates that class to initialize through the app
login_manager = LoginManager(app) # login class 
login_manager.login_view = 'login' # function name of our route
login_manager.login_message_category = 'info' # how would be the "Please log in to access this page." message looks like


from flaskblog import routes