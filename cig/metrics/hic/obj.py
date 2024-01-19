import json, pandas as pd
#import cig.metrics.hic.metadata
from cig.metrics.hic.normalizer import normalize

class HiCMetrics():
    def __init__(self):
        self.df = None
    #-- __init__

    def load(self, label, statsfile):
        with open(statsfile, "r") as f:
            metrics = json.load(f)
        metrics = normalize(metrics)
        if self.df is None:
            self.df = pd.DataFrame(index=[label], data=metrics)
        else:
            self.df.loc[label] = metrics
    #-- load
#-- HiCMetrics
