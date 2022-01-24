import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """
    MGI Sample Management and Tools
    """
    pass

from mgi.pipelines.cli import pl_cli
cli.add_command(pl_cli, name="pl")

from mgi.samples.cli import samples_cli
cli.add_command(samples_cli, name="samples")

from mgi.refs.cli import refs_cli
cli.add_command(refs_cli, name="refs")

from mgi.utils import utils_cli
cli.add_command(utils_cli, name="utils")
