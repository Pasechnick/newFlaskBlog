from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed # need ths to upload files into the db, and allowance to be able to upload surtain files (validator)
from flask_login import current_user # we need current user for update user info (for data check )
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User # we need to import User to make the validation Error message

# reg form inherits from FlaskForm


class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)]) # the length of the username must be from 2 to 20 characters
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                            validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # with this template function we can prevent showing the flaskerror page instead with our error messages under the sign up fields (username, email...)
    # ^it is taken from "wtf_forms" documentaton 
    # def validate_field(self, field):
    #     if True:
    #         raise ValidationError('Validation Message')

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
    remember = BooleanField('Remember Me') # allows user to stay logged in for some time, using a secure cookie 
    submit = SubmitField('Login')


# the form for updating an account info in the account route
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])]) # with FileAllowed validator we can validate particular file extention                            
    submit = SubmitField('Update')


    # with current_user class we want to make a check, so if the username/email does not match to current user's we make an update 
    def validate_username(self, username):
        # the username validation check
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('Validation Message: That Username is taken, please use another')

    def validate_email(self, email):
        # the email validation check
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('Validation Message: That Email is taken, please use another')