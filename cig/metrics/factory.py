from cig.metrics.hic.obj import HiCMetrics
from cig.metrics.picard.obj import PicardMetrics
from cig.metrics.seqlendist.obj import SeqLenDist

known_kinds_and_objs = {
        "hic": HiCMetrics,
        "picard": PicardMetrics,
        "sld": SeqLenDist,
        }
def known_kinds():
    return sorted(known_kinds_and_objs.keys())
#-- known_kinds

def build(kind):
    if kind not in known_kinds():
        raise Exception(f"Unknown kind to build metrics: {kind}")
    return known_kinds_and_objs[kind]()
#-- build
