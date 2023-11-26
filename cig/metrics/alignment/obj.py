import pandas as pd
from cig.metrics.alignment.factory import get_metrics

class AlignmentMetrics():
    #@staticmethod
    def __init__(self):
        self.dfs = {"normalized": None}
    #-- __init__

    def load(self, label, statsfile):
        metrics = get_metrics(statsfile) # dict with kind, original, normalized
        kind = metrics["kind"]
        # kind combined metrics - row index is label
        if getattr(self.dfs, kind, None) is None:
            self.dfs[kind] = pd.DataFrame(index=[label], data=metrics["original"])
        else:
            self.dfs[label].loc[label] = metrics["original"]
        # normalized combined metrics - row index is int
        data = metrics["normalized"]
        if self.dfs["normalized"] is None:
            metrics["normalized"].update({"label": label, "kind": kind})
            self.dfs["normalized"] = pd.DataFrame(index=[0], data=metrics["normalized"]).set_index(["label", "kind"])
        else:
            self.dfs["normalized"].loc[(label, kind),:] = metrics["normalized"]
    #-- load
#-- AlignmentMetrics
