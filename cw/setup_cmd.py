import click, jinja2, os, sys, yaml

from cw import appcon, create_db

@click.command(short_help="setup cromwell")
@click.argument("configs", required=True, nargs=-1)
@click.option("--env", is_flag=True, default=False, help="Attempt to get configs from enviroment. Not all required configs can be detected.")
def setup_cmd(configs, env):
    """
    Setup Cromwell

    \b
    Give configurations as name=value pairs

    \b
    Examples
     cw setup queue=general job_group=/user/default

    \b
    Required configurations for LSF:
     docker_volumes
     job_group
     queue
     user_group
    """
    sys.stdout.write("Setup cromwell: making directories, scripts, and configuration.\n")
    configs = resolve_configs(configs, env)
    for name in appcon.known_directories:
        os.makedirs(appcon.dn_for(name), exist_ok=True)
    create_db(extra_configs=configs)
    write_server_files()
#-- setup_cmd

def required_configs_for_lsf():
    return {
            "docker_volumes": "LSF_DOCKER_VOLUMES",
            "job_group": "LSB_JOBGROUP",
            "queue": "LSB_QUEUE",
            "user_group" : None,
            }
#-- required_configs_for_lsf

def resolve_configs(incoming_configs, env):
    seen_configs = set()
    configs = []
    # Parse the given configs
    for config in incoming_configs:
        n, v = config.split("=")
        seen_configs.add(n)
        configs.append(["lsf", n, v])
    # Which reqruied are missing?
    required_configs = required_configs_for_lsf()
    required_names = required_configs.keys()
    missing_configs = required_names - seen_configs
    # Try getting config from environment
    if env:
        for n in missing_configs:
            v = os.environ.get(required_configs[n], None)
            if v is not None:
                seen_configs.add(n)
                if n == "queue":
                    v = v.replace("-interactive", "")
                configs.append(["lsf", n, v])
    missing_configs = required_names - seen_configs
    if len(missing_configs) > 0:
        raise Exception(f"Missing these configurations: {' '.join(missing_configs)}\nPlease add them to the command arguments as name=value pairs.")
    return configs
#-- required_configs

def write_server_files():
    server_dn = appcon.get("server_dn")
    for name in ("conf", "run", "start"):
        fn = appcon.get(group="server", name=f"{name}_fn")
        fun = globals()[f"server_{name}_content"]
        with open(fn, "w") as f:
            f.write(fun())

def server_conf_content():
    with open(appcon.get(group="resources", name="conf_template_fn"), "r") as f:
        template = jinja2.Template(f.read())
    attrs = {
            "RUNS_DIR": appcon.get("runs_dn"),
            "DB_DIR": appcon.get("db_dn"),
            "LOGS_DIR": appcon.get("logs_dn"),
            "SERVER_PORT": appcon.get(group="server", name="port"),
            "LSF_DOCKER_VOLUMES": appcon.get(group="lsf", name="docker_volumes"),
            "LSF_JOB_GROUP": appcon.get(group="lsf", name="job_group"),
            "LSF_QUEUE": appcon.get(group="lsf", name="queue"),
            "LSF_USER_GROUP": appcon.get(group="lsf", name="user_group"),
            }
    return template.render(attrs)

def server_run_content():
    template_fn = appcon.get(group="resources", name="run_template_fn")
    attrs = {"SERVER_CONF_FN": appcon.get(group="server", name="conf_fn")}
    with open(template_fn, "r") as f:
        template = jinja2.Template(f.read())
    return template.render(**attrs)

def server_start_content():
    attrs = { # put in validating method
            "SERVER_PORT": appcon.get(group="server", name="port"),
            "SERVER_DN": appcon.dn_for("server"),
            #"SERVER_LOG_FN": appcon.get(group="server", name="log_fn"),
            #"SERVER_RUN_FN": appcon.get(group="server", name=run_fn"),
            "LSF_DOCKER_VOLUMES": appcon.get(group="lsf", name="docker_volumes"),
            "LSF_JOB_GROUP": appcon.get(group="lsf", name="job_group"),
            "LSF_QUEUE": appcon.get(group="lsf", name="queue"),
            "LSF_USER_GROUP": appcon.get(group="lsf", name="user_group"),
            }
    template_fn = appcon.get(group="resources", name="start_template_fn")
    with open(template_fn, "r") as f:
        template = jinja2.Template(f.read())
    return template.render(**attrs)
#-- write_server_files
