
import os


class Config:

    # we want them to be constant variables so we remove the "app.config" section from the beginning
    # so there are keynames left

    # we also need to move our database info like the secret key and the uri of db in environmetal variables, 
    # cuz in the future this is the cummon practice. So we need to get used to this habbit
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')

    MAIL_SERVER = 'smtp.gmail.com' 
    MAIL_PORT = 465 
    MAIL_USE_SSL = True 
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')