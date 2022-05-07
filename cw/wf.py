import click, json, os, sys

import cw.server

#curl --connect-timeout 5 --max-time 10 -s http://compute1-exec-226.ris.wustl.edu:8888/api/workflows/v1/c808fe24-0edd-46c4-ba23-ff881725e297/status {"status":"Succeeded","id":"c808fe24-0edd-46c4-ba23-ff881725e297"}

@click.group()
def cli():
    pass

@click.command(short_help="get status of a workflow")
@click.argument("workflow-id", required=True, nargs=1)
def status_cmd(workflow_id):
    """
    Get Status of a Workflow
    """
    server = cw.server.server_factory()
    url = f"{server.url()}/api/workflows/v1/{workflow_id}/status"
    response = server.query(url)
    if not response or response.ok:
        sys.stderr.write("Failed to get response from server at {url}\n")
        return 3
    info = json.loads(response.content.decode())
    sys.stdout.write(f"Workflow ID: {info['id']}\n")
    sys.stdout.write(f"Status:      {info['status']}\n")
cli.add_command(status_cmd, name="status")
