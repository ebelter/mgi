import click, os, re, subprocess, sys, time, yaml

from cw.conf import CromwellConf

@click.command(short_help="Start a cromwell server")
@click.argument("yaml-file", type=str, required=True, nargs=1)
def server_cmd(yaml_file):
    """
    Start a Cromwell Server on LSF

    Give the configuration YAML file, the server script (server/start) will be executed. This command will wait for the job to start, then update the configuration YAML wit hthe host oname of the cromwell server.
    """
    # load yaml
    # check setup
    # start server
    # wait for host
    with open(yaml_file, "r") as f:
        cw_attrs = yaml.safe_load(f)
    cc = CromwellConf(cw_attrs)

    job_id = start_server(cc)
    sys.stdout.write(f"Waiting for job <{job_id}> to start to obtain HOST...\n")

    host = wait_for_host(job_id)
    sys.stdout.write(f"Server running on <{host}> port <{cw_attrs['CROMWELL_PORT']}>\n")

    cw_attrs["CROMWELL_JOB_ID"] = job_id
    cw_attrs["CROMWELL_HOST"] = host
    cw_attrs["CROMWELL_URL"] = f"{cw_attrs['CROMWELL_HOST']}:{cw_attrs['CROMWELL_PORT']}\n"
    sys.stdout.write(f"Updating YAML file <{yaml_file}>\n")
    with open(yaml_file, "w") as f:
        f.write(yaml.dump(cw_attrs))

    sys.stdout.write("Server ready!\n")
#-- server_cmd

def start_server(cc):
    # Launch server, return lsf job id
    server_start_fn = cc.server_start_fn
    output = subprocess.check_output([server_start_fn])
    found = re.match(r"\AJob <(\d+)> is submitted to queue <(.+)>", output.decode("UTF-8"))
    if not found:
        raise Exception(f"Failed to parse LSF bsub command output to get job id: {output}")
    return found.group(1)
#-- start_server

def wait_for_host(job_id):
    cmd = ["bjobs", "-w", job_id]
    tries = 0
    host = None
    while tries < 6:
        tries += 1
        output = subprocess.check_output(cmd)
        lines = output.decode('UTF-8').splitlines()
        tokens = lines[1].split()
        # STATUS 2 <> HOST 5
        if tokens[2] == "RUN":
            host = tokens[5]
            break
        elif tokens[2] == "DONE" or tokens[2] == "EXIT":
            raise Exception(f"Seems server <{job_id}> IS DONE/EXIT. Fix and try again!")
        time.sleep(5)
    if host is None:
        raise Exception(f"Seems server job is not starting. Fix and try again.")
    return host
#--
