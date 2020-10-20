# to create a blueprint we need to import blueprint from flask 
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
#after moving all imports we need sometimes to change the place where it has been imported "flaskblog.users.forms" and ect...
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

#making the instance of a Blueprint, almost same as with instance of Flask "app" object 
users = Blueprint('users', __name__)

# We change app.routes to users.route cuz we using it as a users instance right now

#  methods =['GET', 'POST'] list of allowed methods when we press sign up button 
@users.route("/register", methods =['GET', 'POST'])
def register():
    if current_user.is_authenticated: # current user check
        return redirect(url_for('main.home'))
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
        return redirect(url_for('users.login')) # so after the form is sended we redirect the user at the home function -> @app.route("/home") def home(): return render_template("home.html", posts = posts) 
    return render_template('register.html', title = 'Register', form = form)


@users.route("/login", methods =['GET', 'POST'])
def login():
    if current_user.is_authenticated: # current user check
        return redirect(url_for('main.home'))
    form = LoginForm()
    #  creating some dummy data to check the login form 
    if form.validate_on_submit():
        # before we were simply checking the hardcoded data, and now we need to check the database for valid data 
        # firstly the user will be logged in with an email, so we need to write a check for the email in the db:
        user = User.query.filter_by(email = form.email.data).first() # finds the first User by entered email in the id
        if user and bcrypt.check_password_hash(user.password, form.password.data): # so if the user exist and the password the user entered is valid we want to login the user and we also need to import the login user function 
            login_user(user, remember = form.remember.data) # "user" - what we want to login, "remember" - remember me form (boolean) we have created
            next_page = request.args.get('next') # this line 
            return redirect(next_page) if next_page else redirect(url_for('main.home')) # use of ternary conditional 
        else:
            flash("login unsuccessful. Pls check ur email  and password", "danger")
    return render_template('login.html', title = 'Login', form = form)


# logout route we need ...
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods =['GET', 'POST'])
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
        return redirect(url_for('users.account'))
    elif request.method == "GET":
        # populate the form with the current data of the user
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file) # it grabs the image in the user model (models.py) where we hardcoded that the default user image is the "default.jpg"
    return render_template('account.html', title = 'Account', image_file = image_file, form=form)


# route to go to all users's post by clicking on the username's tag
@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type = int)
    user = User.query.filter_by(username=username).first_or_404() # get the first user with this username and if u get non, return 404 "no found" error 
    # by putting "\" (backlash) we can break up multiple lines without actually breaking the code, so we can look up the code clear 
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page = page, per_page=5)
    return render_template("user_posts.html", posts = posts, user=user) 


#TWO ROUTES WITH RESET PASSWORD FUNCTIONALITY:

# the route to reset the password
# user enters his email addres, where the reset password information be send
@users.route("/reset_password", methods =['GET', 'POST']) 
def reset_request():
    # making sure that the user is logged out
    if current_user.is_authenticated: 
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit(): # at this point the user has submitted an email into our form, so we need to grab the user for that email
        user = User.query.filter_by(email=form.email.data).first()
        # after we got the user, we need to send this user an email with their token, so they can reset the password
        send_reset_email(user) # this function is written above
        flash('An email has been sent with instructions to reset your password', 'info') 
        return redirect(url_for('users.login'))
    return render_template("reset_request.html", title = 'Reset Password', form=form)



# here is the route where the user actually resets his password (the route for the request for reset is above)
# to make sure that it is the actual user we need to be sure that the toke that we gave them in the email is active
# # so by sending them an email with a link containing this token we will know that it is them when they navigate to this route 
# so this route is similar to this above but accept the token as paramenter
   
@users.route("/reset_password/<token>", methods =['GET', 'POST']) 
def reset_token(token):
    # making sure that the user is logged out
    if current_user.is_authenticated: 
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    # if we dont get user back, it means the token is invalid or expired, so we put this conditional 
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    # and if the token valid we can dispaly the form so the user can update it's password
    form = ResetPasswordForm()
    # getting the password changed and saved to the db
    if form.validate_on_submit():
        hashed_pasword = bcrypt.generate_password_hash(form.password.data).decode('utf-8') 
        user.password = hashed_pasword # it will hash that password from our "form.password.data" which we do have a password field in this reset passord from above
        db.session.commit() # will commit the changes of user's password 
        flash('Your password has been updated ! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    # the user will be send to the form to update the password
    return render_template("reset_token.html", title = 'Reset Password', form=form)