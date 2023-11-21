import os, sys
from cig.metrics.helpers import str_to_number

def parse(f):
    metrics = {}
    for l in f:
        if l.startswith("SN"):
            m = parse_SN_line(l.rstrip())
            metrics.update(m)
        elif l.startswith("RL"):
            m = parse_RL_line(l.rstrip())
            metrics.update(m)
    return metrics
#-- parse

def parse_SN_line(l):
    sn, k, v, *c = l.split("\t")
    k = k.rstrip(":").replace(" (%)", "")#.replace(" ", "_")
    return {k: str_to_number(v)}
#-- parse_SN_line

# Read lengths. Use `grep ^RL | cut -f 2-` to extract this part. The columns are: read length, count
# RL  75  62943876
def parse_RL_line(l):
    rl, l, c = l.split("\t")
    return {"read length": str_to_number(l), "read count": str_to_number(c)}
#-- parse_RL_line
