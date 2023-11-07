import click, os, sys
from cig.metrics.helpers import OutHandle
from cig.metrics.seqlendist.obj import SeqLenDist
from cig.metrics.seqlendist.reports import write_csv_report, write_text_report, write_plot_report

@click.command()
@click.argument("seqfiles", required=True, nargs=-1)
@click.option("--distbin", "-b", default="lr", help="Numerical binning to report: asm or lr, see above.")
@click.option("--labels", "-l", help="Labels for multiple seqfiles to group and evaluate together. Give one per seqfile, in order, separated by commas.")
@click.option("--out", "-o", default="-", help="Dirname/basename to use when outputing reports.")
@click.option("--reports", "-r", default=["text"], multiple=True, help="reports to generate: csv, text, plot.")
def seqlendist_cmd(seqfiles, labels, out, reports, distbin):
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
    try:
        labels = resolve_labels(labels, seqfiles, out)
    except Exception as e:
        sys.stderr.write(f"{e}\n")
        sys.exit(2)
    if "plot" in reports and out == "-":
        sys.stderr.write("ERROR Cannot output dist plot to STDOUT, plaease specify a value for '--out'.\n")
        sys.exit(2)

    sld = SeqLenDist(distbin)
    for i, seqfile in enumerate(seqfiles):
        sys.stderr.write(f"Processing seqfile: {seqfile}\n")
        sld.load(seqfile, labels[i])
    sld.complete()
    if "text" in reports:
        with OutHandle(out, ext="txt", mode="w") as out_h:
            sys.stderr.write(f"Writing TEXT report: {out_h.fn}\n")
            text_report = write_text_report(out_h.fh, sld)
    if "csv" in reports:
        with OutHandle(out, ext="csv", mode="w") as out_h:
            sys.stderr.write(f"Writing CSV report: {out_h.fn}\n")
            csv_report = write_csv_report(out_h.fh, sld)
    if "plot" in reports:
        with OutHandle(out, ext="png", mode="wb") as out_h:
            sys.stderr.write(f"Writing PLOT report: {out_h.fn}\n")
            write_plot_report(out_h.fh, sld)
#-- lendist_cmd

def resolve_labels(labels, seqfiles, out):
    if labels is None:
        if out is not None:
            label = os.path.basename(out)
            return [out for i in range(0, len(seqfiles))]
        else:
            return list(map(lambda sf: os.path.basename(sf).split(".")[0], seqfiles))

    labels = labels.split(",")
    if len(labels) != len(seqfiles):
        raise Exception(f"ERROR Unequal number of labels {len(labels)} => {labels}) given for seqfiles: {len(seqfiles)}")
        #return [labels[0] for i in range(0, len(seqfiles))]
    return labels
#-- resolve_labels

if __name__ == '__main__':
    seqlendist_cmd()
#-- __main__
