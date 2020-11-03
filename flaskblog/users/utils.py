import os
import secrets
from PIL import Image
from flask import url_for, current_app # we need current_app so that we use it instead of "app "instance
from flask_mail import Message
from flaskblog import mail


# logic for uploading a new picture as avatar 
def save_picture(form_picture):
    random_hex = secrets.token_hex(8) # saves picture we upload with random hex token 8 bytes
    _, f_ext = os.path.splitext(form_picture.filename) # we need the file extention at the end of the filename. we do not need to grab the file name so we can use underscore "_" to through away a variable name 
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn) #full path to the package directory
    
    # resizing picture (the upload image might be too big, so the page will load slowly in some cases), so we can change it to our needed size
    output_size = (125, 125) # sets the size...
    i = Image.open(form_picture) # we create a new image
    i.thumbnail(output_size) # will resize

    i.save(picture_path) # saves resized pic (i) to it's path

    # so right after a user updates it's account avatar the uploaded picture will be resized in: 125 x 125 pixels and saved in our file system
    # and the picture name is hashed as we have claimed 
    # we can also delete the old pictures but next time... 
    
    return picture_fn


# EMAIL SENDING 
# with this function we can sent email to the user with token and instructions to reset the password 
# before we also need to install another flask extention flask-mail
def send_reset_email(user):
    token = user.get_reset_token()
    # we also need to keep in mind that the sender email has to have something from the damain name or it will land in the spam folder 
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
    # _external=True needs to get an absolute url rather then a relative (like in our app directory)
    # keep in mind that we need to write this message without tab or space
    msg.body = f''' To reset your password visit the folowing link:
{url_for('users.reset_token', token = token, _external=True)} 

If you did not make ths request then simply ignore this email and no changes will be made
'''
    mail.send(msg) # the actual code that sends the email