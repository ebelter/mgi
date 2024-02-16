from cig.metrics.rnaseq.obj import RnaSeqMetrics
from cig.metrics.hic.obj import HiCMetrics

known_kinds_and_objs = {
        "rnaseq": RnaSeqMetrics,
        "hic": HiCMetrics,
        }
def known_kinds():
    return sorted(known_kinds_and_objs.keys())
#-- known_kinds

def build(kind):
    if kind not in known_kinds():
        raise Exception(f"Unknown kind to build metrics: {kind}")
    return known_kinds_and_objs[kind]()
#-- build
