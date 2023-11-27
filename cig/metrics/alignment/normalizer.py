import pandas as pd

def metric_names_mapper():
    data = {                 # samtools    vg
            "total":         ["sequences", "alignments"],
            "aligned":       ["reads mapped", "aligned"],
            "aligned pct":   ["aligned pct", "aligned pct"],
            "secondary":     ["non-primary alignments", "secondary"],
            "paired":        ["reads paired", "properly paired"],
            "paired pct":    ["paired pct", "paired pct"],
            "unmapped":      ["reads unmapped", "unmapped"], 
            "unmapped pct":  ["unmapped pct", "unmapped pct"],
            "quality mean":  ["average quality", "mapping quality mean"]
            }
    return pd.DataFrame(index=["samtools", "vg"], data=data)
#-- metric_names_mapper

def normalize(kind, metrics):
    mapper = metric_names_mapper()
    normalized = {}
    for name in mapper.columns:
        normalized[name] = metrics.get(mapper.loc[kind][name], 0)

    normalized["aligned pct"] = str(round((normalized["aligned"] * 100)/ normalized["total"], 2))+"%"
    normalized["paired pct"] = str(round((normalized["paired"] * 100)/ normalized["total"], 2))+"%"
    normalized["unmapped pct"] = str(round((normalized["unmapped"] * 100)/ normalized["total"], 2))+"%"
    return normalized
#-- normalize
