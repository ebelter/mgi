import pandas as pd
from cig.metrics.alignment.factory import get_metrics

class AlignmentMetrics():
    #@staticmethod
    def __init__(self):
        self.dfs = {"normalized": None}
    #-- __init__

    def load(self, label, statsfile):
        metrics = get_metrics(statsfile)
        # dict with kind, original, normalized
        # kind combined metrics
        if getattr(self.dfs, metrics["kind"], None) is None:
            self.dfs[metrics["kind"]] = pd.DataFrame(index=metrics["original"].keys(), data={label: metrics["original"].values()})
        else:
            self.dfs[metrics["kind"]][label] = metrics["original"].values()
        # normalized combined metrics
        if self.dfs["normalized"] is None:
            self.dfs["normalized"] = pd.DataFrame(index=metrics["normalized"].keys(), data={label: metrics["normalized"].values()})
        else:
            self.dfs["normalized"][label] = metrics["normalized"].values()
    #-- load
#-- AlignmentMetrics
