from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# after we have imported the DB we need to specify the URI for DB (where the DB located)
# then we need to create the DB 

 
app = Flask(__name__)  # the app instance will be used to run the application (will be used in run.py)
app.config['SECRET_KEY'] = '5e5b968d2e77c6d37d2b17ee2bc819de' # we set secret key so we can use wtf forms, z.B. so we can stay logged in (look log in form )

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db' # here we specify a relative path ("///" - says that this path is relative) where the DB located (just a local file in the folder)
# after we create the location, we create the DB itself: we make an instance first:
db = SQLAlchemy(app) #SQLAlchemy DB instance, where the DB-Structure is represented as classes (colled models), we make those classes in "models.py"
# after that we create class models that will be our DB structure. Every class is going to be it's own table in the DB -> in models.py 
# after we created the classes for DB (structure/scheme) we go to python shell to create the DB itself, so it uses the structure we have created in "models.py" 

# > python3 # we should execute the shell inside of the folder where the app located 
# >>> from flaskblog import db  # makes instance of db
# >>> from flaskblog.models import User, Post  # creates a db structure 
# >>> db.create_all()  # creates an actual db file 

from flaskblog import routes # we need import routes here, cuz "routes.py" uses "app" variable, so we need to place it down after the "app" is initialized "app = Flask(__name__)", otherways there will be "circular import" trouble 