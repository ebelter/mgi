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
    try:
        metadata = metadata_for_wf(wf)
    except Exception as e:
        sys.stderr.write(f"Failed to get metdata workflow <{wf.wf_id}>: {e.args[0]}\n")
        sys.exit(1)
    sys.stdout.write(f"{json.dumps(metadata, indent=4)}")
#-- metadata_cmd

def metadata_for_wf(wf):
    server = cw.server.server_factory()
    if not server.is_running():
        raise Exception(f"Cromwell server is not running at <{server.url()}>")
    url = f"{server.url()}/api/workflows/v1/{wf.wf_id}/metadata?excludeKey=submittedFiles&expandSubWorkflows=true"
    response = server.query(url)
    if not response or not response.ok:
        raise Exception(f"Server error encountered getting metadata with <{url}>")
    return json.loads(response.content.decode())
#-- metadata_for_wf
