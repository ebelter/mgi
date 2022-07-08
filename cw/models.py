from cw import db

class Config(db.Model):
    __tablename__ = 'config'
    __table_args__ = (
        db.UniqueConstraint(
            "group",
            "name",
            name="uniq_config",
        ),
    )
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group = db.Column(db.String(length=32), default="general", nullable=False, index=True)
    name = db.Column(db.String(length=32), nullable=False, index=True)
    value = db.Column(db.String(length=128), nullable=True)
#-- Config

class Pipeline(db.Model):
    __tablename__ = 'pipeline'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(length=32), nullable=False, index=True, unique=True)
    wdl = db.Column(db.String(length=256), nullable=False)
    imports = db.Column(db.String(length=256), nullable=True)
    outputs = db.Column(db.String(length=256), nullable=True)

    workflows = db.relationship("Workflow", backref="pipeline", lazy="dynamic")
#-- Pipeline

class Workflow(db.Model):
    __tablename__ = 'workflow'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(length=32), nullable=False, index=True)
    wf_id = db.Column(db.String(length=48), nullable=False, unique=True, index=True)
    pipeline_id = db.Column(db.Integer, db.ForeignKey("pipeline.id"), nullable=False, index=True)
    status = db.Column(db.String(length=32), default="new", nullable=False)
    inputs = db.Column(db.String(length=256), nullable=True)
#-- Workflow
