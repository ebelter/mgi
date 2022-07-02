import click, os, subprocess, sys

from cw import db, Workflow
from cw.model_helpers import get_pipeline
from cw.server import server_factory

@click.command(short_help="submit a workflow")
@click.argument("name", required=True, nargs=1)
@click.argument("pipeline_identifier", required=True, nargs=1)
@click.argument("inputs_json", required=True, nargs=1)
def submit_cmd(name, pipeline_identifier, inputs_json):
    """
    Submit a Workflow

    \b
    Give:
    name  workflow name for reference
    pipeline_identifier  pipeline name/id
    inputs_json          pipeline inputs json

    Workflow id and name will be saved to the database.
    """
    #if not force:
    #    verify_duplicate_wfs_not_running(name)
    pipeline = get_pipeline(pipeline_identifier)
    if pipeline is None:
        sys.stderr.write(f"Failed to find pipeline for <{pipeline_identifier}>!\n")
        sys.exit(1)
    if not os.path.exists(inputs_json):
        sys.stderr.write(f"Inputs json <{inputs_json}> does not exists!\n")
        sys.exit(1)
    sys.stdout.write(f"Pipeline:    {pipeline.name}\n")
    sys.stdout.write(f"Inputs json: {inputs_json}\n")
    output = submit_wf(pipeline, inputs_json)
    sys.stdout.write(f"{output}")
    wf_id = resolve_wf_id_from_submit_output(output)
    sys.stdout.write(f"Workflow ID: {wf_id}\n")
    wf = Workflow(name=name, wf_id=wf_id, status="new", pipeline=pipeline)
    db.session.add(wf)
    db.session.commit()
    sys.stdout.write("Workflow submitted and added to the database\n")
#-- submit_cmd

def verify_duplicate_wfs_not_running(wf_name):
    wfs = Workflow.query.filter(Workflow.name == name).all()
    if len(wfs) == 0:
        return
    for wf in wfs:
        status = get_wf_startus(wf)
        if status in ["New", "Running"]:
            sys.stderr.write(f"Found running workflow: {wf.wf_id}\n")
            sys.exit(1)
        if status in ["Succeeded"]:
            sys.stderr.write(f"Found succeeded workflow: {wf.wf_id}\n")
            sys.exit(1)
#-- verify_duplicate_wfs_not_running

def get_wf_status(wf_id):
    server = cw.server.server_factory()
    url = f"{server.url()}/api/workflows/v1/{workflow_id}/status"
    sys.stdout.write(f"URL: {url}\n")
    response = server.query(url)
    if not response or not response.ok:
        return None
    info = json.loads(response.content.decode())
    return info["status"]
#-- get_wf_status()

def submit_wf(pipeline, inputs_json):
    wdl = pipeline.wdl
    if not os.path.exists(wdl):
        sys.stdout.write(f"Pipeline {pipeline.name} WDL {wdl} does not exist!\n")
        return
    server = server_factory()
    if not server.is_running():
        sys.stdout.write(f"Cromwell server is not running or misconfigured.\n")
        return
    cmd = ["java", "-jar", "/apps/cromwell/cromwell.jar", "submit", pipeline.wdl, "-i", inputs_json, "--host", server.url()]
    if pipeline.imports is not None:
        cmd += ["--imports", pipeline.imports]
    return subprocess.check_output(cmd)
#-- submit_wf

def resolve_wf_id_from_submit_output(output):
    #[2022-05-18 10:56:51,19] [info] Slf4jLogger started
    #[2022-05-18 10:56:52,14] [info] Workflow e933af86-b64c-43b2-abcc-1241e8d7e69a submitted to http://compute1-exec-226.ris.wustl.edu:8888
    for l in output.decode().split("\n"):
        tokens = l.split(" ")
        if tokens[3] == "Workflow":
            return tokens[4]
            break
#-- resolve_wf_id_from_submit_output
