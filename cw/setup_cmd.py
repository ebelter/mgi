import click, jinja2, os, sys, yaml

from cw import appcon, create_db

@click.command(short_help="setup cromwell")
@click.argument("configs", required=True, nargs=-1)
def setup_cmd(configs):
    """
    Setup Cromwell

    \b
    Give configurations as name=value pairs

    \b
    Examples
     cw setup queue=general

    \b
    Required configurations for LSF:
     docker_volumes
     job_group
     queue
     user_group
    """
    sys.stdout.write("Setup cromwell: making directories, scripts, and configuration.\n")
    extra_configs = resolve_additional_configs(configs)
    for name in appcon.known_directories:
        os.makedirs(appcon.dn_for(name), exist_ok=True)
    create_db(extra_configs=extra_configs)
    write_server_files()
#-- setup_cmd

def resolve_additional_configs(configs):
    required_configs = set(["docker_volumes", "job_group", "queue", "user_group"])
    seen_configs = set()
    extra_configs = []
    for config in configs:
        n, v = config.split("=")
        seen_configs.add(n)
        extra_configs.append(["lsf", n, v])
    missing_configs = required_configs - seen_configs
    if len(missing_configs) > 0:
        raise Exception(f"Missing these configurations: {' '.join(missing_configs)}\nPlease add them to the command arguments as name=value pairs.")
    return extra_configs
#--

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
            "LSF_QUEUE": appcon.get(group="lsf", name="user_group"),
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
            "LSF_QUEUE": appcon.get(group="lsf", name="user_group"),
            "LSF_USER_GROUP": appcon.get(group="lsf", name="user_group"),
            }
    template_fn = appcon.get(group="resources", name="start_template_fn")
    with open(template_fn, "r") as f:
        template = jinja2.Template(f.read())
    return template.render(**attrs)
#-- write_server_files
