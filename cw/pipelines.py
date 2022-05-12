import click, os, sys, tabulate, yaml

from cw.conf import CromwellConf

class PipelinesDb(object):
    def __init__(self, fn):
        self.fn = fn
        self.load()

    def load(self):
        with open(self.fn, "r") as f:
            self.db = yaml.safe_load(f)

    def save(self):
        with open(self.fn, "w") as f:
            yaml.dump(self.db, f)

    # pipelines
    def get_pipelines(self):
        pipelines = []
        for name, attrs in self.db["pipelines"].items():
            pipelines.append([name]+attrs)
        return pipelines.copy()

    def add_pipeline(self, name, attrs):
        # TODO
        #if attrs.get("wdl", None) is None:
        #    raise Exception("Need attribute <wdl> to add pipeline")
        #  check if wdl exists?
        #  check if pipeline exists?
        self.db["pipelines"][name] = attrs
        self.save()
        self.load()
    ##- pipelines

    # workflows
    def get_workflow(self, id):
        pass

    def get_workflows(self):
        pass

    def add_wolkflow(self, id, name):
        pass
    ##- workflows
#-- PipelinesDb

@click.group()
def cli():
    pass

@click.command(short_help="list pipelines")
@click.argument("name", required=True, nargs=1)
@click.argument("wdl", required=True, nargs=1)
@click.option("--imports", "-i", required=False, help="Imports zip file if needed to run pipeline")
def add_cmd(name, wdl, imports):
    """
    Add Pipeline

    Give pipeline name and WDL. Optionally add the imports zip file needed to run.
    """
    cc = CromwellConf.load()
    pfn = cc.server_pipelines_fn()
    pdb = PipelinesDb(fn=pfn)
    pdb.add_pipeline(name=name, attrs=[wdl, imports])
    print(f"Add pipeline {name} {wdl} {imports}")
cli.add_command(add_cmd, name="add")

@click.command(short_help="list pipelines")
def list_cmd():
    """
    List Pipelines
    """
    cc = CromwellConf.load()
    pfn = cc.server_pipelines_fn()
    pdb = PipelinesDb(fn=pfn)

    pipelines = pdb.get_pipelines()
    if len(pipelines) == 0:
        sys.stderr.write(f"No pipelines found in pipleines db <{pfn}>. Maybe try adding one.")
    print(tabulate.tabulate(pipelines, ["NAME", "WDL", "IMPORTS"], tablefmt="simple"))
cli.add_command(list_cmd, name="list")
