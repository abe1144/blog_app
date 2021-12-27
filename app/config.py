import os

base_dir = os.path.dirname(os.path.abspath(__name__))


class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(base_dir, 'database.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'asldkfjaslkjfioweor203984oiasdfjl'
    SECURITY_PASSWORD_SALT = 'skdfjalsdjf'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    UPLOADED_IMAGES_DEST = 'static/images/uploads'
    UPLOADED_PATH='static/images/uploads'
