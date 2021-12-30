import click

from mgi.models import db, Entity

update_help = """
    Add Entites Into MGI

    \b
    Add via command line:

    Give comma separated names and features as name=value pairs.

    NAME1 F1=V1 F2=V2 ...

    NAME1,NAME2 F1=V1 F2=V2 ...


    Add via TSV:
    
    Give a TSV file of with columns and one entity per row. Column 'name' is required.

    NAME\tF1\tF2
    NAME1\tV1\tV2
    NAME2\tV3\tV4

    """

def update_entities(entities, features):
    for entity in entities:
        for f in features:
            

            if k == "name":
                setattr(entity, name, v)
            else:
                ef = get_entity_feature(entity, k)
                if ef is None:
                    ef = create_entity_feature()
        db.session.add(entity)
    db.session.commit()
#-- update_entities
