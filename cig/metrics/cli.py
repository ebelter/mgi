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

from cig.metrics.collate.cmd import collate_cmd
cli.add_command(collate_cmd, "collate")

from cig.metrics.seqlendist.cmd import seqlendist_cmd
cli.add_command(seqlendist_cmd, "seqlendist")
