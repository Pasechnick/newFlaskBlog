from flask import Flask
from flask_sqlalchemy import SQLAlchemy

 
app = Flask(__name__)
app.config['SECRET_KEY'] = '5e5b968d2e77c6d37d2b17ee2bc819de'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db = SQLAlchemy(app)

from flaskblog import routes