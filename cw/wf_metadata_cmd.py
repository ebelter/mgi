import click, json, os, sys

import cw.server

@click.command(short_help="get metadata of a workflow")
@click.argument("workflow-id", required=True, nargs=1)
def metadata_cmd(workflow_id):
    """
    Get Workflow Metadata
    """
    server = cw.server.server_factory()
    url = f"{server.url()}/api/workflows/v1/{workflow_id}/metadata?excludeKey=submittedFiles&expandSubWorkflows=true"
    response = server.query(url)
    if not response or not response.ok:
        sys.stderr.write(f"Failed to get response from server at {url}\n")
        return 3
    sys.stdout.write(f"{json.dumps(json.loads(response.content.decode()), indent=4)}")
