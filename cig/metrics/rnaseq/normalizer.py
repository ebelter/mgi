import pandas as pd
from cig.metrics.helpers import number_to_str

def normalize(metrics):
    normalized = {}
    for k in metrics.keys():
        normalized[k] = metrics[k]
        if k.startswith("pct"):
            normalized[k] = number_to_str(round(metrics[k]*100, 2))+"%"
    return normalized
#-- normalize
