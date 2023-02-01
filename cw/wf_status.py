import click, json, os, sys

from cw import db
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
    status = server.status_for_workflow(workflow_id)
    if status is None:
        sys.stderr.write(f"Failed to get status for workflow {workflow_id} ... see above errors.\n")
        sys.exit(1)
    update_status(wf, status)
    sys.stdout.write(f"{status}\n")
#-- status_cmd

def update_status(wf, status):
    if wf is not None and wf.status != status:
        wf.status = status
        db.session.add(wf)
        db.session.commit()
#-- update_status
