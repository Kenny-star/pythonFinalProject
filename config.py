import os
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    