import click, os, sys, yaml

from cw.conf import CromwellConf
from cw import appcon, create_db

@click.command(short_help="setup cromwell")
@click.argument("configs", required=True, nargs=-1)
def setup_cmd(configs):
    """
    Setup Cromwell

    \b
    Give configurations as name=value pairs

    \b
    Required configurations for LSF:
     docker_volumes
     job_group
     queue
     user_group
    """
    cc = CromwellConf.safe_load()
    sys.stdout.write("Setup cromwell: making directories, scripts, and configuration.\n")
    extra_configs = resolve_additional_configs(configs)
    for name in appcon.known_directories:
        os.makedirs(appcon.dn_for(name), exist_ok=True)
    create_db(extra_configs=extra_configs)
    cc.write_server_files()
#-- setup_cmd

def resolve_additional_configs(configs):
    required_configs = set(["docker_volumes", "job_group", "queue", "user_group"])
    seen_configs = set()
    extra_configs = []
    for config in configs:
        n, v = config.split("=")
        seen_configs.add(n)
        extra_configs.append(["lsf", f"lsf_{n}".upper(), v])
    missing_configs = required_configs - seen_configs
    if len(missing_configs) > 0:
        raise Exception(f"Missing these configurations: {' '.join(missing_configs)}\nPlease add them to the command arguments as name=value pairs.")
    return extra_configs
#--
