import os # need to grab the file extention of the uploaded image and saves it do db with this extention (image.jpg, image.png, ect..)
import secrets # we need in order to get randomize picture name when we upload a new pic
from PIL import Image # this class is installed with Pillow package (pip3 install Pillow) so we can autoresize big pictures to prevent the site from loading big files
from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm # we need UpdateAccountForm so we can use validation check
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required # imports that class so we can check the user email and password validation with the db data, and with current user we can deliver user a



posts = [
    {
        'author': 'corey schafer',
        'title': 'blog post 1',
        'content': 'First post content',
        'date_posted': 'april 20, 2002'
    },

    {
        'author': 'alex mitu',
        'title': 'blog post 2',
        'content': 'second post content',
        'date_posted': 'april 23, 2012'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register", methods =['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pasword = bcrypt.generate_password_hash(form.password.data).decode('utf-8') 
        user = User(username = form.username.data, email = form.email.data, password = hashed_pasword) 
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created ! You are now able to log in', 'success') 
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)


@app.route("/login", methods =['GET', 'POST'])
def login():
    if current_user.is_authenticated: 
        return redirect(url_for('home'))
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first() 
        if user and bcrypt.check_password_hash(user.password, form.password.data): 
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next') 
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("login unsuccessful. Pls check ur email  and password", "danger")
    return render_template('login.html', title = 'Login', form = form)



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


# logic for uploading a new picture as avatar and saving in DB 
# we take picture data as argument
def save_picture(form_picture):
    random_hex = secrets.token_hex(8) # saves picture we upload with random hex token 8 bytes. so there is no same names in the DB
    # "os.path.splitext" function return two values: file name without the extention and the extention itself. So with underscore "_"  we through away the variable name and we grab the name (also can use "f_name"), we grab the extention with "f_ext"
    # form_picture - will be the data from the field (name of the picture)
    _, f_ext = os.path.splitext(form_picture.filename) # we need the file extention at the end of the filename. we do not need to grab the file name so we can use underscore "_" to through away a variable name 
    picture_fn = random_hex + f_ext # makes name for the uploaded picture ("picture_fn" - picture filename)
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn) # full path to the package directory
    
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
@login_required 
def account():
    # creates an instance of that update account form 
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # looks for picture data 
        if form.picture.data: 
            picture_file = save_picture(form.picture.data) # saves picture through "save_picture" function that accepts argument - the input data "form.picture.data" - the picture itself
            # saves the uploaded picture as new picture for user
            current_user.image_file = picture_file
        # if the form is valid we can update and commit data directly in SQL db
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated !', 'success')
         # we redirect right after data submitted, cuz of get\post method ("post-get redirect pattern")
        return redirect(url_for('account'))
    # as soon as we getting redirected to account page it should populate the form with the current data of the user:
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    # here we set the image file that will be passed in the account template
    # it grabs the "image_file" in the user model (models.py) where we hardcoded that the default user image is the "default.jpg"
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file) 
    # we pass in the "image_file" variable into the account template (so it will be shown at "account.html") as additional argument. This way we can use now the "image_file" as source of the image
    # we also pass in the instance of "updateAccountForm()" through "form" variable as argument, so we can use it in the account template
    return render_template('account.html', title = 'Account', image_file = image_file, form=form)