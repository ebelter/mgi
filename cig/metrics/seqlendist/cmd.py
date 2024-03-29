import click, os, sys
from cig.metrics.helpers import OutHandle, resolve_labels
from cig.metrics.seqlendist.obj import SeqLenDist
import cig.metrics.seqlendist.reports as sld_reports

@click.command()
@click.argument("seqfiles", required=True, nargs=-1)
@click.option("--bins", "-b", default="lr", help="Numerical binning to report: asm or lr, see above.")
@click.option("--labels", "-l", help="Labels for multiple seqfiles to group and evaluate together. Give one per seqfile, in order, separated by commas.")
@click.option("--out", "-o", default="-", help="Dirname/basename to use when outputing reports.")
@click.option("--reports", "-r", type=click.Choice(sld_reports.available_reports()), multiple=True, help=f"reports to generate: {','.join(sld_reports.available_reports())}.")
def seqlendist_cmd(seqfiles, labels, out, reports, bins):
    """
    Generate Length Distribution Reports from Seqfiles

    \b
    Known seqfiles: fasta [gz], fastq [gz]

    \b
    Bins
    * asm - assembly bins
      1M+
      250K-1M
      100K-250K
      10K-100K
      5K-10K
      2K-5K
      1-2K
    * lr - long read bins
      20001+
      10001-20000
      5001-10000
      2001-5000
      1001-2000
      501-1000
      201-500
      1-200
    * comma separated list - "1" will always be added as first number
      1,50001,100001,1000001 => [1, 50001, 100001, 1000001]
    * colon separated limit and interval - "1" will be added to the limit
      2000:1000 => [1, 1001, 2001]
    """
    try:
        labels = resolve_labels(labels, seqfiles)
    except Exception as e:
        sys.stderr.write(f"{e}\n")
        sys.exit(2)
    if "png" in reports and out == "-":
        sys.stderr.write("ERROR Cannot output dist plot to STDOUT, plaease specify a value for '--out'.\n")
        sys.exit(2)

    sld = SeqLenDist(bins)
    for i, seqfile in enumerate(seqfiles):
        sys.stderr.write(f"Processing seqfile: {seqfile}\n")
        sld.load(seqfile, labels[i])
    sld.complete()
    for report_type in reports:
        report_writer_name = f"write_{report_type}_report"
        writer = getattr(sld_reports, report_writer_name)
        rformat = report_type
        if report_type.startswith("plot"):
            rformat = "png"
        out_n = ".".join([out, report_type])
        with OutHandle(out_n, ext=rformat) as out_h:
            sys.stderr.write(f"Writing {report_type.upper()} report: {out_h.fn}\n")
            writer(out_h.fh, sld)
#-- lendist_cmd

def resolve_labels(labels, seqfiles):
    if labels is None:
        labels = []
        for seqfile in seqfiles:
            #seqfile_tokens = os.path.basename(seqfile).split(".")
            labels.append(".".join([e for e in os.path.basename(seqfile).split(".") if e not in ("fasta", "fastq", "gz")]))
        #return list(map(lambda sf: os.path.basename(sf).split(".")[0], seqfiles))
        return labels

    labels = labels.split(",")
    if len(labels) != len(seqfiles):
        return [labels[0] for i in range(0, len(seqfiles))]
    return labels
#-- resolve_labels
