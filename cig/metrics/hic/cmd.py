import click, sys
from cig.metrics.helpers import OutHandle, resolve_labels
from cig.metrics.hic.obj import HiCMetrics
import cig.metrics.hic.reports as hic_reports

@click.command()
@click.argument("statsfiles", required=True, nargs=-1)
@click.option("--labels", "-l", help="Labels for multiple statsfiles to group and evaluate together. Give one per seqfile, in order, separated by commas.")
@click.option("--out", "-o", default="-", help="Dirname/basename to use when outputing reports.")
@click.option("--reports", "-r", type=click.Choice(hic_reports.available_reports()), default=["table"], multiple=True, help=f"reports to generate: {','.join(hic_reports.available_reports())}.")
def hic_cmd(statsfiles, labels, out, reports):
    """
    Collate Hi-C from Metrics

    \b
    Known statsfiles:
    JSON from ENCODE HiC Pipeline

    \b
    Reports available:
    csv   - summary metrics as CSV, suitable for loading into a spreadsheet
    mw    - mediawiki formatted table
    table - tabulate formatted table
    """
    try:
        labels = resolve_labels(labels, statsfiles, out)
    except Exception as e:
        sys.stderr.write(f"{e}\n")
        sys.exit(2)

    m = HiCMetrics()
    for i, statsfile in enumerate(statsfiles):
        sys.stderr.write(f"Processing seqfile: {statsfile}\n")
        m.load(labels[i], statsfile)
    for report_type in reports:
        report_writer_name = f"write_report_{report_type}"
        writer = getattr(hic_reports, report_writer_name)
        with OutHandle(out, ext=report_type) as out_h:
            sys.stderr.write(f"Writing {report_type.upper()} report: {out_h.fn}\n")
            writer(out_h.fh, m)
#-- hic_cmd
