import click, json, os, sys

from cw.model_helpers import get_wf
import cw.server

@click.command(short_help="get status of a workflow")
@click.argument("workflow-id", required=True, nargs=1)
def status_cmd(workflow_id):
    """
    Get Status of a Workflow

    Give workflow id, cromwell workflow id, or name to get status.
    """
    wf = get_wf(workflow_id)
    if wf is not None:
        workflow_id = wf.wf_id
    server = cw.server.server_factory()
    url = f"{server.url()}/api/workflows/v1/{workflow_id}/status"
    #sys.stdout.write(f"URL: {url}\n")
    response = server.query(url)
    if not response or not response.ok:
        sys.stderr.write(f"Failed to get response from server at {url}\n")
        return 3
    info = json.loads(response.content.decode())
    sys.stdout.write(f"Workflow ID: {info['id']}\n")
    sys.stdout.write(f"Status:      {info['status']}\n")