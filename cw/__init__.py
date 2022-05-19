import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine

from cw.helpers import sqlite_uri_for_file

flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = None
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(flask_app)
def db_uri(db_uri=None):
    if db_uri is not None:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    return flask_app.config['SQLALCHEMY_DATABASE_URI']
db.uri = db_uri

migrate = Migrate(flask_app, db)
dn = os.environ.get("CW_DN", None)
if dn is None:
    dn = os.getcwd()
db_uri = os.environ.get("CW_DB_URI", None)
if db_uri is None:
    db_uri = sqlite_uri_for_file(os.path.join(dn, "cw.db"))
db.uri(db_uri)

from cw.models import Config, Pipeline, Workflow

def create_db(uri=None):
    if uri is None:
        uri = db.uri()
        if uri is None:
            raise Exception("No DB URI given or found!")
    engine = create_engine(uri)
    db.metadata.create_all(engine)
#-- create_db
