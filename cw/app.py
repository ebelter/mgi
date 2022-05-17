import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = None
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from cw.conf import CromwellConf
from cw.models import Config, Pipeline, Workflow

def create():
    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    db.metadata.create_all(engine)

def sqlite_uri_for_file(fn):
    return 'sqlite:///' + os.path.abspath(fn)

def connect(db_uri=None):
    if db_uri is None:
        db_uri = sqlite_uri_for_file(os.path.join(CromwellConf.server_db_fn()))
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    return db

def uri(db_uri=None):
    if db_uri is not None:
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    return app.config['SQLALCHEMY_DATABASE_URI']
