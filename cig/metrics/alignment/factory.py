import cig.metrics.alignment.normalizer as normalizer
from cig.metrics.alignment.parser.obj import StatsfileParser

def get_metrics(statsfile):
    parser = StatsfileParser(statsfile)
    metrics = parser.parse()
    normalized_metrics = normalizer.normalize(parser.kind, metrics)
    return {
            "kind": parser.kind,
            "original": metrics,
            "normalized": normalized_metrics,
            }
#--
