import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """
    MGI Sample Management and Tools
    """
    pass

from mgi.utils import utils_cli
cli.add_command(utils_cli, name="utils")
