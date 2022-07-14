import click, os, re, requests, subprocess, sys, time, yaml

from cw import appcon
import cw.cromshell

def server_factory():
    host = appcon.get(group="server", name="host")
    port = appcon.get(group="server", name="port")
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
        if response is False:
            return False
        return response.ok

    def query(self, url):
        # Response ok status_code reason json content
        try:
            response = requests.get(url)
        except:
            return False
        return response

    def status_for_workflow(self, wf_id):
        url = f"{self.url()}/api/workflows/v1/{wf_id}/status"
        response = self.query(url)
        if not response or not response.ok:
            sys.stderr.write(f"Failed to get response from server at {url}\n")
            return None
       # info = json.loads(response.content.decode())
        info = response.json()
        return info.get("status", "unknown").lower()
    #-- status_for_workflow
#-- Server

@click.group()
def cli():
    pass

from cw.heartbeat_cmd import heartbeat_cmd as cmd
cli.add_command(cmd, "heartbeat")

@click.command(short_help="Start a cromwell server")
def start_cmd():
    """
    Start a Cromwell Server on LSF

     This command will the run server script (server/start), then wait for the job to start and update the configuration YAML (cw.yaml) with the host name of the cromwell server.
    """
    server = server_factory()
    if server.is_running():
        sys.stdout.write(f"Server is already up and running at <{server.url}>\n")
        sys.exit(0)

    job_id = start_server()
    sys.stdout.write(f"Waiting for job <{job_id}> to start to obtain HOST...\n")

    host = wait_for_host(job_id)
    port = appcon.get(group="server", name="port")
    sys.stdout.write(f"Server running on <{host}> port <{port}>\n")

    #2022-07-07 17:07:03,041 cromwell-system-akka.dispatchers.engine-dispatcher-4 INFO  - Cromwell 60 service started on 0.0.0.0:8888...


    url = appcon.set(group="server", name="job_id", value=job_id)
    url = appcon.set(group="server", name="host", value=host)
    url = f"http://{host}:{port}"
    url = appcon.set(group="server", name="url", value=url)
    sys.stdout.write(f"Updating application configuration...\n")
    rv, msg = cw.cromshell.update_server(url)
    sys.stderr.write(msg)
    sys.stdout.write("Server ready!\n")
cli.add_command(start_cmd, name="start")

def start_server():
    # Launch server, return lsf job id
    server_start_fn = appcon.get(group="server", name="server_start_fn")
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
    job_id = appcon.get(group="server", name="job_id")
    if job_id is None:
        sys.stdout.write(f"No job id found in configuration, cannot stop server\n")
        return
    url = appcon.get(group="server", name="url")
    sys.stdout.write(f"Server URL: <{url}>\n")
    sys.stdout.write(f"Stopping job <{job_id}>\n")
    cmd = ["bkill", job_id]
    subprocess.call(cmd)
    sys.stdout.write(f"Updating application configuration...\n")
    url = appcon.set(group="server", name="job_id", value=None)
    url = appcon.set(group="server", name="host", value=None)
    url = appcon.set(group="server", name="url", value=None)
cli.add_command(stop_cmd, name="stop")
