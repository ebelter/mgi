import click, os
from collections import defaultdict
from mgi.pipelines import hic

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.group(context_settings=CONTEXT_SETTINGS)
def pl_cli():
    """
    Pipelines Info and Tools
    """
    pass

# histograms by metric grouped by sample
# histograms, tables by sample(s)

# CLI Helpers
def resolve_samples(samples_and_dns):
    samples = []
    for sample_and_dns in samples_and_dns:
        group = []
        tokens = sample_and_dns.split(":")
        if len(tokens) == 2:
            label = tokens[0]
        elif len(tokens) == 3:
            label = tokens[1]
        else:
            raise Exception(f"")
        dn = os.path.abspath(tokens[-1])
        sample = {
                "name": tokens[0],
                "label": label,
                "dn": dn,
                "stats_fn": os.path.join(dn, "stats_1.json")}
        sample["stats"] = hic.load_stats(sample["stats_fn"])
        samples.append(sample)
    return samples
#--

def group_samples_by_name(samples):
    groups = defaultdict(lambda: [])
    for sample in samples:
        groups[sample["name"]].append(sample)
    return groups
#--

# HiC
@pl_cli.group(name="hic", help="hic pipelines helpers")
def hic_cli():
    """
    HiC Pipelines
    """
    pass
#--

reports_available = ["ch", "table",]
@hic_cli.command(name="benchmarks", short_help="")
@click.argument("samples", nargs=-1)
@click.option("--output", "-o", default=".", help="Output directory to write files.")
@click.option("--reports", "-r", default=reports_available[0], show_default=True,
        help="Comma separated report to run: {' '.join(reports_available}",
        callback=lambda ctx, param, value: value.split(","),
        )
def benchmarks_cmd(samples, output, reports):
    """
    ENCODE HiC Benchmarks

    \b
    Give a list of samples and directory names. Put colons between a sample and directories to compare. Note some reports vary in the required smaple and directories expected.

    Sample directory format examples:

    Sample with on run
    sample1.b38:/data/sample1.b38

    Sample with2 runs:
    sample1:/data/sample1.b38:/data/sample1.chm13

    Reports
    ch        Runs grouped per sample, with alignment and hic benchmarks plots
    detail    Benchmarks metrics by sample
    table     Text table of benchmarks

    """
    samples = resolve_samples(sorted(samples))
    groups = group_samples_by_name(samples)
    output_dn = os.path.abspath(output)
    if "ch" in reports:
        hic.create_benchmarks_comparative_histograms(groups, output_dn)
    if "detail" in reports:
        for sample in samples:
            hic.create_benchmarks_detail_histogram(sample, output_dn)
    if "table" in reports:
        print(hic.get_benchmarks_table(samples))
#--
