import click, os, requests, subprocess, sys

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """
    Cromwell on MGI Compute
    """
    pass

@cli.command(name="heartbeat", short_help="Check if the cromwell server is running")
@click.argument("server", required=False, nargs=1)
def cw_heartbeat_cmd(server):
    """
    Give VM name and port
    """
    if server is None:
        cromwell_server_environ_key = "CROMWELL_SERVER"
        os.environ.get(cromwell_server_environ_key, None)
        if server is None:
            sys.stderr.write(f"No server given or found in environment '{cromwell_server_environ_key}' variable.\n")
            sys.exit(1)
    url = f"http://{server}/engine/v1/version"
    response = requests.get(url)
    if not response.ok:
        sys.stderr.write("No response from {server}. Correct server? Is cromwell running?")
        sys.exit(1)
    sys.stdout.write(f"Cromwell server is up and running version {response.content}.\n")
#-- cw_heartbeat_cmd

from cw.printc_cmd import printc_cmd as cmd
cli.add_command(cmd, "printc")

@cli.command(name="server", short_help="Start a cromwell server")
@click.option("--local", is_flag=True, required=False, default=False, help="Run a cromwell server locally in the background")
def server_cmd(local):
    """
    Start a Cromwell Server

    Run distributed cromwell server. The file that is run is 'cromwell/server/start'

    If running a local server in the background, the file is 'cromwell/server/run'
    """
    if local:
        bn = "run"
    else:
        bn = "start"
    fn =os.path.join("cromwell", "server", bn)
    if not os.path.exists(fn):
        sys.stderr.write(f"Can not find cromwell server {fn} to run. Have you setup up cromwell?")
        sys.exit(1)
    sys.stderr.write(f"RUNNING: {fn}\n")
    subprocess.call([fn])
#-- server_cmd

from cw.setup_cmd import setup_cmd as cmd
cli.add_command(cmd, "setup")
