import click, os, sys
from cig.metrics.helpers import OutHandle, resolve_labels
from cig.metrics.alignment.obj import AlignmentMetrics
import cig.metrics.alignment.reports as am_reports

@click.command()
@click.argument("statsfiles", required=True, nargs=-1)
@click.option("--labels", "-l", help="Labels for multiple statsfiles to group and evaluate together. Give one per seqfile, in order, separated by commas.")
@click.option("--out", "-o", default="-", help="Dirname/basename to use when outputing reports.")
@click.option("--reports", "-r", type=click.Choice(am_reports.available_report_types()), multiple=True, help=f"reports to generate: {','.join(am_reports.available_report_types())}.")
def alignment_cmd(statsfiles, labels, out, reports):
    """
    Generate Alignment Reports from Statsfiles
    \b
    Known statsfiles: samtools stat, vg stat
    \b
    Reports
    \b
    Give report type and format as colon separated pairs like "summary:csv". If not format is given, csv is the default.
    \b
    Reports Types:
    summary - normalized metrics
    \b
    Report Formats:
    csv  - CSV suitable for loading into a spreadsheet
    json - JSON
    mw   - mediawiki table
    png  - plot of ...
    text - tabulate formatted table
    yaml - YAML
    """
    try:
        labels = resolve_labels(labels, statsfiles, out)
    except Exception as e:
        sys.stderr.write(f"{e}\n")
        sys.exit(2)
    try:
        report_writers = resolve_reports(reports)
    except Exception as e:
        sys.stderr.write(f"{e}\n")
        sys.exit(2)

    am = AlignmentMetrics()
    for i, statsfile in enumerate(statsfiles):
        sys.stderr.write(f"Processing statsfile: {statsfile}\n")
        am.load(labels[i], statsfile)
    for report_type, report_format, writer in report_writers:
        with OutHandle(out, ext=report_format) as out_h:
            sys.stderr.write(f"Writing {report_type.upper()} report as {report_format.upper()} to {out_h.fn}\n")
            writer(out_h.fh, am)
#-- alignment_cmd

def resolve_reports(input_reports):
    reports = []
    for report in input_reports:
        if ":" in report:
            report_type, report_format = report.split(":")
        else:
            report_type = report
            report_format = "table"
        if report_type not in am_reports.available_report_types():
            raise Exception(f"Unknown report type ({report_type}) in given report: {report}")
        if report_format not in am_reports.available_report_formats():
            raise Exception(f"Unknown report format ({report_format}) in given report: {report}")
        writer = getattr(am_reports, "_".join(["write", report_type, "report", report_format]), None)
        if writer is None:
            raise Exception(f"Unknown report ({report}) given report: {report}")
        reports.append([report_type, report_format, writer])
    return reports
#-- resolve_reports
