from mgi import db

class Entity(db.Model):
    __tablename__ = 'entity'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=48), unique=True, index=True)
    kind = db.Column(db.String(length=16), nullable=False, index=True)

    features = db.relationship("EntityFeature", back_populates="entity")
    paths = db.relationship("EntityPath", back_populates="entity")
    def __str__(self):
        return self.name
#-- Entity

class EntityFeature(db.Model):
    __tablename__ = 'entity_feature'
    __table_args__ = (
        db.UniqueConstraint(
            "entity_id",
            "group",
            "name",
            name="uniq_efeature",
        ),
    )
    entity_id = db.Column(db.Integer, db.ForeignKey("entity.id"), primary_key=True)
    group = db.Column(db.String(length=32), primary_key=True)
    name = db.Column(db.String(length=48), primary_key=True)
    value = db.Column(db.String(length=128))

    entity = db.relationship("Entity", back_populates="features")
    def __str__(self):
        return ":".join([self.name, self.group, self.value])
#-- EntityFeature

class EntityPath(db.Model):
    __tablename__ = 'entity_path'
    __table_args__ = (
        db.UniqueConstraint(
            'entity_id',
            'value',
            name='uniq_epath',
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    entity_id = db.Column(db.Integer, db.ForeignKey("entity.id"), nullable=False)
    group = db.Column(db.String(length=32), primary_key=True)
    value = db.Column(db.String(length=256), nullable=False, unique=True, index=True)
    checksum = db.Column(db.String(length=32), nullable=True)
    kind = db.Column(db.String(length=16), nullable=False, index=True)
    exists = db.Column(db.Boolean, default=False)

    entity = db.relationship("Entity", back_populates="paths")
    def __str__(self):
        return self.value
#-- EntityPath
