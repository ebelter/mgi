import click, jinja2, json, os, sys
from cw.model_helpers import get_pipeline
import cw.server

@click.command(short_help="render pipelien inputs")
@click.argument("identifier", required=True, nargs=1)
@click.argument("data", required=True, nargs=-1)
@click.option("--output", "-o", type=click.File('w'), required=True, help="Output file for rendered inputs.")
def inputs_cmd(identifier, data, output):
    """
    Render Pipeline Inputs

    \b 
    Apply data to a pipeline's inputs file and save. Inputs file musgt be a jinja2 template.

    \b
    Give the pipeline, input data (as ATTR=VALUE pairs), and output file name.

    \b
    Data examples, the ATTRS must be fields in the inputs file template.
    SAMPLE=HG002 REF=/storage1/fs1/hprc/Active/GCRh38
    """
    pl = get_pipeline(identifier)
    if pl is None:
        sys.stderr.write(f"Failed to get pipeline for <{identifier}>\n")
        sys.exit(1)
    inputs_fn = pl.inputs
    if inputs_fn is None:
        sys.stderr.write(f"Pipeline <{pl.id} {pl.name}> does not have inputs associated with it. Please use the update command to add an inputs file.\n")
        sys.exit(1)
    if not os.path.exists(inputs_fn):
        sys.stderr.write(f"Pipeline <{pl.id} {pl.name}> inputs file <{inputs_fn}> does not exist. Please use the update command to add an inputs file that exists.\n")
        sys.exit(1)
    data_d = {}
    for d in data:
        k, v = d.split("=", 1)
        data_d[k] = v
    with open(inputs_fn, "r") as f:
        inputs_template = jinja2.Template(f.read())
    output.write(inputs_template.render(data_d))
    sys.stderr.write(f"Wrote pipeline <{pl.name}> inputs to {output.name}\n")
#-- inputs_cmd
