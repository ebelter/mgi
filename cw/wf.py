import click, json, os, sys

import cw.server

#curl --connect-timeout 5 --max-time 10 -s http://compute1-exec-226.ris.wustl.edu:8888/api/workflows/v1/c808fe24-0edd-46c4-ba23-ff881725e297/status {"status":"Succeeded","id":"c808fe24-0edd-46c4-ba23-ff881725e297"}

@click.group()
def cli():
    pass

import click, os, sys, tabulate, yaml
from cw.conf import CromwellConf
from cw.db import connect, db, Workflow
import cw.db

@click.command(short_help="add a workflow")
@click.argument("wf_id", required=True, nargs=1)
@click.argument("name", required=True, nargs=1)
@click.option("status", "-s", default="new", required=False, nargs=1)
@click.option("pipeline","-p", default=0, required=False, nargs=1)
def add_cmd(wf_id, name, status, pipeline):
    """
    Add Workflow

    Give workflow id, name, status, and pipeline. Optionally give the status and pipeline.
    """
    db = connect()
    wf = Workflow(wf_id=wf_id, name=name, status=status, pipeline_id=pipeline)
    db.session.add(wf)
    db.session.commit()
    print(f"Add workflow {id} {name} {status} {pipeline}")
cli.add_command(add_cmd, name="add")

@click.command(short_help="list workflows")
def list_cmd():
    """
    List Workflows
    """
    db = connect()
    workflows = Workflow.query.all()
    if len(workflows) == 0:
        sys.stderr.write(f"No workflows found in db")
        return
    rows = []
    for w in workflows:
        rows.append([w.wf_id, w.name, w.status, w.pipeline_id])
    print(tabulate.tabulate(rows, ["WF_ID" , "NAME", "STATUS", "PIPELINE"], tablefmt="simple"))
cli.add_command(list_cmd, name="list")

from cw.wf_status_cmd import status_cmd as cmd
cli.add_command(cmd, name="status")

from cw.wf_metadata_cmd import metadata_cmd as cmd
cli.add_command(cmd, name="metadata")
