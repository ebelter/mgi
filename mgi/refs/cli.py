import click, sys

from mgi.entity.add import add_help, add_entities

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
