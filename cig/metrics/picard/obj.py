import pandas as pd
from cig.metrics.picard.normalizer import normalize
from cig.metrics.picard.parser import parse

class PicardMetrics():
    def __init__(self):
        self.df = None
    #-- __init__

    def load(self, label, statsfile):
        with open(statsfile, "r") as f:
            metrics = normalize(parse(f))
        if self.df is None:
            self.df = pd.DataFrame(index=[label], data=metrics)
        else:
            self.df.loc[label] = metrics
    #-- load
#-- RnaSeqMetrics
