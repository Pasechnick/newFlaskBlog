import os # need to grab the file extention of the uploaded image and saves it do db with this extention (image.jpg, image.png, ect..)
import secrets # we need in order to get randomize picture name when we upload a new pic
from PIL import Image # this class is installed with Pillow package (pip3 install Pillow) so we can autoresize big pictures to prevent the site from loading big files
from flask import render_template, url_for, flash, redirect, request, abort # import abort for update route
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required 


@app.route("/")
@app.route("/home")
def home():
    # grabbing this "page" variable we can pass it to paginate, with type "int" we insure if someone tries to enter something different form a number 
    page = request.args.get('page', 1, type = int) # we are grabbing the page, default page is 1, type int will cuz our site to appear a value error if someone passes anything other then integer as page number 
    # with .order_by(Post.date_posted.desc() we can order out posts from new...to...old way
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page=5) # instead of query.all() we are using paginate method to be able to set amount of posts to preload (instead of loading them all once)  
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


# logout route we need ...
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
@login_required
def new_post():
    form = PostForm() # instance of the form to send 
    if form.validate_on_submit():
        # connection to the data base, so the pos we create will be saved in the db
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit() # will add the post to db
        flash("Your Post has been created !", "success")
        return redirect(url_for("home"))
    return render_template('create_post.html', title = 'New Post', form = form, legend = 'New Post')


# with flask we can make a variables within our routes
# we want to create an id, where it is a part if the route
# - <int:post_id> where "int" is what we can expect from the variable to be (can be "string" or etc...)
@app.route("/post/new/<int:post_id>") 
def post(post_id):
    # lets fetch this post if it exists - we getting this by id
    post = Post.query.get_or_404(post_id) # we can use a normal ".get" or ".first" to get the id, but ".get_or_404" will find the variable or return a 404 error (page does not exist) 
    # then, if the post exist it will redirect us to the actual post
    return render_template('post.html', title = post.title, post=post)


#update route 
@app.route("/post/new/<int:post_id>/update", methods =['GET', 'POST']) 
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
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET': # then populate the for with below values (old text and title)
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title = 'Update Post', form = form, legend = 'Update Post')


#delete route
@app.route("/post/new/<int:post_id>/delete", methods =['POST']) 
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your Post has been deleted !', 'success')
    return redirect(url_for('home'))


# route to go to all users's post by clicking on the username's tag
@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type = int)
    user = User.query.filter_by(username=username).first_or_404() # get the first user with this username and if u get non, return 404 "no found" error 
    # by putting "\" (backlash) we can break up multiple lines without actually breaking the code, so we can look up the code clear 
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page = page, per_page=5)
    return render_template("user_posts.html", posts = posts, user=user) 