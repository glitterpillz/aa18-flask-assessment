import os

class Configuration:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SECRET_KEY = 'beepboop'
    SQLALCHEMY_TRACK_MODIFICATIONS = False