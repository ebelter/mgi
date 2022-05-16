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
        db_uri = sqlite_uri_for_file(os.path.join(CromwellConf.db_fn))
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

class Pipeline(db.Model):
    __tablename__ = 'pipeline'
    __table_args__ = (
     db.UniqueConstraint('name',
       'kind',
       name='uniq_pipeline'),)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(length=32), nullable=False, index=True)
    kind = db.Column(db.String(length=32), nullable=False, index=True)
    wdl = db.Column(db.String(length=128), nullable=False, index=True)
    imports = db.Column(db.String(length=128), nullable=True, index=True)

    workflows = db.relationship("Workflow", backref="pipeline", lazy="dynamic")
#-- Pipeline

class Workflow(db.Model):
    __tablename__ = 'workflow'
    __table_args__ = (
     db.UniqueConstraint('name',
       name='uniq_worflow'),)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(length=32), nullable=False, index=True)
    status = db.Column(db.String(length=32), default="new", nullable=False, index=True)
    pipeline_id = db.Column(db.Integer, db.ForeignKey("pipeline.id"), nullable=True)
    #pipeline = db.relationship("Pipeline")
#-- Workflow
