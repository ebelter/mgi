import click, sys

from cw.setup_cmd import server_conf_content, server_run_content, server_start_content

@click.group()
def cli():
    """
    Marginally Useful Tools
    """
    pass


@click.command(short_help="print a server resource file")
@click.argument("name", required=True, type=click.Choice(["conf", "start", "run"]), nargs=1)
def printr_cmd(name):
    """
    Print Cromwell Server Resource File

    Print out the server configurtation applied file content to STDOUT.
    """
    fun = globals()[f"server_{name}_content"]
    sys.stdout.write(fun())
cli.add_command(printr_cmd, name="printr")
