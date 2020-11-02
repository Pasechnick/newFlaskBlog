import os # importing for the email config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager 
from flask_mail import Mail # the extention we need for password reset procedure



 
app = Flask(__name__)
app.config['SECRET_KEY'] = '5e5b968d2e77c6d37d2b17ee2bc819de'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app) # creates that class to initialize through the app
login_manager = LoginManager(app) # login class 
login_manager.login_view = 'login' # function name of our route
login_manager.login_message_category = 'info' # how would be the "Please log in to access this page." message looks like


# setting up a mail configuration 
# we say that we use gmail protocols for the mail client. 
# We use environmental variables: EMAIL_USER, EMAIL_PASS, so the MAIL_SERVER can use tha actual password and email to be able to send the email

# for some reason we have to rework the email congigs...
# i also need to turn off "less secure app access" in security settings of gmail otherways it will be an authentication error 

app.config['MAIL_SERVER'] = 'smtp.gmail.com' # it was smtp.googlemail.com
app.config['MAIL_PORT'] = 465 # was 587
app.config['MAIL_USE_SSL'] = True # was TLS
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app) # initializing 

from flaskblog import routes
