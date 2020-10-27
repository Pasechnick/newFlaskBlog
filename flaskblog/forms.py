from flask_wtf import FlaskForm
# with flask_wtf we actually write python classes that will be representatives of our forms and then they will be automaticlay converted in HTML forms when we see them through templates
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo



# reg form inherits from FlaskForm

# whinthin the form it will have some form fields and they will be imported classes as well
# this classes are installed within flask_wtf but we need to import them here extra: StringField, PasswordField, SubmitField, BooleanField
# we get those classes using attributes: username, email, passeord...
# inside of those fields we need some validators to validate the input data, we also need import them: DataRequired, Length, Email, EqualTo
class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)]) # the length of the username must be from 2 to 20 characters
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                            validators=[DataRequired(), EqualTo('password')]) # argument in "EqualTo()" should be a field that we want it to be equal to: "password" 
    submit = SubmitField('Sign Up')

# class FormName(FlaskForm):
#       atributeForTheFieldClass = FlaskWTFField('Name/Label', )
#       field2
#       field3
#       ...


class LoginForm(FlaskForm):
    email = StringField('Email',
                            validators=[DataRequired(), Email()])
    password = PasswordField('Password', 
                            validators=[DataRequired()])
    remember = BooleanField('Remember Me') # allows user to stay logged in for some time, using a secure cookie 
    submit = SubmitField('Login')