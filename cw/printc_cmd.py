import click, jinja2, os, sys, yaml

from cw import appcon
from cw.setup_cmd import server_conf_content

@click.command(short_help="print the cromwell server config")
def printc_cmd():
    """
    Print Cromwell Config

    Requires configured DB with LSF parameters. Prints to STDOUT.
    """
    sys.stdout.write(server_conf_content())
#-- printc_cmd
