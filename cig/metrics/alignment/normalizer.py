import pandas as pd

def metric_names_mapper():
    data = {                 # samtools    vg
            "total":         ["sequences", "alignments"],
            "aligned":       ["reads mapped", "aligned"],
            "secondary":     ["non-primary alignments", "secondary"],
            "paired":        ["reads paired", "properly paired"],
            "unmapped":      ["reads unmapped", "unmapped"], 
            "quality mean":  ["average quality", "mapping quality mean"]
            }
    return pd.DataFrame(index=["samtools", "vg"], data=data)
#-- metric_names_mapper

def normalize(kind, metrics):
    mapper = metric_names_mapper()
    normalized = {}
    for name in mapper.columns:
        normalized[name] = metrics.get(mapper.loc[kind][name], 0)

    normalized["aligned pct"] = round(normalized["aligned"] / normalized["total"], 4)
    normalized["paired pct"] = round(normalized["paired"] / normalized["total"], 4)
    normalized["unmapped pct"] = round(normalized["unmapped"] / normalized["total"], 4)
    return normalized
#-- normalize
