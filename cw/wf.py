import click, sys, tabulate
from cw import db, Workflow
from cw.model_helpers import get_wf, get_pipeline, resolve_features, wf_features, wf_features_help

#curl --connect-timeout 5 --max-time 10 -s http://compute1-exec-226.ris.wustl.edu:8888/api/workflows/v1/c808fe24-0edd-46c4-ba23-ff881725e297/status {"status":"Succeeded","id":"c808fe24-0edd-46c4-ba23-ff881725e297"}

@click.group()
def cli():
    pass

add_help = f"""
Add a Workflow:w

\b
Give workflow features as key=value pairs.

\b
Workflow features:
{tabulate.tabulate(wf_features_help(),tablefmt='plain')}
"""
@click.command(short_help="add a workflow", help=add_help)
@click.argument("features", required=True, nargs=-1)
def add_cmd(features):
    features = resolve_features(features, wf_features())
    if "pipeline" not in features:
        sys.stderr.write("[ERROR] Missing pipeline to create workflow")
        return
    pipeline = get_pipeline(features.pop("pipeline"))
    if not pipeline:
        sys.stderr.write("[ERROR] Could not create workflow, failed to get pipeline for <{features['pipeline']}>")
        return
    features["pipeline_id"] = pipeline.id
    wf = Workflow(**features)
    db.session.add(wf)
    db.session.commit()
    print(f"Add workflow {wf.id} {wf.wf_id} {wf.name} {wf.status} {wf.pipeline.name}")
cli.add_command(add_cmd, name="add")

@click.command(short_help="list workflows")
def list_cmd():
    """
    List Workflows
    """
    workflows = Workflow.query.all()
    if len(workflows) == 0:
        sys.stderr.write(f"No workflows found in db")
        return
    rows = []
    for w in workflows:
        rows.append([w.wf_id, w.name, w.status, w.pipeline.name])
    print(tabulate.tabulate(rows, ["WF_ID" , "NAME", "STATUS", "PIPELINE"], tablefmt="simple"))
cli.add_command(list_cmd, name="list")

from cw.wf_metadata_cmd import metadata_cmd as cmd
cli.add_command(cmd, name="metadata")

from cw.wf_status_cmd import status_cmd as cmd
cli.add_command(cmd, name="status")

from cw.wf_submit_cmd import submit_cmd as cmd
cli.add_command(cmd, name="submit")

update_help = f"""
Update a Workflow

\b
Give a workflow id/name/wf_id and features as key=value pairs to update.

\b
Workflow features:
{tabulate.tabulate(wf_features_help(),tablefmt='plain')}
"""
@click.command(help=update_help, short_help="update a workflow")
@click.argument("identifier", required=True, nargs=1)
@click.argument("features", required=True, nargs=-1)
def update_cmd(identifier, features):
    obj = get_wf(identifier)
    if obj is None:
        sys.stderr.write(f"Failed to get workflow for <{identifier}>")
        sys.exit(1)
    features = resolve_features(features, wf_features())
    if "pipeline" in features:
        p = get_pipeline(features["pipeline"])
        if p is None:
            sys.stderr.write(f"Failed to get pipeline for <{identifier}>")
            sys.exit(1)
        features["pipeline"] = p
    rows = []
    for k, v in features.items():
        rows.append([k, getattr(obj, k), v])
        setattr(obj, k, v)
    db.session.add(obj)
    db.session.commit()
    print(f"Update workflow <{identifier}>\n{tabulate.tabulate(rows, ['ATTR', 'FROM', 'TO'], tablefmt='simple')}")
cli.add_command(update_cmd, name="update")
