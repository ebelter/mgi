import click, sys, tabulate

from mgi.entity.add import add_help, add_entities
from mgi.entity.list import list_help, list_entities
from mgi.entity.helpers import get_entity, paths_rdr_factory as rdr_factory
from mgi.models import db
from mgi.helpers import resolve_features

@click.group(short_help="work with samples")
def samples_cli():
    """
    Samples!
    """
    pass

@click.command(help=add_help, short_help="add samples into mgi")
@click.argument("names", required=True, nargs=-1)
def add_cmd(names):
    created, existed = add_entities(names=set(names), kind="sample")
    sys.stdout.write(f"Added {len(created)} of {len(created) - len(existing)}, with these {len(existed)} existing:\n{''.join(existed)}\n")
samples_cli.add_command(add_cmd, name="add")

@click.command(help=list_help, short_help="list samples and features")
@click.argument("filter-by", nargs=-1)
def list_cmd(filter_by):
    known_features = ["name", "sets"]
    features = resolve_features(filter_by, known_features)
    features["kind"] = "sample"
    rows = list_entities(features)
    if rows:
        sys.stdout.write(tabulate.tabulate(rows, list(map(lambda s: s.upper(), known_features)), tablefmt="simple", numalign="left"))
    else:
        sys.stderr.write("No entities found for given fitlers.\n")
samples_cli.add_command(list_cmd, name="list")

@samples_cli.command(name="remove", short_help="remove samples")
@click.argument("names", required=True, nargs=-1)
def remove_cmd(names):
    """
    Remove Samples

    Give names, will remove.
    """
    removed = 0
    for name in names:
        e = get_entity(name=name, kind="sample")
        if e is not None:
            removed += 1
            db.session.delete(e)
    db.session.commit()
    sys.stdout.write(f"Done. Removed {removed} of {len(names)} samples, skipped {len(names)-removed} not found.\n")
#-- remove_cmd

@samples_cli.command(name="rename", short_help="rename a sample")
@click.argument("name", required=True, nargs=1)
@click.argument("new_name", required=True, nargs=1)
def rename_cmd(name, new_name):
    sample = get_entity(name=name, kind="sample")
    if sample is None:
        raise Exception(f"Failed to get sample for {name}")
    setattr(sample, "name", new_name)
    db.session.add(sample)
    db.session.commit()
    sys.stderr.write(f"Rename sample from {name} to {sample.name}\n")
#-- rename_cmd

@click.group(help=add_help, short_help="work with samples paths")
def samples_paths_cli():
    """
    Samples Paths!
    """
    pass
samples_cli.add_command(samples_paths_cli, name="paths")

from mgi.entity.path import update_help, update_entities_paths;
@samples_paths_cli.command(name="update", help=update_help, short_help="update samples paths")
@click.argument("tsv", nargs=1)
@click.argument("features", nargs=-1)
def samples_paths_update_cmd(tsv, features):
    features = resolve_features(features, known_features=["entity", "value", "checksum", "exists", "group", "kind"], boolean_features=["exists"])
    rdr = rdr_factory(tsv)
    added, updated = update_entities_paths(rdr=rdr, features=features, entity_kind="ref", create_entities=True)
    sys.stdout.write(f"Done. Added {added} and updated {updated} of {added+updated} given paths.\n")
#-- samples_paths_update_cmd
