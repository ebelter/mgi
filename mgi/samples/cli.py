import click, sys

from mgi.entity.add import add_help, add_entities

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
