import click, sys

from mgi.models import Entity, EntitySet

list_help = """
    List Entities

    Give features as key=value pairs. If no features, all entities will be shown.
    """

def list_entities(features):
    eset_name = features.pop("sets", None)
    q = Entity.query.filter_by(**features)
    if eset_name is not None:
        eset = EntitySet.query.filter_by(name=eset_name).one_or_none()
        if eset is None:
            raise Exception(f"No entity set found for {eset_name}.")
        q = q.filter(Entity.sets.any(id=eset.id))
    rows = []
    for e in q:
        row = list(map(lambda a: getattr(e, a, None), ["name"]))
        row.insert(1, ",".join(map(lambda eset: eset.name, e.sets)))
        rows.append(row)
    return rows
#-- list_entities
