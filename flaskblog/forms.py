from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed 
from flask_login import current_user 
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField # "TextAreaField" is needed for the post content - the text
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


# a new class to post a new post  
class PostForm(FlaskForm):
     title = StringField('Title', validators =[DataRequired()]) # every post has to have a title
     content = TextAreaField('Content', validators=[DataRequired()]) # every post must has a text area field
     submit = SubmitField('Post') # title of the submit button will be "Post"

     # then we create an instance of this form in the routes.py and we pass it in the create_post.html template, so we can read and save data to DB