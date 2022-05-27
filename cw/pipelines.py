import click, os, sys, tabulate, yaml

from cw import db, Pipeline
from cw.model_helpers import resolve_features, pipeline_features

@click.group()
def cli():
    pass

known_features = pipeline_features()
rows = list(map(lambda k: [k, known_features[k]["desc"]], known_features.keys())) 
add_pipeline_help = f"""
Add a Pipeline

\b
Give pipeline features as key=value pairs.

\b
Pipeline features:
{tabulate.tabulate(rows,tablefmt='plain')}
"""
@click.command(help=add_pipeline_help, short_help="add a pipeline")
@click.argument("features", required=True, nargs=-1)
def add_cmd(features):
    features = resolve_features(features, known_features)
    if "name" not in features.keys():
        raise Exception(f"FAILED to add pipeline: 'name' is required\n")
    if "wdl" not in features.keys():
        raise Exception(f"FAILED to add pipeline: 'wdl' is required\n")
    if not os.path.exists(features["wdl"]):
        raise Exception(f"FAILED to add pipeline: WDL file <{features['wdl']}> does not exist\n")
    if "imports" in features.keys() is not None and not os.path.exists(features["imports"]):
        raise Exception(f"FAILED to add pipeline: Imports file <{features['imports']}> does not exist\n")
    if "outputs"in features.keys() is not None and not os.path.exists(features["outputs"]):
        raise Exception(f"FAILED to add pipeline: Outputs file <{features['outputs']}> does not exist\n")
    p = Pipeline(**features)
    db.session.add(p)
    db.session.commit()
    print(f"Add pipeline {p.name} {p.wdl} {p.imports} {p.outputs}")
cli.add_command(add_cmd, name="add")

@click.command(short_help="list pipelines")
def list_cmd():
    """
    List Pipelines
    """
    pipelines = Pipeline.query.all()
    if len(pipelines) == 0:
        sys.stderr.write(f"No pipelines found in pipleines db")
        return
    rows = []
    for p in pipelines:
        rows.append([p.name, p.wdl, p.imports])
    print(tabulate.tabulate(rows, ["NAME", "WDL", "IMPORTS"], tablefmt="simple"))
cli.add_command(list_cmd, name="list")
