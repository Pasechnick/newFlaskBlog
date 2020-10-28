from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed # need ths to upload files into the db, and allowance to be able to upload certain files (validator)
from flask_login import current_user # we need current user for update user info (for data check) so that the user do not change values of username and ect. if he doesn't make changes
from wtforms import StringField, PasswordField, SubmitField, BooleanField
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


# also inherits from FlaskForm
# the form for updating an account info in the account route
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
                        # 'Update Profile Picture' - label. with FileField we can accept images so we can update picture of account. 
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])]) # with FileAllowed validator we can validate particular file extention                            
    submit = SubmitField('Update')


    # with current_user class we want to make a check, so if the username/email does not match to current user's we make an update 
    def validate_username(self, username):
        # the username validation check
        if username.data != current_user.username: # so the data (username) we enter will be checked with the data from DB
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError('Validation Message: That Username is taken, please use another')

    def validate_email(self, email):
        # the email validation check
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError('Validation Message: That Email is taken, please use another')