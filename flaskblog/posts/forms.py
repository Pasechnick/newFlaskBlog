from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


# a new class to post a post 
class PostForm(FlaskForm):
     title = StringField('Title', validators =[DataRequired()]) # every post has to have a title
     content = TextAreaField('Content', validators=[DataRequired()]) # every post has a text area field
     submit = SubmitField('Post') 

     # then wee create an instance of this form in the routes.py