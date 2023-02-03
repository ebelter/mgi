import click, collections, json, os, sys, tabulate
from datetime import datetime, timedelta

from cw import db
from cw.model_helpers import get_wf
import cw.server

@click.command(short_help="get status of a workflow")
@click.argument("workflow-id", required=True, nargs=1)
@click.option("--detailed", "-d", is_flag=True, required=False, default=False, help="Output detailed ststus including task status and run times.")
def status_cmd(workflow_id, detailed):
    """
    Get Status of a Workflow

    Give workflow id, cromwell workflow id, or name to get status.

    """
    wf = get_wf(workflow_id)
    if wf is not None:
        workflow_id = wf.wf_id
    server = cw.server.server_factory()
    if not server.is_running():
        sys.stderr.write(f"Cannot get status for workflow because the cromwell server is not running.\n")
    if detailed:
        (status, detail) = detailed_status(server, wf)
    else:
        status = server.status_for_workflow(workflow_id)
        detail = status
    if status is None:
        sys.stderr.write(f"Failed to get status for workflow {workflow_id} ... see above errors.\n")
        sys.exit(1)
    update_status(wf, status)
    sys.stdout.write(f"{detail}\n")
#-- status_cmd

def detailed_status(server, wf):
    known_statuses = ["done", "running", "preempted", "failed"]
    tasks = []
    now = datetime.now()
    md = server.metadata_for_workflow(wf.wf_id)
    for task_name, calls in md["calls"].items():
        time_elapsed = timedelta(seconds=0)
        call_statuses = collections.defaultdict(lambda: 0)
        for call in calls:
            # 2023-01-25T03:52:44.028Z
            start = datetime.strptime(call["start"], "%Y-%m-%dT%H:%M:%S.%fZ")
            if "end" in call:
                end = datetime.strptime(call["end"], "%Y-%m-%dT%H:%M:%S.%fZ")
            else:
                end = now
            time_elapsed += end - start
            call_statuses[call["executionStatus"].lower()] += 1
        task = [task_name, str(time_elapsed).split(".")[0]]
        for status in known_statuses:
            task.append(call_statuses[status])
        tasks.append(task)
    detail = f"""Workflow ID:      {md['id']}
Status:           {md['status']}
Workflow name:    {wf.name}
Workflow inputs:  {wf.inputs}
Workflow name:
Tasks:
"""
    detail += tabulate.tabulate(tasks, headers=["name", "time"]+known_statuses, tablefmt="plain")
    return (md["status"].lower(), detail)
#-- detailed_status

def update_status(wf, status):
    if wf is not None and wf.status != status:
        wf.status = status
        db.session.add(wf)
        db.session.commit()
#-- update_status
