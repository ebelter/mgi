import click, os, sys, yaml

from cw.conf import CromwellConf

@click.command(short_help="setup cromwell")
def setup_cmd():
    """
    Setup Cromwell

    Give the YAML configuration as a file to setup cromwell.

    Run this command without the YAML file to print the configuration to fill out and save. Then rerun this command with the YAML file.
    """
    yaml_fn = CromwellConf.yaml_fn()
    if not os.path.exists(yaml_fn):
        with open(yaml_fn, "w") as f:
            f.write(yaml.dump(dict.fromkeys(CromwellConf.attribute_names())))
        sys.stderr.write(f"Saved YAML configuration to <{yaml_fn}>. Fill out all attributes, then rerun this command.\n")
        sys.exit(0)
    sys.stdout.write("Setup cromwell: making directories, scripts, and configuration.\n")
    cc = CromwellConf.from_yaml()
    cc.setup()
#-- setup_cmd
