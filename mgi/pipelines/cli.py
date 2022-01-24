import click
from mgi.pipelines import encode_hic

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
def pl_cli():
    """
    Pipelines Info and Tools
    """
    pass

@pl_cli.group(name="encode-hic", help="work with samples")
def encode_hic_cli():
    """
    ENCODE HiC Pipeline
    """
    pass
#pl_cli.add_command(encode_hic_cli, name="enocode_hic")

@encode_hic_cli.command(name="benchmarks", short_help="generate benchmark tables and histograms")
@click.argument("files", nargs=-1)
@click.option("--report", help="Report to generate: table, hisotgrams")
def benchmarks(files, report):
    """
    ENCODE HiC Benchmarks
    """
    table = encode_hic.get_benchmarks_table(files[0])
    print(table)
#--
