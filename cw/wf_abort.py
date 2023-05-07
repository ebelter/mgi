import click, sys

from cw import db
from cw.model_helpers import get_wf
import cw.server

@click.command(short_help="stop a workflow")
@click.argument("workflow-id", required=True, nargs=1)
def abort_cmd(workflow_id):
    """
    Abort a Workflow

    Give workflow id or cromwell workflow id to abort (stop) a workflow.

    """
    wf = get_wf(workflow_id)
    if wf is None:
        print(f"Failed to get workflow for {workflow_id}")
        sys.exit(1)
    else:
        workflow_id = wf.wf_id
    server = cw.server.server_factory()
    if not server.is_running():
        sys.stderr.write(f"Cannot abort workflow because the cromwell server is not running.\n")
    result = server.abort_workflow(workflow_id)
    if result is None:
        sys.stderr.write(f"Failed to abort workflow {workflow_id} ... see above errors.\n")
        sys.exit(1)
    sys.stdout.write(f"{result}\n")
#-- abort_cmd
