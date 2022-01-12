import click, os, sys, yaml

from cw.conf import CromwellConf

@click.command(short_help="setup cromwell")
@click.argument("yaml-file", type=click.File('r'), required=False, nargs=1)
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
    print("Setup!")
    attrs = yaml.safe_load(yaml_file)
    cc = CromwellConf(attrs)
    print(f"Creating cromwell directory structure in {cc.cromwell_dn}")
    cc.makedirs()
    for ft in ("conf", "run", "start"):
        fun = getattr(cc, f"server_{ft}_content")
        with open(getattr(cc, f"server_{ft}_fn"), "w") as f:
            f.write(fun())
#-- setup_cmd
