import click, os, sys, yaml

from cw.conf import CromwellConf

@click.command(short_help="setup cromwell")
def setup_cmd():
    """
    Setup Cromwell

    Run this command without the YAML file to print the configuration to file <cw.yaml> to fill out and save. Then rerun this command with the completed YAML file to create directories and files.
    """
    cc = CromwellConf.safe_load()
    if not cc.is_validated:
        cc._attrs["CROMWELL_DIR"] = os.getcwd()
        cc.save()
        sys.stderr.write(f"Saved YAML configuration to <{cc.yaml_fn()}>. Fill out all attributes, then rerun this command.\n")
        sys.exit(0)
    sys.stdout.write("Setup cromwell: making directories, scripts, and configuration.\n")
    cc.setup()
#-- setup_cmd
