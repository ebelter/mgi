import click, os, sys, tabulate, yaml

from cw import db, Pipeline
from cw.model_helpers import resolve_features, pipeline_features, get_pipeline

@click.group()
def cli():
    "Commands for Pipelines"
    pass

from cw.pipelines.add import cmd as add_cmd
cli.add_command(add_cmd, name="add")

from cw.pipelines.inputs import inputs_cmd
cli.add_command(inputs_cmd, name="inputs")

@click.command(short_help="show detailed pipeline info")
@click.argument("pipeline_id", required=True, nargs=1)
def detail_cmd(pipeline_id):
    """
    Pipelines Detail

    Show all the files for a pipeline. Give pipeline name or id.

    """
    pipeline = get_pipeline(pipeline_id)
    if pipeline is None:
        sys.stderr.write(f"Failed to get pipeline for {pipeline_id}")
    else:
        sys.stdout.write(f"Name:     {pipeline.name}\nID:       {pipeline.id}\nWDL:      {pipeline.wdl}\nImports:  {pipeline.imports}\nInputs:   {pipeline.inputs}\nOutputs:  {pipeline.outputs}\n")
cli.add_command(detail_cmd, name="detail")

@click.command(short_help="list pipelines")
def list_cmd():
    """
    Pipelines List

    List all pipelines and their WDLs. Use the detail command to see all the files for a pipeline.

    """
    pipelines = Pipeline.query.all()
    if len(pipelines) == 0:
        sys.stderr.write(f"No pipelines found in pipleines db")
        return
    rows = []
    for p in pipelines:
        rows.append([p.name, p.wdl])
    print(tabulate.tabulate(rows, ["NAME", "WDL"], tablefmt="simple"))
cli.add_command(list_cmd, name="list")

known_features = pipeline_features()
rows = list(map(lambda k: [k, known_features[k]["desc"]], known_features.keys())) 
update_pipeline_help = f"""
Update a Pipeline

\b
Give a pipeline and features as key=value pairs to update.

\b
Pipeline features:
{tabulate.tabulate(rows,tablefmt='plain')}
"""
@click.command(help=update_pipeline_help, short_help="update a pipeline")
@click.argument("identifier", required=True, nargs=1)
@click.argument("features", required=True, nargs=-1)
def update_cmd(identifier, features):
    p = get_pipeline(identifier)
    if p is None:
        sys.stderr.write(f"Failed to get pipeline for <{identifier}>")
        sys.exit(1)
    features = resolve_features(features, known_features)
    rows = []
    for k, v in features.items():
        rows.append([k, getattr(p, k), v])
        setattr(p, k, v)
    db.session.add(p)
    db.session.commit()
    print(f"Update pipeline <{identifier}>\n{tabulate.tabulate(rows, ['ATTR', 'FROM', 'TO'], tablefmt='simple')}")
cli.add_command(update_cmd, name="update")

from cw.pipelines.validate import validate_cmd
cli.add_command(validate_cmd, name="validate")
