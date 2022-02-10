import json, numpy as np, operator, os, tabulate, yaml
from collections import defaultdict
import matplotlib.pyplot as plt

def get_benchmarks():
    return {
            # Alignment
            "aligned": { # >.9; .75-.9; <.75
                "cat": "alignment",
                "original_name": "2_alignments",
                "ops": [[operator.ge, 75], [operator.gt, 90]],
                "status": ["fail", "marg", "pass"],
                "desc": ">90% (<75%)",
                },
            "unique": { # ? Guessing 75%
                "cat": "alignment",
                "original_name": "total_unique",
                "ops": [[operator.ge, 40]],
                "status": ["fail", "pass"],
                "desc": ">=40%",
                },
            "chimeric": { # .1-.3 typical
                "cat": "alignment",
                "original_name": "chimera_paired",
                "ops": [[operator.ge, 10], [operator.le, 30]],
                "status": ["atypical", "atypical", "typical"],
                "desc": "10-30%",
                },
            "duplicates": { # <.4 pass
                "cat": "alignment",
                "original_name": "total_duplicates",
                "ops": [[operator.lt, 40]],
                "status": ["marg", "pass"],
                "desc": "<40%",
                },
            "unmapped": { # <.1 typical
                "cat": "alignment",
                "original_name": "chimera_ambiguous",
                "ops": [[operator.le, 10]],
                "status": ["atypical", "typical"],
                "desc": "<10%",
                },
            # HiC
            "hic_contacts": { # >.5; .2-.5; <.2
                "cat": "hic",
                "ops": [[operator.ge, 20], [operator.gt, 50]],
                "status": ["fail", "marg", "pass"],
                "desc": ">50% (<20%)",
                },
            "inter_chromosomal": { # <.4 typical
                "cat": "hic",
                "ops": [[operator.lt, 40]],
                "status": ["atypical", "typical"],
                "desc": "<40%",
                },
            "intra_chromosomal": { # >.4 typical
                "cat": "hic",
                "ops": [[operator.gt, 40]],
                "status": ["atypical", "typical"],
                "desc": ">40%",
                },
            # intra fragment   <.1; .1-.2; >.2
            #"intra_fragment": [[[operator.lt, .1], [operator.lt, .2], [operator.lt, 1]], ["fail", "marginal", "pass"], ">40%"],
            #ligations #fail < .05 #marginal .05 .25 #pass > .25
            "short_range": { # <.3; .3-.6; >.6
                "cat": "hic",
                "ops": [[operator.lt, 30], [operator.le, 60]],
                "status": ["fail", "marg", "pass"],
                "desc": "<30% (>60%)",
                },
            "long_range": { # >.35; .2-.35; <.2
                "cat": "hic",
                "original_name": "long_range_greater_than_20kb",
                "ops": [[operator.gt, 35], [operator.ge, 20]],
                "status": ["fail", "marg", "pass"],
                "desc": ">35% (<20%)",
                },
            }
#--

def get_benchmark_names_for_category(cat):
    benchmarks = get_benchmarks()
    return filter(lambda n: benchmarks[n]["cat"] == cat, benchmarks.keys())
#--

def load_stats(stats_fn):
    # Load the original stats
    with open(stats_fn, "r") as f:
        stats = json.load(f)

    # Benchmarks
    benchmarks = get_benchmarks()

    # Add Aligned to Orig Stats
    #stats["pct_sequenced_aligned"] = stats["pct_2_alignments"]
    stats["pct_sequenced_2_alignments"] = stats["pct_2_alignments"]
    stats["pct_unique_2_alignments"] = None
    stats["pct_unique_aligned"] = None
    # Add Chimeric Stats
    stats["pct_sequenced_chimera_ambiguous"] = round(stats["no_chimera_found"] * 100 / stats["sequenced_read_pairs"], 2)
    stats["pct_unique_chimera_ambiguous"] = None
    stats["pct_sequenced_chimera_paired"] = round(stats["2_alignments_a1_a2b_a1b2_b1a2"] * 100 / stats["sequenced_read_pairs"], 2)
    stats["pct_unique_chimera_paired"] = round(stats["2_alignments_a1_a2b_a1b2_b1a2"] * 100 / stats["total_unique"], 2)
    # Add short range sum
    stats["pct_sequenced_short_range"] = sum(list(map(lambda r: stats["_".join(["pct_sequenced_short_range", r])], ["less_than_500bp", "500bp_to_5kb", "5kb_to_20kb"])))
    stats["pct_unique_short_range"] = sum(list(map(lambda r: stats["_".join(["pct_unique_short_range", r])], ["less_than_500bp", "500bp_to_5kb", "5kb_to_20kb"])))
    # Collect and Fix
    new_stats = {
            "sequenced": stats["sequenced_read_pairs"],
            "unique": stats["total_unique"],
            "multimapped": { "seqd": stats["pct_3_or_more_alignments"], },
            }
    for name in sorted(benchmarks.keys()):
        original_name = name
        if "original_name" in benchmarks[name]:
            original_name = benchmarks[name]["original_name"]
        seqd_k = "_".join(["pct", "sequenced", original_name])
        seqd_pct = stats[seqd_k]
        seqd_v = int(round(seqd_pct*stats['sequenced_read_pairs']))
        uniq_k = "_".join(["pct", "unique", original_name])
        uniq_pct = stats[uniq_k]
        if uniq_pct is not None:
            uniq_v = int(round(seqd_pct*stats['total_unique']))
        else:
            uniq_v = None
        # Some of these stats are reversed sequenced v. unique
        if uniq_pct is None or uniq_pct > seqd_pct:
            new_stats[name] = {
                    "seqd": [seqd_v, seqd_pct],
                    "uniq": [uniq_v, uniq_pct],
                    }
        else: # flipped
            new_stats[name] = {
                    "seqd": [uniq_v, uniq_pct],
                    "uniq": [seqd_v, seqd_pct],
                    }
    return new_stats
#--

def get_benchmarks_stats(samples):
    benchmarks = get_benchmarks()
    rows = []
    for name in benchmarks.keys():
        ops = benchmarks[name]["ops"]
        statuses = benchmarks[name]["status"]
        desc = benchmarks[name]["desc"]
        new_rows = [ [name, desc], [name+" uniq", desc] ]
        #new_rows = [ [name+" %", desc], [name+" uniq %", desc] ]
        for j, subn in enumerate(["seqd", "uniq"]):
            for sample in samples:
                stats_v = sample["stats"][name][subn][0]
                stats_pct = sample["stats"][name][subn][1]
                if stats_pct is not None:
                    ops_evals = list(map(lambda op: op[0](stats_pct, op[1]), ops))
                    status = statuses[ops_evals.count(True)]
                    #value = "{:.2%}".format(stats_pct/100)
                else:
                    continue
                new_rows[j].append(f"{status}")
                new_rows[j].append(f"{stats_pct}")
                new_rows[j].append(f"{stats_v}")
            j += 1
        for row in new_rows:
            if len(row) > 2:
                rows.append(row)
    headers=["STAT", "THRESHOLD"]
    for s in samples:
        headers += [s["label"].upper(), "PCT", "VALUE"]
    return headers, rows
#--
