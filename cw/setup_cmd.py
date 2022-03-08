import click, sys, yaml

from cw.conf import CromwellConf

@click.command(short_help="setup cromwell")
@click.argument("yaml-file", type=str, required=False, nargs=1)
def setup_cmd(yaml_file):
    """
    Setup Cromwell

    Give the YAML configuration as a file to setup cromwell.

    Run this command without the YAML file to print the configuration to fill out and save. Then rerun this command with the YAML file.
    """
    if not yaml_file:
        sys.stderr.write("Fill out and save the YAML configuration to a file. Then rerun this command.\n\n")
        sys.stdout.write(yaml.dump(dict.fromkeys(CromwellConf.attribute_names())))
        sys.exit(0)
    sys.stdout.write("Setup cromwell: making directories, scripts, and configuration.\n")
    cc = CromwellConf.from_yaml(yaml_file)
    cc.setup()
#-- setup_cmd
