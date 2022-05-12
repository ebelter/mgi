import click, os, requests, subprocess, sys

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """
    Cromwell on MGI Compute
    """
    pass

from cw.heartbeat_cmd import heartbeat_cmd as cmd
cli.add_command(cmd, "heartbeat")

from cw.outputs_cmd import outputs_cmd as cmd
cli.add_command(cmd, "outputs")

from cw.pipelines import cli as pipelines_cli
cli.add_command(pipelines_cli, "pipelines")

from cw.printc_cmd import printc_cmd as cmd
cli.add_command(cmd, "printc")

from cw.server import cli as server_cli
cli.add_command(server_cli, "server")

from cw.setup_cmd import setup_cmd as cmd
cli.add_command(cmd, "setup")

from cw.wf import cli as wf_cli
cli.add_command(wf_cli, "wf")
