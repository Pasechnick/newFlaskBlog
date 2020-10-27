from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError # we import "ValidationError" so we can can validate existend email and username with custom errors
from flaskblog.models import User # we need to import User class to make the validation Error message, we need access to "username" in DB


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

    # with this template function we can prevent showing the flaskerror page instead with our error messages under the sign up fields (username, email...)
    # it is taken from "wtf_forms" documentaton:
    # the "field" as argument - the fieldname that we want to validate (it should be inside of the class where we write the function, "RegistrationForm" currently and we checking for "username" and "email") 
    
    # def validate_field(self, field): 
    #     if True:
    #         raise ValidationError('Validation Message')

    # custom validation that prevent flask errors with the same data entered when sign up
    def validate_username(self, username): # prevent sign up with the same username
        user = User.query.filter_by(username = username.data).first() # we query submitted username in DB whether it already exists in the DB 
        if user: # so if this username exists in the DB there will be an error. So if there is nothing found, it will not hit "if" conditional
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
    remember = BooleanField('Remember Me') # allows user to stay logged in for some time, using a secure cookie 
    submit = SubmitField('Login')