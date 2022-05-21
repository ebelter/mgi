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
DN = os.environ.get("CW_DN", None)
if DN is None:
    DN = os.getcwd()
DB_URI = os.environ.get("CW_DB_URI", None)
if DB_URI is None:
    DB_URI = sqlite_uri_for_file(os.path.join(DN, "server", "db"))
    #DB_URI = sqlite_uri_for_file(os.path.join(DN, "cw.db"))
db.uri(DB_URI)

from cw.models import Config, Pipeline, Workflow

def create_db(uri=None):
    if uri is None:
        uri = db.uri()
        if uri is None:
            raise Exception("No DB URI given or found!")
    engine = create_engine(uri)
    db.metadata.create_all(engine)
#-- create_db

class AppCon(object):
    def __init__(self):
        pass

    def get(self, name, group="general"):
        c = Config.query.filter(Config.group == group, Config.name == name).one_or_none()
        if c is None:
            return None
        return c.value

    def set(self, name, value, group="general"):
        c = Config.query.filter(Config.group == group, Config.name == name).one_or_none()
        if c is None:
            c = Config(name=name, group=group)
        c.value = value
        db.session.add(c)
        db.session.commit()
        return c.value

    def dn_for(self, name):
        return os.path.join(DN, name)

    def server_start_fn(self):
        return os.path.join(self.dn_for("server"), "start")
#--
appcon = AppCon()
