import click, os, sys, tabulate, yaml
from cw.conf import CromwellConf
from cw.db import connect, db, Pipeline
import cw.db

@click.group()
def cli():
    pass

@click.command(short_help="add a pipeline")
@click.argument("name", required=True, nargs=1)
@click.argument("wdl", required=True, nargs=1)
@click.option("--imports", "-i", required=False, help="Imports zip file if needed to run pipeline")
def add_cmd(name, wdl, imports):
    """
    Add Pipeline

    Give pipeline name and WDL. Optionally add the imports zip file needed to run.
    """
    if not os.path.exists(wdl):
        raise Exception(f"FAILED to add pipeline: WDL file <{wdl}> does not exist.\n")
    if imports is not None and not os.path.exists(imports):
        raise Exception(f"FAILED to add pipeline: Imports file <{imports}> does not exist.\n")
    db = connect()
    p = Pipeline(name=name, wdl=wdl)
    db.session.add(p)
    db.session.commit()
    print(f"Add pipeline {name} {wdl} {imports}")
cli.add_command(add_cmd, name="add")

@click.command(short_help="list pipelines")
def list_cmd():
    """
    List Pipelines
    """
    db = connect()
    pipelines = Pipeline.query.all()
    if len(pipelines) == 0:
        sys.stderr.write(f"No pipelines found in pipleines db")
        return
    rows = []
    for p in pipelines:
        rows.append([p.name, p.wdl, p.imports])
    print(tabulate.tabulate(rows, ["NAME", "WDL", "IMPORTS"], tablefmt="simple"))
cli.add_command(list_cmd, name="list")
