import click, requests, sys

from cw import appcon

@click.command(name="heartbeat", short_help="Check if the cromwell server is running")
def heartbeat_cmd():
    """
    Check the Cromwell Server

    Give the configuration YAML file, the server script (server/start) will be executed. This command will wait for the job to start, then update the configuration YAML wit hthe host oname of the cromwell server.

    CROMWELL_HOST and CROMWELL_PORT must be set in the YAML configuration.
    """
    host = appcon.get(group="server", name="host")
    if host is None:
        sys.stderr.write("Can't find server 'host' in application configuration.\n")
        sys.exit(1)

    port = appcon.get(group="server", name="port")
    if port is None:
        sys.stderr.write("Can't find server 'port' in application configuration.\n")
        sys.exit(1)
    url = f"http://{host}:{port}/engine/v1/version"
    sys.stdout.write(f"Checking host <{host}> listening on <{port}> ...\n")
    sys.stdout.write(f"URL: {url}\n")
    response = requests.get(url)
    if not response.ok:
        sys.stderr.write(f"No response from {url}. Correct server? Is cromwell running?\n")
        sys.exit(1)
    sys.stdout.write(f"Cromwell server is up and running! Response: {response.content}\n")
#-- cw_heartbeat_cmd
