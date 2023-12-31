import click

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """
    Metrics Scripts and Helpers
    """
    pass

from cig.metrics.alignment.cmd import alignment_cmd
cli.add_command(alignment_cmd, "alignment")

from cig.metrics.hic.cmd import hic_cmd
cli.add_command(hic_cmd, "hic")

from cig.metrics.rnaseq.cmd import rnaseq_cmd
cli.add_command(rnaseq_cmd, "rnaseq")

from cig.metrics.seqlendist.cmd import seqlendist_cmd
cli.add_command(seqlendist_cmd, "seqlendist")
