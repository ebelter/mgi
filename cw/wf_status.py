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
    server = cw.server.server_factory()
    status = server.status_for_workflow(workflow_id)
    if status is None:
        sys.stderr.write(f"Failed to get status for workflow {workflow_id} ... see above errors.\n")
        sys.exit(1)
    if wf is not None:
        wf.status = status
        db.session.add(wf)
        db.session.commit()
    sys.stdout.write(f"{status}\n")
#-- status_cmd
