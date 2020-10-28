import os 
import secrets
from PIL import Image 
from flask import render_template, url_for, flash, redirect, request, abort # import abort for update route
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm # importing "PostForm" class so we can use instance of it in "/post/new" route to be able to post a new post
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required 


@app.route("/")
@app.route("/home")
def home():
    # grabs all posts from the DB, that have been made. The way we display those Posts we implement in home.html template
    posts = Post.query.all() 
    return render_template("home.html", posts = posts)

@app.route("/about")
def about():
    return render_template("about.html")

#  methods =['GET', 'POST'] list of allowed methods when we press sign up button 
@app.route("/register", methods =['GET', 'POST'])
def register():
    if current_user.is_authenticated: # current user check
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        #so if the form valid to submit (all length and signs are correct) we can hash the password and do the authentication procedure 
        hashed_pasword = bcrypt.generate_password_hash(form.password.data).decode('utf-8') # "form.password.data" is the password that user has entered and ".decode('utf-8')" is needed to decde from bytes to a regular string
        user = User(username = form.username.data, email = form.email.data, password = hashed_pasword) # getting the data from user into the db, where we get allready hashed password with "password = hashed_pasword"
        #saving the entered dta to the db
        db.session.add(user)
        db.session.commit()
        # creating the message for successfull sign up with the flash message
        flash(f'Your account has been created ! You are now able to log in', 'success') # with the help of format methode (f string) - f'text text {form.username.data}!' we can use placeholder inside of a text
        return redirect(url_for('login')) # so after the form is sended we redirect the user at the home function -> @app.route("/home") def home(): return render_template("home.html", posts = posts) 
    return render_template('register.html', title = 'Register', form = form)


@app.route("/login", methods =['GET', 'POST'])
def login():
    if current_user.is_authenticated: # current user check
        return redirect(url_for('home'))
    form = LoginForm()
    #  creating some dummy data to check the login form 
    if form.validate_on_submit():
        # before we were simply checking the hardcoded data, and now we need to check the database for valid data 
        # firstly the user will be logged in with an email, so we need to write a check for the email in the db:
        user = User.query.filter_by(email = form.email.data).first() # finds the first User by entered email in the id
        if user and bcrypt.check_password_hash(user.password, form.password.data): # so if the user exist and the password the user entered is valid we want to login the user and we also need to import the login user function 
            login_user(user, remember = form.remember.data) # "user" - what we want to login, "remember" - remember me form (boolean) we have created
            next_page = request.args.get('next') # this line 
            return redirect(next_page) if next_page else redirect(url_for('home')) # use of ternary conditional 
        else:
            flash("login unsuccessful. Pls check ur email  and password", "danger")
    return render_template('login.html', title = 'Login', form = form)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


# logic for uploading a new picture as avatar 
def save_picture(form_picture):
    random_hex = secrets.token_hex(8) # saves picture we upload with random hex token 8 bytes
    _, f_ext = os.path.splitext(form_picture.filename) # we need the file extention at the end of the filename. we do not need to grab the file name so we can use underscore "_" to through away a variable name 
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn) #full path to the package directory
    
    # resizing picture (the upload image might be too big, so the page will load slowly in some cases), so we can change it to our needed size
    output_size = (125, 125) # sets the size...
    i = Image.open(form_picture) # we create a new image
    i.thumbnail(output_size) # will resize

    i.save(picture_path) # saves resized pic (i) to it's path

    # so right after a user updates it's account avatar the uploaded picture will be resized in: 125 x 125 pixels and saved in our file system
    # and the picture name is hashed as we have claimed 
    # we can also delete the old pictures but next time... 
    
    return picture_fn


@app.route("/account", methods =['GET', 'POST'])
@login_required #extention knows that we need to be logged in to access this route 
def account():
    # creates an instance of that Update form 
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # if the form is valid we can update data directly in SQL db
        if form.picture.data: 
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated !', 'success')
         # we redirect right after data submitted, cuz of get\post method
        return redirect(url_for('account'))
    elif request.method == "GET":
        # populate the form with the current data of the user
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file) # it grabs the image in the user model (models.py) where we hardcoded that the default user image is the "default.jpg"
    return render_template('account.html', title = 'Account', image_file = image_file, form=form)


# route to create posts
@app.route("/post/new", methods =['GET', 'POST']) 
@login_required # to create a post requires to be logged in 
def new_post():
    form = PostForm() # instance of the PostForm class from forms.py so we can save data in DB that will be input from create_post template 
    if form.validate_on_submit():
        # connection to the data base, so the post we create will be saved in the db
        post = Post(title=form.title.data, content=form.content.data, author=current_user) # form.title.data, form.content.data - the input data that the user put in the form (in create_post template)
        db.session.add(post)
        db.session.commit() # will add the post to db
        flash("Your Post has been created !", "success")
        return redirect(url_for("home"))
    return render_template('create_post.html', title = 'New Post', form = form, legend = 'New Post')



# with flask we can make a variables within our routes, so we can create a route with id of a specific post
# we want to create an id, where it is a part if the route, so that we can access a specific post 
# - <int:post_id> where "int" is what we can expect from the variable "post_id" to be (can be "string" or etc...), so by putting "int" we specify "post_id" variable to be an integer number
@app.route("/post/new/<int:post_id>") # so we basiclay create "post_id" within the route itself, so if the number of the post will be "1" "post_id" will be 1, if number of the post will be "2" "post_id" will be 2
def post(post_id):
    # lets get this post if it exists - we getting this by id
    # "post" variable will save the the number that "post_id" is
    post = Post.query.get_or_404(post_id) # we can use a normal ".get" or ".first" to get the id, but ".get_or_404" (give me the post with that id or return not exist error) will find the variable or return a 404 error (page does not exist) 
    # then, if the post does exist it will redirect us to the actual post
    return render_template('post.html', title = post.title, post=post)


# UPDATE post route 
@app.route("/post/new/<int:post_id>/update", methods =['GET', 'POST']) 
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    # only the user who wrote this post can update this post
    if post.author != current_user:
        abort(403) # 403 is http responce for a forbitten route 
    form = PostForm()
    # within here we actually update the post with new values:
    # where "form.title.data" and "form.content.data" are the inputs
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data 
        db.session.commit() # sending the data to DB without using db.session.add() cuz those values are already in the DB and we just change them not creating the new
        flash('Your post has been updated !', 'success')
        return redirect(url_for('post', post_id=post.id)) # redirects to that updated specific post
    elif request.method == 'GET': # populates the form with below values (old text and title) when we go to the update post route
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title = 'Update Post', form = form, legend = 'Update Post') # is 


# delete route
@app.route("/post/new/<int:post_id>/delete", methods =['POST']) # we do not need GET request, because we are going to accept when they submitted from that modal 
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    # delete command and then commiting the changes
    db.session.delete(post)
    db.session.commit()
    flash('Your Post has been deleted !', 'success')
    return redirect(url_for('home'))


