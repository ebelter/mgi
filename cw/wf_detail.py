import click, collections, sys, tabulate
from datetime import datetime, timedelta

from cw import db
from cw.model_helpers import get_wf
import cw.server

@click.command(short_help="get details of a workflow")
@click.argument("workflow-id", required=True, nargs=1)
def detail_cmd(workflow_id):
    """
    Get Detailed Status of a Workflow

    Give workflow id or cromwell workflow id (wf_id) to get display detailed status.

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
    (status, detail) = detailed_status(server, wf)
    if status is None:
        print(f"{detail}")
        sys.exit(1)
    if wf.status != status:
        wf.status = status
        db.session.add(wf)
        db.session.commit()
    sys.stdout.write(f"{detail}\n")
#-- detail_cmd

def detailed_status(server, wf):
    known_statuses = ["aborted", "done", "running", "preempted", "failed"]
    tasks, failed_calls = [], []
    now = datetime.now()
    md = server.metadata_for_workflow(wf.wf_id)
    if md is None:
        return (None, f"Failed to get metadata for {wf.wf_id}")
    total_time_elapsed = timedelta(seconds=0)
    for task_name, calls in md["calls"].items():
        time_elapsed = timedelta(seconds=0)
        call_statuses = collections.defaultdict(lambda: 0)
        for call in calls:
            # 2023-01-25T03:52:44.028Z
            start = datetime.strptime(call["start"], "%Y-%m-%dT%H:%M:%S.%fZ")
            if "end" in call:
                end = datetime.strptime(call["end"], "%Y-%m-%dT%H:%M:%S.%fZ")
                time_elapsed += end - start
            else:
                pass
                #end = now
            #time_elapsed += end - start
            call_statuses[call["executionStatus"].lower()] += 1
            if call["executionStatus"] == "Failed": # accumulate failed calls for investigation
                if "subWorkflowMetadata" in call:
                    pass #failed_calls.append(f"{call['subWorkflowMetadata']['workflowName']} {call['subWorkflowMetadata']['stdout']}")
                else:
                    pass #failed_calls.append(f"{call['workflowName']} {call['stdout']}")
        task = [task_name, str(time_elapsed).split(".")[0]]
        for status in known_statuses:
            task.append(call_statuses[status])
        tasks.append(task)
        total_time_elapsed += time_elapsed
    detail = f"""ID:       {md['id']}
Status:   {md['status']}
Name:     {wf.name}
Inputs:   {wf.inputs}
Pipeline: {wf.pipeline.name}
Time:     {str(total_time_elapsed)}
"""
    detail += tabulate.tabulate(tasks, headers=["task", "time"]+known_statuses, tablefmt="plain")
    if len(failed_calls) > 0:
        detail += "\nFailed calls:\n"+"\n".join(failed_calls)
    return (md["status"].lower(), detail)
#-- detailed_status
