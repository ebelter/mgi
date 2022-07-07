import click, json, os, sys

from cw import db
from cw.model_helpers import get_wf
import cw.server

@click.command(short_help="get status of a workflow")
@click.argument("workflow-id", required=True, nargs=1)
@click.option("--update", "-u", is_flag=True, required=False, default=False, help="If workflow is in the DB, updarte its status there.")
def status_cmd(workflow_id, update):
    """
    Get Status of a Workflow

    Give workflow id, cromwell workflow id, or name to get status.

    Add --update to change the status in the database.
    """
    wf = get_wf(workflow_id)
    if wf is not None:
        workflow_id = wf.wf_id
    status = status_for_wf_id(workflow_id)
    if wf is not None:
        wf.status = status
        db.session.add(wf)
        db.session.commit()
    sys.stdout.write(f"Workflow ID: {workflow_id}\n")
    sys.stdout.write(f"Status:      {status}\n")
#-- status_cmd

def status_for_wf_id(wf_id):
    server = cw.server.server_factory()
    url = f"{server.url()}/api/workflows/v1/{wf_id}/status"
    response = server.query(url)
    if not response or not response.ok:
        sys.stderr.write(f"Failed to get response from server at {url}\n")
        sys.exit(1)
    info = json.loads(response.content.decode())
    return info.get("status", "unknown").lower()
#-- status_for_wf_id
