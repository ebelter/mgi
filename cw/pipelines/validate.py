import click, os, subprocess, sys

from cw.model_helpers import get_pipeline

@click.command(short_help="submit a workflow")
@click.argument("name", required=True, nargs=1)
@click.argument("pipeline_identifier", required=True, nargs=1)
@click.option("--inputs", "-i", required=False, help="Filled out inputs JSON")
def validate_cmd(name, pipeline_identifier, inputs):
    """
    Validate Pipeline and Inputs

    \b
    Give:
    pipeline_identifier  pipeline name/id

    Optionally give:
    inputs_json          inputs json

    WOMTOOL will validate the pipeline WDL with the inputs, if given.
    """
    pipeline = get_pipeline(pipeline_identifier)
    if pipeline is None:
        sys.stderr.write(f"Failed to find pipeline for <{pipeline_identifier}>!\n")
        sys.exit(1)
    if inputs is not None and not os.path.exists(inputs):
        sys.stderr.write(f"Inputs JSO file <{inputs_json}> does not exist!\n")
        sys.exit(1)
    sys.stdout.write(f"Pipeline:    {pipeline.name}\n")
    #sys.stdout.write(f"Inputs json: {inputs_json}\n")
    output = validate_pipeline(pipeline, inputs_json)
    sys.stdout.write(f"{output.decode()}")
#-- submit_cmd

def validate_pipeline(pipeline, inputs_json=None):
    cmd = ["java", "-jar", "/apps/cromwell/womtool.jar", "validate", pipeline.wdl]
    if inputs is not None:
        cmd += ["-i", inputs]
    if pipeline.imports: # unzip the imports to the temp dir
        prev_dn = os.getcwd()
        temp_d = tempfile.TemporaryDirectory()
        os.chdir(temp_d.name)
        subprocess.check_call(["unzip", pipeline.imports])
        output = subprocess.check_output(cmd)
        os.chdir(prev_dn)
        temp_d.cleanup()
    else:
        output = subprocess.check_output(cmd)
    return output
#-- validate_pipeline
