# to create a blueprint we need to import blueprint from flask 
from flask import render_template, request, Blueprint
from flaskblog.models import Post

#making the instance of a Blueprint, almost same as with instance of Flask "app" object 
main = Blueprint('main', __name__)

# We change app.routes to main.route cuz we using it as a main blueprint instance right now

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type = int) 
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page=5) 
    return render_template("home.html", posts = posts) 

@main.route("/about")
def about():
    return render_template("about.html")