import click, os, sys, tabulate
from cw import db, Pipeline
from cw.model_helpers import pipeline_features, resolve_features

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
def cmd(features):
    features = resolve_features(features, known_features)
    if "name" not in features.keys():
        raise Exception(f"FAILED to add pipeline: 'name' is required\n")
    if "wdl" not in features.keys():
        raise Exception(f"FAILED to add pipeline: 'wdl' is required\n")
    if "imports" in features.keys() is not None and not os.path.exists(features["imports"]):
        raise Exception(f"FAILED to add pipeline: Imports file <{features['imports']}> does not exist\n")
    if "outputs"in features.keys() is not None and not os.path.exists(features["outputs"]):
        raise Exception(f"FAILED to add pipeline: Outputs file <{features['outputs']}> does not exist\n")
    pipeline = Pipeline(**features)
    db.session.add(pipeline)
    db.session.commit()
    sys.stdout.write(f"Name:     {pipeline.name}\nID:       {pipeline.id}\nWDL:      {pipeline.wdl}\nImports:  {pipeline.imports}\nInputs:   {pipeline.inputs}\nOutputs:  {pipeline.outputs}\n")
#-- cmd
