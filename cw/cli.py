import click, os, requests, subprocess, sys

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """
    Cromwell on MGI Compute
    """
    pass

from cw.pipelines.cli import cli as pipelines_cli
cli.add_command(pipelines_cli, "pipelines")

from cw.server import cli as server_cli
cli.add_command(server_cli, "server")

from cw.setup_cmd import setup_cmd as cmd
cli.add_command(cmd, "setup")

from cw.wf_cli import cli as wf_cli
cli.add_command(wf_cli, "wf")

from cw.utils import cli as utils_cli
cli.add_command(utils_cli, "utils")
