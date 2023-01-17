import click, os, subprocess, time, sys

from cw import db, Workflow
from cw.model_helpers import get_pipeline
import  cw.server

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
    sys.stdout.write(f"{output.decode()}")
    wf_id = resolve_wf_id_from_submit_output(output)
    sys.stdout.write(f"Workflow {wf_id} submitted, waiting for it to start...\n")
    status = wait_for_workflow_to_start(wf_id)
    wf = Workflow(name=name, wf_id=wf_id, status=status, pipeline=pipeline, inputs=inputs_json)
    db.session.add(wf)
    db.session.commit()
    sys.stdout.write(f"Workflow status: {status}\n")
    if status == "running":
        sys.stdout.write("Workflow is running and saved DB!\n")
    elif status == "failed":
        sys.stdout.write("Workflow failed to start. Please verify by checking server logs in <server/log>. Typically failures are due to misconfiguration of inputs or missing files.\n")
    else:
        sys.stdout.write(f"Workflow has been submitted, but has not started running. Please verify if it is running with the command 'cw wf status {wf_id}', or the server logs in <server/log>.\n")
#-- submit_cmd

def submit_wf(pipeline, inputs_json):
    wdl = pipeline.wdl
    if not os.path.exists(wdl):
        sys.stdout.write(f"Pipeline {pipeline.name} WDL {wdl} does not exist!\n")
        return
    server = cw.server.server_factory()
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

def wait_for_workflow_to_start(wf_id):
    server = cw.server.server_factory()
    cnt = 0
    status = "unknown"
    time.sleep(3)
    while cnt < 20:
        status = server.status_for_workflow(wf_id)
        if status != "submitted":
            break
        time.sleep(1)
        cnt += 1
    return status
#-- wait_for_workflow_to_start
