import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

mgi_app = Flask(__name__)
class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
mgi_app.config.from_object(Config)
db = SQLAlchemy(mgi_app)
migrate = Migrate(mgi_app, db)

from mgi import models
