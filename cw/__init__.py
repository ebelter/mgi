import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine

def db_uri(db_uri=None):
    if db_uri is not None:
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    return flask_app.config['SQLALCHEMY_DATABASE_URI']

DN = os.environ.get("CW_DN", None)
if DN is None:
    DN = os.getcwd()
DB_URI = os.environ.get("CW_DB_URI", None)
if DB_URI is None:
    DB_URI = "sqlite:///"+os.path.join(DN, "server", "db")
flask_app = Flask(__name__)
flask_app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_uri(db_uri=DB_URI)
flask_app.app_context().push()

db = SQLAlchemy(flask_app)
db.uri = db_uri
migrate = Migrate(flask_app, db)

from cw.models import Config, Pipeline, Workflow

class AppCon(object):
    def __init__(self):
        self.dn = DN
        self.resources_dn = os.path.join(os.path.dirname(__file__), "resources")
        self.known_directories = set(["db", "logs", "runs", "server"])

    def dn_for(self, name):
        if name not in self.known_directories:
            raise Exception(f"Unknown directory: {name}")
        return os.path.join(self.dn, name)

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
#--
appcon = AppCon()

def create_db(uri=None, extra_configs=[]):
    if uri is None:
        uri = db.uri()
        if uri is None:
            raise Exception("No DB URI given or found!")
    engine = create_engine(uri)
    db.metadata.create_all(engine)
    server_dn = os.path.join(appcon.dn, "server")
    configs = [
            ["general", "db_dn", os.path.join(appcon.dn, "db")],
            ["general", "logs_dn", os.path.join(appcon.dn, "logs")],
            ["general", "runs_dn", os.path.join(appcon.dn, "runs")],
            ["general", "server_dn", server_dn],
            ["server", "port", "8888"],
            ["server", "server_start_fn", os.path.join(server_dn, "start")],
            ["resources", "conf_template_fn", os.path.join(appcon.resources_dn, "server.conf.jinja")],
            ["resources", "run_template_fn", os.path.join(appcon.resources_dn, "server.run.jinja")],
            ["resources", "start_template_fn", os.path.join(appcon.resources_dn, "server.start.jinja")],
            ["server", "conf_fn", os.path.join(server_dn, "conf")],
            ["server", "run_fn", os.path.join(server_dn, "run")],
            ["server", "start_fn", os.path.join(server_dn, "start")],
            ]
    configs += extra_configs
    for group, name, value in configs:
        appcon.set(group=group, name=name, value=value)
#-- create_db
