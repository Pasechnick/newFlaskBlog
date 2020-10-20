# to create a blueprint we need to import blueprint from flask 
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

#making the instance of a Blueprint, almost same as with instance of Flask "app" object 
posts = Blueprint('posts', __name__)


# route to create posts
@posts.route("/post/new", methods =['GET', 'POST']) 
@login_required
def new_post():
    form = PostForm() # instance of the form to send 
    if form.validate_on_submit():
        # connection to the data base, so the pos we create will be saved in the db
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit() # will add the post to db
        flash("Your Post has been created !", "success")
        return redirect(url_for("main.home"))
    return render_template('create_post.html', title = 'New Post', form = form, legend = 'New Post')


# with flask we can make a variables within our routes
# we want to create an id, where it is a part if the route
# - <int:post_id> where "int" is what we can expect from the variable to be (can be "string" or etc...)
@posts.route("/post/new/<int:post_id>") 
def post(post_id):
    # lets fetch this post if it exists - we getting this by id
    post = Post.query.get_or_404(post_id) # we can use a normal ".get" or ".first" to get the id, but ".get_or_404" will find the variable or return a 404 error (page does not exist) 
    # then, if the post exist it will redirect us to the actual post
    return render_template('post.html', title = post.title, post=post)


#update route 
@posts.route("/post/new/<int:post_id>/update", methods =['GET', 'POST']) 
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    # only the user who wrote this post can update this post
    if post.author != current_user:
        abort(403) # 403 is http responce for a forbitten route 
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated !', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET': # then populate the for with below values (old text and title)
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title = 'Update Post', form = form, legend = 'Update Post')


#delete route
@posts.route("/post/new/<int:post_id>/delete", methods =['POST']) 
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your Post has been deleted !', 'success')
    return redirect(url_for('main.home'))