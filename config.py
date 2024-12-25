import os

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    NAS_DIRECTORY = 'upload'  #Path_to_the_NAS_storage, for we'll use local storage