import click, json, os, sys
from cw.model_helpers import get_wf
import cw.server

@click.command(short_help="get metadata of a workflow")
@click.argument("identifier", required=True, nargs=1)
def metadata_cmd(identifier):
    """
    Get Workflow Metadata

    Give workflow cromwell id, name, or local db id.

    Use 'list' command to see workflow, adn 'add' command to add workflows to the local db.
    """
    wf = get_wf(identifier)
    if wf is None:
        sys.stderr.write(f"Failed to get workflow for <{identifier}>\n")
        sys.exit(1)
    server = cw.server.server_factory()
    if not server.is_running():
        sys.stderr.write("Cromwell server is not running\n")
        sys.exit(1)
    try:
        metadata = server.metadata_for_wf(wf)
    except Exception as e:
        sys.stderr.write(f"Failed to get metdata workflow <{wf.wf_id}>: {e.args[0]}\n")
        sys.exit(1)
    sys.stdout.write(f"{json.dumps(metadata, indent=4)}")
#-- metadata_cmd
