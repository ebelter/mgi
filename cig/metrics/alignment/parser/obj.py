from cig.metrics.alignment.parser.samtools import parse as samtools_parser
from cig.metrics.alignment.parser.vg import parse as vg_parser

class StatsfileParser(object):
    def __init__(self, statsfile):
        self.statsfile = statsfile
        self.kind, self.parser = get_parser(statsfile)

    def parse(self):
        with open(self.statsfile, "r") as f:
            return self.parser(f)
#-- StatsfileParser

def get_parser(statsfile):
    with open(statsfile, "r") as f:
        firstl = f.readline()
        if firstl.startswith("# This file was produced by samtools stats"):
            metrics_kind = "samtools_stat"
            return "samtools", samtools_parser
        elif firstl.startswith("Total alignments: "):
            metrics_kind = "vg_stat"
            return "vg", vg_parser
        else:
            raise Exception(f"Failed to determine stats file kind for {statsfile}")
#-- get_parser
