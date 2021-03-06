import click, sys, tabulate

from mgi.entity.add import add_help, add_entities
from mgi.entity.list import list_help, list_entities
from mgi.entity.helpers import get_entity, paths_rdr_factory as rdr_factory
from mgi.models import db
from mgi.helpers import resolve_features

@click.group(help=add_help, short_help="work with refs")
def refs_cli():
    """
    Refs!
    """
    pass

@click.command(help=add_help, short_help="add refs into mgi")
@click.argument("names", required=True, nargs=-1)
def add_cmd(names):
    created, existed = add_entities(names=set(names), kind="ref")
    sys.stdout.write(f"Added {len(created)} of {len(created) - len(existing)}, with these {len(existed)} existing:\n{''.join(existed)}\n")
refs_cli.add_command(add_cmd, name="add")

@click.command(help=list_help, short_help="list references and features")
@click.argument("filter-by", nargs=-1)
def list_cmd(filter_by):
    known_features = ["name", "sets"]
    features = resolve_features(filter_by, known_features)
    features["kind"] = "reference"
    rows = list_entities(features)
    if rows:
        sys.stdout.write(tabulate.tabulate(rows, list(map(lambda s: s.upper(), known_features)), tablefmt="simple", numalign="left"))
    else:
        sys.stderr.write("No entities found for given fitlers.\n")
refs_cli.add_command(list_cmd, name="list")

@refs_cli.command(name="remove", short_help="remove refs")
@click.argument("names", required=True, nargs=-1)
def remove_cmd(names):
    """
    Remove Refs

    Give names, will remove.
    """
    removed = 0
    for name in names:
        e = get_entity(name=name, kind="ref")
        if e is not None:
            removed += 1
            db.session.delete(e)
    db.session.commit()
    sys.stdout.write(f"Done. Removed {removed} of {len(names)} refs, skipped {len(names)-removed} not found.\n")
#-- remove_cmd

@refs_cli.command(name="rename", short_help="rename a ref")
@click.argument("name", required=True, nargs=1)
@click.argument("new_name", required=True, nargs=1)
def rename_cmd(name, new_name):
    ref = get_entity(name=name, kind="ref")
    if ref is None:
        raise Exception(f"Failed to get ref for {name}")
    setattr(ref, "name", new_name)
    db.session.add(ref)
    db.session.commit()
    sys.stderr.write(f"Rename ref from {name} to {ref.name}\n")
#-- rename_cmd

@click.group(help=add_help, short_help="work with refs paths")
def refs_paths_cli():
    """
    Refs Paths!
    """
    pass
refs_cli.add_command(refs_paths_cli, name="paths")

from mgi.entity.path import update_help, update_entities_paths;
@refs_paths_cli.command(name="update", help=update_help, short_help="update ref paths")
@click.argument("tsv", nargs=1)
@click.argument("features", nargs=-1)
def refs_paths_update_cmd(tsv, features):
    features = resolve_features(features, known_features=["entity", "value", "checksum", "exists", "group", "kind"], boolean_features=["exists"])
    rdr = rdr_factory(tsv)
    added, updated = update_entities_paths(rdr=rdr, features=features, entity_kind="ref", create_entities=True)
    sys.stdout.write(f"Done. Added {added} and updated {updated} of {added+updated} given paths.\n")
#-- refs_paths_update_cmd
