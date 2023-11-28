import click, sys
from cig.metrics.helpers import OutHandle, resolve_labels
from cig.metrics.rnaseq.obj import RnaSeqMetrics
import cig.metrics.rnaseq.reports as rna_reports

@click.command()
@click.argument("statsfiles", required=True, nargs=-1)
@click.option("--labels", "-l", help="Labels for multiple statsfiles to group and evaluate together. Give one per seqfile, in order, separated by commas.")
@click.option("--out", "-o", default="-", help="Dirname/basename to use when outputing reports.")
@click.option("--reports", "-r", type=click.Choice(rna_reports.available_reports()), default=["table"], multiple=True, help=f"reports to generate: {','.join(rna_reports.available_reports())}.")
def rnaseq_cmd(statsfiles, labels, out, reports):
    """
    Generate RNA Seq Reports from Statsfiles

    \b
    Known statsfiles: picard rna-seq
    \b
    Reports available:
    csv  - summary metrics as CSV, suitable for loading into a spreadsheet
    json - summary metrics as JSON
    text - tabulate formatted table
    yaml - summary metrics as YAML
    """
    try:
        labels = resolve_labels(labels, statsfiles, out)
    except Exception as e:
        sys.stderr.write(f"{e}\n")
        sys.exit(2)

    m = RnaSeqMetrics()
    for i, statsfile in enumerate(statsfiles):
        sys.stderr.write(f"Processing seqfile: {statsfile}\n")
        m.load(labels[i], statsfile)
    for report_type in reports:
        report_writer_name = f"write_report_{report_type}"
        writer = getattr(rna_reports, report_writer_name)
        with OutHandle(out, ext=report_type) as out_h:
            sys.stderr.write(f"Writing {report_type.upper()} report: {out_h.fn}\n")
            writer(out_h.fh, m)
#-- lendist_cmd
