import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import create_engine

app = Flask(__name__)
#default_db_fn = db_url_for_file(os.path.join("server", "db"))
app.config['SQLALCHEMY_DATABASE_URI'] = None
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

def create(url):
    engine = create_engine(url)
    db.metadata.create_all(engine)

def url_for_file(fn):
    return 'sqlite:///' + os.path.abspath(fn)

def set_url(db_url):
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url

class Pipeline(db.Model):
    __tablename__ = 'pipeline'
    __table_args__ = (
     db.UniqueConstraint('name',
       'kind',
       name='uniq_pipeline'),)
    id = db.Column((db.Integer), primary_key=True, autoincrement=True)
    name = db.Column(db.String(length=32), nullable=False, index=True)
    kind = db.Column(db.String(length=32), nullable=False, index=True)
    wdl = db.Column(db.String(length=128), nullable=False, index=True)
    imports = db.Column(db.String(length=128), nullable=True, index=True)
