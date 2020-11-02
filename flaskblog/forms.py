from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed 
from flask_login import current_user 
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField # text area field is needed for the content
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User 


class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                            validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError('Validation Message: That Username is taken, please use another')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('Validation Message: That Email is taken, please use another')



class LoginForm(FlaskForm):
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired()])
    remember = BooleanField('Remember Me') 
    submit = SubmitField('Login')



class UpdateAccountForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])]) 
    submit = SubmitField('Update')


   
    def validate_username(self, username):
        
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('Validation Message: That Username is taken, please use another')

    def validate_email(self, email):
        
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('Validation Message: That Email is taken, please use another')


# a new class to post a post 
class PostForm(FlaskForm):
     title = StringField('Title', validators =[DataRequired()]) # every post has to have a title
     content = TextAreaField('Content', validators=[DataRequired()]) # every post has a text area field
     submit = SubmitField('Post') 

     # then wee create an instance of this form in the routes.py


# this is a form for our route. Reset password page where a user can submit their email for their account so instructions can be send
# remember that this inherits from FlaskForm class...
class RequestResetForm(FlaskForm):
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    # validation if the account NOT exist for the email address
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        # then, if there is no user under this email, the user have to register
        if user is None:
            raise ValidationError('There is no account with that email, register first.')

# form where the user actually reset the password
class ResetPasswordForm(FlaskForm):
    # new password will be typed here
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                         validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

# right after we have created those two forms: RequestResetForm, ResetPasswordForm, we have to create routes that will handle them and then we create the html templates