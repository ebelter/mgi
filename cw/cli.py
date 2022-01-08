import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """
    Cromwell on MGI Compute
    """
    pass

from cw.cprint_cmd import cprint_cmd
cli.add_command(cprint_cmd, "cprint")

from cw.setup_cmd import setup_cmd
cli.add_command(setup_cmd, "setup")
