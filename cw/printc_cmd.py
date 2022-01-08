import click, jinja2, os, sys, yaml

from cw.conf import CromwellConf

@click.command(short_help="print the cromwell server config")
@click.argument("yaml-file", type=click.File('r'), nargs=1)
def printc_cmd(yaml_file):
    """
    Config Print [CPRINT]

    Given a filled in config YAML file, apply it to the cromwell configuration and print.
    """
    attrs = yaml.safe_load(yaml_file)
    cc = CromwellConf(attrs)
    sys.stdout.write(cc.server_conf())
#-- printc_cmd
