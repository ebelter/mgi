import json, pandas as pd

class StarMetrics():
    def __init__(self):
        self.df = None
    #-- __init__

    def load(self, label, statsfile):
        with open(statsfile, "r") as f:
            metrics = json.load(f)["star_log_qc"]
        if self.df is None:
            self.df = pd.DataFrame(index=[label], data=metrics)
        else:
            self.df.loc[label] = metrics
    #-- load
#-- StarMetrics
