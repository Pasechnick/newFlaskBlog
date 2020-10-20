# to create a blueprint we need to import blueprint from flask 
from flask import render_template, request, Blueprint
from flaskblog.models import Post

#making the instance of a Blueprint, almost same as with instance of Flask "app" object 
main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    # grabbing this "page" variable we can pass it to paginate, with type "int" we insure if someone tries to enter something different form a number 
    page = request.args.get('page', 1, type = int) # we are grabbing the page, default page is 1, type int will cuz our site to appear a value error if someone passes anything other then integer as page number 
    # with .order_by(Post.date_posted.desc() we can order out posts from new...to...old way
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page=5) # instead of query.all() we are using paginate method to be able to set amount of posts to preload (instead of loading them all once)  
    return render_template("home.html", posts = posts) 

@main.route("/about")
def about():
    return render_template("about.html")