import click, csv

from mgi.models import db, Entity, EntityPath
from mgi.entity.helpers import resolve_entity_and_kind_from_value

update_help = """
    Update Entities Paths
    
    \b
    Give entity path features on the command line as equal separated name / value pairs.

    Entity name and/or file kind can be determined if not given. The entity name and file kind must be in the file name. This cannot be done if the value is a path.

    \b
    Entity Path Attributes
    entity    The entity name
    group     A group to gather paths by
    kind      bam, gvcf, ...
    checksum  A checksum for the files
    exists    True (true, 1, Y) or False (false, 2, N)
    value     The file or path

    \b
    UPDATE by giving all needed features on the command line.

    entity=sample_1 value=/data/sample_1.bam group=new kind=bam exists=0

    Have the command guess at the entity name and file kind:

    value=/data/sample_1.bam group=new exists=0

    \b
    UPDATE with a file of files. Give a headerless file with paths, and features on the command line. Entity name will be guessed from the file names.
    
    FILE contents:

    /data/sample_1.bam
    /data/sample_2.bam

    Command parameters:

    FILE group=new kind=bam exists=0

    \b
    UPDATE with a TSV of paths and features, optionally including features on the command line. TSV much contain a value. For ease, do not include the entity and/or kind, if they are in the file name.

    FILE contents:

    entity  value               kind  checksum  exists
    S1      /data/sample_1.bam  bam2  ghrhdj    Y
    S2      /data/sample_2.bam  bam2  hdhdfi    Y
    S3      /data/sample_3.bam  bam2  fgihfd    Y

    Command parameters:

    FILE group=chohort_22

    """

def get_entity(name, kind):
    return Entity.query.filter(Entity.name == name, Entity.kind == kind).one_or_none()
#-- get_entity

def add_entity(name, kind):
    return Entity(name=name, kind=kind)
#-- add_entity
    
def get_entity_path(features):
    return EntityPath.query.filter(EntityPath.entity_id == features["entity_id"], EntityPath.value == features["value"]).one_or_none()
#-- get_entity_path

def add_entity_path(attrs):
    return EntityPath(**attrs)
#-- add_entity_path

def update_entity_path(ep, attrs):
    for k, v in attrs:
        setattr(ep, k, v)
#-- update_entity_path

def update_entities_paths(rdr, features, entity_kind, create_entities=True):
    added, updated = 0, 0
    for ep_d in rdr:
        # Need a value
        if "value" not in ep_d:
            raise Exception(f"No entity path value given in:\n{ep_d}")

        # Get entity name from ep dict, then check features
        entity_name = ep_d.pop("entity", None)
        if entity_name is None:
            entity_name = features.pop("entity", None)

        # If not given, get entity name and ep kind from file name
        if entity_name is None or "kind" not in ep_id:
            ename1, kind, ename2 = resolve_entity_and_kind_from_value(ep_d["value"])
            if entity_name is None: # FIXME use ename2?
                entity_name = ename1
            if "kind" not in ep_d:
                ep_d["kind"] = kind

        # Add or create the entity
        entity = get_entity(name=entity_name, kind=entity_kind)
        if entity is None: # FIXME maybe do not create?
            entity = add_entity(entity_name, entity_kind)
            if entity is None:
                raise Exception("Failed to create entity: {entity_name} {entity_kind}")
            db.session.add(entity)
            db.session.flush()

        # Update the sp dict
        ep_d["entity_id"] = entity.id
        ep_d.update(features)
        # Add or create the ep
        ep = get_entity_path(ep_d)
        if ep is None:
            added += 1
            ep = add_entity_path(ep_d)
        else:
            updated += 1
            update_entity_path(ep, ep_d)
        db.session.add(ep)
    db.session.commit()
    return added, updated
#-- update_entities_paths
