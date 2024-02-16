import click, sys
from cig.metrics.helpers import OutHandle, resolve_labels
import cig.metrics.factory, cig.metrics.collate.reports

@click.command()
@click.argument("statsfiles", required=True, nargs=-1)
@click.option("--kind", "-k", required=True, help=f"The kind of files to collate. Known kinds: {', '.join(cig.metrics.factory.known_kinds())}")
@click.option("--labels", "-l", help="Labels for multiple statsfiles to group and evaluate together. Give one per seqfile, in order, separated by commas.")
@click.option("--out", "-o", default="-", help="Dirname/basename to use when outputing reports.")
@click.option("--reports", "-r", type=click.Choice(cig.metrics.collate.reports.available_reports()), default=["table"], multiple=True, help=f"reports to generate: {','.join(cig.metrics.collate.reports.available_reports())}.")
def collate_cmd(kind, statsfiles, labels, out, reports):
    """
    Collate and Generate Reports from Statsfiles

    \b
    Reports available:
    csv  - suitable for loading into a spreadsheet
    json - JSON
    text - tabulate formatted table
    yaml - YAML
    """
    try:
        labels = resolve_labels(labels, statsfiles, out)
    except Exception as e:
        sys.stderr.write(f"{e}\n")
        sys.exit(2)

    m = cig.metrics.factory.build(kind)
    for i, statsfile in enumerate(statsfiles):
        sys.stderr.write(f"Processing seqfile: {statsfile}\n")
        m.load(labels[i], statsfile)
    for report_type in reports:
        report_writer_name = f"write_{report_type}_report"
        writer = getattr(cig.metrics.collate.reports, report_writer_name)
        with OutHandle(out, ext=report_type) as out_h:
            sys.stderr.write(f"Writing {report_type.upper()} report: {out_h.fn}\n")
            writer(out_h.fh, m)
#-- lendist_cmd
