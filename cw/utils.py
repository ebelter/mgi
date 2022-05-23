import click, sys

from cw.setup_cmd import server_conf_content

@click.group()
def cli():
    """
    Marginally Useful Tools
    """
    pass

@click.command(short_help="print the cromwell server config")
def printc_cmd():
    """
    Print Cromwell Config

    Requires configured DB with LSF parameters. Prints to STDOUT.
    """
    sys.stdout.write(server_conf_content())
cli.add_command(printc_cmd, name="printc")
