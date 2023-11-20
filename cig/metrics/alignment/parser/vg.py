import re
from cig.metrics.helpers import str_to_number

def parse(f):
    metrics = {}
    total_p = re.compile(r"^Total ")
    parens_p = re.compile(r" \(.*$")
    for l in f:
        k, v = l.rstrip().split(": ")
        k = re.sub(total_p, "", k)
        k = re.sub(parens_p, "", k)
        k = k.lower()
        if "events" in v:
            metrics.update(parse_events(k, v))
        elif "," in v:
            v = re.sub(parens_p, "", v)
            metrics.update(parse_multi(k, v))
        elif "second" in v:
            metrics[k] = str_to_number(re.sub(r" (reads\/)?seconds?", "", v))
        elif " " in v:
            metrics[k] = v
        else:
            metrics[k] = str_to_number(v)
    # % mapped
    metrics["unaligned"] = int((metrics["alignments"]) - int(metrics["aligned"]))
    metrics["aligned pct"] = round((int(metrics["aligned"]) * 100 )/ int(metrics["alignments"]), 2)
    metrics["paired pct"] = round((int(metrics["properly paired"]) * 100 )/ int(metrics["aligned"]), 2)
    return metrics
#-- parse

def parse_events(k, v):
    snv_p = re.compile(r"(\d+) bp in (\d+) read")
    m = re.search(snv_p, v)
    return {
            " ".join([k, "bp"]): str_to_number(m.group(1)),
            " ".join([k, "events"]): str_to_number(m.group(2))
    }
#-- parse_events

def parse_multi(k, v):
    m = {}
    for n in v.split(", "):
        tokens = n.split(" ")
        m[" ".join([k, tokens[0].lower()])] = str_to_number(tokens[1])
    return m
#-- parse_multi
