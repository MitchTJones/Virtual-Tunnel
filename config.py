import os

class Config(object):
    SECRET_KEY = 'hci-2020-hard-to-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(os.path.abspath(os.path.dirname(__file__)), 'users.db')
    IMAGE_UPLOADS = 'static/uploads'

