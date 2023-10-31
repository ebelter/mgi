import click, sys
from cig.metrics.helpers import OutHandle
from cig.metrics.seqlendist.obj import SeqLenDist
from cig.metrics.seqlendist.reports import write_csv_report, write_text_report, write_plot_report

@click.command()
@click.argument("seqfiles", required=True, nargs=-1)
@click.option("--output", "-o", default="-", help="dirname/basename to use when outputing reports")
@click.option("--reports", "-r", default=["text"], multiple=True, help="reports to generate: csv, text, plot")
@click.option("--distbin", "-b", default="lr", help="Numerical binning to report: asm or lr, see above")
def seqlendist_cmd(seqfiles, output, reports, distbin):
    """
    Generate Length Distributuion Reports from Seqfiles

    \b
    Known seqfiles: fasta [gz], fastq [gz]
    \b
    Reports available:
    text - general output from a template
    csv  - output data as CSV, suitable for loading into a spreadsheet
    plot - plot of sequence lengths

    \b
    Bins
    asm - assembly bins
      1M+
      250K-1M
      100K-250K
      10K-100K
      5K-10K
      2K-5K
      1-2K
    lr - long read bins
      20001+
      10001-20000
      5001-10000
      2001-5000
      1001-2000
      501-1000
      201-500
      1-200
    """
    if "plot" in reports and output == "-":
        sys.stderr.write("ERROR Cannot output dist plot to STDOUT, plaease specify a value for '--output'.\n")
        sys.exit(2)

    sld = SeqLenDist(distbin)
    for seqfile in seqfiles:
        sys.stderr.write(f"Processing seqfile: {seqfile}\n")
        sld.load(seqfile)
    sld.complete()
    if "text" in reports:
        with OutHandle(output, ext="txt", mode="w") as out_h:
            sys.stderr.write(f"Writing TEXT report: {out_h.fn}\n")
            text_report = write_text_report(out_h.fh, sld)
    if "csv" in reports:
        with OutHandle(output, ext="csv", mode="w") as out_h:
            sys.stderr.write(f"Writing CSV report: {out_h.fn}\n")
            csv_report = write_csv_report(out_h.fh, sld)
    if "plot" in reports:
        with OutHandle(output, ext="png", mode="wb") as out_h:
            sys.stderr.write(f"Writing PLOT report: {out_h.fn}\n")
            write_plot_report(out_h.fh, sld)
#-- lendist_cmd

if __name__ == '__main__':
    seqlendist_cmd()
#-- __main__
