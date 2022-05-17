import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine

from cw.conf import CromwellConf

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = None
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

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

def uri():
    return app.config['SQLALCHEMY_DATABASE_URI']

class Config(db.Model):
    __tablename__ = 'config'
    __table_args__ = (
        db.UniqueConstraint(
            "name",
            "group",
            name="uniq_config",
        ),
    )
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(length=32), nullable=False, index=True)
    group = db.Column(db.String(length=32), default="general", nullable=False, index=True)
    value = db.Column(db.String(length=128), nullable=True)
#-- Config

class Pipeline(db.Model):
    __tablename__ = 'pipeline'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(length=32), nullable=False, index=True, unique=True)
    wdl = db.Column(db.String(length=128), nullable=False)
    imports = db.Column(db.String(length=128), nullable=True)

    workflows = db.relationship("Workflow", backref="pipeline", lazy="dynamic")
#-- Pipeline

class Workflow(db.Model):
    __tablename__ = 'workflow'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wf_id = db.Column(db.String(length=48), nullable=False, index=True)
    name = db.Column(db.String(length=32), nullable=False, index=True)
    status = db.Column(db.String(length=32), default="new", nullable=False)
    pipeline_id = db.Column(db.Integer, db.ForeignKey("pipeline.id"), nullable=True, index=True)
#-- Workflow
