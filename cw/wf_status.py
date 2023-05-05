import click, sys

from cw import db
from cw.model_helpers import get_wf
import cw.server

@click.command(short_help="get status of a workflow")
@click.argument("workflow-id", required=True, nargs=1)
def status_cmd(workflow_id):
    """
    Get Status of a Workflow

    Give workflow id or cromwell workflow id to get status.

    """
    wf = get_wf(workflow_id)
    if wf is None:
        print(f"Failed to get workflow for {workflow_id}")
        sys.exit(1)
    else:
        workflow_id = wf.wf_id
    server = cw.server.server_factory()
    if not server.is_running():
        sys.stderr.write(f"Cannot get status for workflow because the cromwell server is not running.\n")
    status = server.status_for_workflow(workflow_id)
    if status is None:
        sys.stderr.write(f"Failed to get status for workflow {workflow_id} ... see above errors.\n")
        sys.exit(1)
    if wf is not None and wf.status != status:
        wf.status = status
        db.session.add(wf)
        db.session.commit()
    sys.stdout.write(f"{status}\n")
#-- status_cmd
