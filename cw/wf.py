import click, json, os, sys

import cw.server

#curl --connect-timeout 5 --max-time 10 -s http://compute1-exec-226.ris.wustl.edu:8888/api/workflows/v1/c808fe24-0edd-46c4-ba23-ff881725e297/status {"status":"Succeeded","id":"c808fe24-0edd-46c4-ba23-ff881725e297"}

@click.group()
def cli():
    pass

from cw.wf_status_cmd import status_cmd as cmd
cli.add_command(cmd, name="status")

from cw.wf_metadata_cmd import metadata_cmd as cmd
cli.add_command(cmd, name="metadata")
