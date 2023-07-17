import click, os, re, sys, tabulate
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

\b
If these features were not specified, but exist as these file names, they will be included:
FEATURE   WDL FILE WITH EXT REPLACING ".wdl"
inputs    .inputs.json
outputs   .outputs.yaml
imports   .imports.zip
"""
@click.command(help=add_pipeline_help, short_help="add a pipeline")
@click.argument("features", required=True, nargs=-1)
def cmd(features):
    features = resolve_features(features, known_features)
    if "name" not in features.keys():
        raise Exception(f"FAILED to add pipeline: 'name' is required\n")
    if "wdl" not in features.keys():
        raise Exception(f"FAILED to add pipeline: 'wdl' is required\n")
    for k, v in (["inputs", "json"], ["outputs", "yaml"], ["imports", "zip"]):
        if k in features.keys() is not None:
            if not os.path.exists(features[k]):
                raise Exception(f"FAILED to add pipeline: Given {k} file <{features[k]}> does not exist\n")
        else:
            fn = re.sub(r".wdl$", ".".join(["", k, v]), features["wdl"])
            if os.path.exists(fn):
                features[k] = fn
    pipeline = Pipeline(**features)
    db.session.add(pipeline)
    db.session.commit()
    sys.stdout.write(f"Name:     {pipeline.name}\nID:       {pipeline.id}\nWDL:      {pipeline.wdl}\nInputs:   {pipeline.inputs}\nOutputs:  {pipeline.outputs}\nImports:  {pipeline.imports}\n")
#-- cmd
