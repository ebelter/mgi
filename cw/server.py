import click, os, re, requests, subprocess, sys, time, yaml

from cw.conf import CromwellConf
import cw.cromshell

def server_factory():
    cc = CromwellConf.load()
    host = cc.getattr("CROMWELL_HOST")
    port = cc.getattr("CROMWELL_PORT")
    return Server(host, port)
#-- server_factory

class Server(object):
    def __init__(self, host=None, port="8888"):
        self.host = host
        self.port = port

    def url(self):
        if self.host is None:
            return None
        return f"http://{self.host}:{self.port}"

    def is_running(self):
        url = self.url()
        if url is None:
            return False
        response = self.query(url)
        return response.ok

    def query(self, url):
        try:
            response = requests.get(url)
        except:
            return False
        return response
#-- Server

@click.group()
def cli():
    pass

@click.command(short_help="Start a cromwell server")
def start_cmd():
    """
    Start a Cromwell Server on LSF

     This command will the run server script (server/start), then wait for the job to start and update the configuration YAML (cw.yaml) with the host name of the cromwell server.
    """
    cc = CromwellConf.load()
    server = server_factory()
    if server.is_running():
        sys.stdout.write(f"Server is already up and running at <{cc.getattr('CROMWELL_URL')}>\n")
        sys.exit(0)

    job_id = start_server(cc)
    sys.stdout.write(f"Waiting for job <{job_id}> to start to obtain HOST...\n")

    host = wait_for_host(job_id)
    port = cc.getattr('CROMWELL_PORT')
    sys.stdout.write(f"Server running on <{host}> port <{port}>\n")

    cc.setattr("CROMWELL_JOB_ID", job_id)
    cc.setattr("CROMWELL_HOST", host)
    url = f"http://{host}:{port}"
    cc.setattr("CROMWELL_URL", url)
    sys.stdout.write(f"Updating YAML file <{cc.yaml_fn()}>\n")
    cc.save()
    rv, msg = cw.cromshell.update_server(url)
    sys.stderr.write(msg)
    sys.stdout.write("Server ready!\n")
cli.add_command(start_cmd, name="start")

def start_server(cc):
    # Launch server, return lsf job id
    server_start_fn = cc.server_start_fn()
    if not os.path.exists(server_start_fn):
        raise Exception(f"Server start script [server_start_fn] not found. Has 'cw setup <YAMLFILE>' been run?")
    output = subprocess.check_output(["/bin/bash", server_start_fn])
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

@click.command(short_help="Stop the cromwell server")
def stop_cmd():
    """
    Stop the Cromwell Server
    """
    cc = CromwellConf.load()
    job_id = cc.getattr("CROMWELL_JOB_ID")
    if job_id is None:
        sys.stdout.write(f"No job id found in configuration, cannot stop server\n")
        return
    url = cc.getattr("CROMWELL_URL")
    sys.stdout.write(f"Server URL: <{url}>\n")
    sys.stdout.write(f"Stopping job <{job_id}>\n")
    cmd = ["bkill", job_id]
    subprocess.call(cmd)
    sys.stdout.write(f"Updating YAML file <cw.yaml>\n")
    url = cc.setattr("CROMWELL_JOB_ID", None)
    url = cc.setattr("CROMWELL_HOST", None)
    url = cc.setattr("CROMWELL_URL", None)
    cc.save()
cli.add_command(stop_cmd, name="stop")
