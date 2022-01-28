import json, numpy as np, operator, os, tabulate, yaml
from collections import defaultdict
import matplotlib.pyplot as plt

def get_benchmarks():
    return {
            # Alignment
            "aligned": { # >.9; .75-.9; <.75
                "cat": "alignment",
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
    stats["pct_sequenced_aligned"] = stats["pct_2_alignments"]
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
            "multimapped": { "seqd": stats["pct_3_or_more_alignments"], },
            }
    for name in sorted(benchmarks.keys()):
        original_name = name
        if "original_name" in benchmarks[name]:
            original_name = benchmarks[name]["original_name"]
        seqd_k = "_".join(["pct", "sequenced", original_name])
        seqd_v = stats[seqd_k]
        uniq_k = "_".join(["pct", "unique", original_name])
        uniq_v = stats[uniq_k]
        # Some of these stats are reversed sequenced v. unique
        if uniq_v is None or uniq_v > seqd_v:
            new_stats[name] = {
                    "seqd": seqd_v,
                    "uniq": uniq_v,
                    }
        else: # flipped
            new_stats[name] = {
                    "seqd": uniq_v,
                    "uniq": seqd_v,
                    }
    return new_stats
#--

def get_benchmarks_table(samples):
    benchmarks = get_benchmarks()
    rows = []
    for name in benchmarks.keys():
        ops = benchmarks[name]["ops"]
        statuses = benchmarks[name]["status"]
        desc = benchmarks[name]["desc"]
        new_rows = [ [name+" %", desc], [name+" uniq %", desc] ]
        for j, subn in enumerate(["seqd", "uniq"]):
            for sample in samples:
                stats_v = sample["stats"][name][subn]
                if stats_v is not None:
                    value = "{:.2%}".format(stats_v/100)
                    ops_evals = list(map(lambda op: op[0](stats_v, op[1]), ops))
                    status = statuses[ops_evals.count(True)]
                else:
                    continue
                    value = "N/A"
                    status = "N/A"
                new_rows[j].append(f"{status} {value}")
            j += 1
        for row in new_rows:
            if len(row) > 2:
                rows.append(row)
    return tabulate.tabulate(rows, headers=["STAT", "THRESHOLD"]+list(map(lambda s: s["label"].upper(), samples)))
#--

def create_benchmarks_comparative_histograms(groups, output_dn="."):
    for cat in ("alignment", "hic"):
        for metric_name in get_benchmark_names_for_category(cat):
            aligned_reads_histogram(groups, metric_name)
            plt.title(f"{cat.title()} - {' '.join(metric_name.split('_')).title()}")
            fn = os.path.join(output_dn, ".".join(["all", cat, metric_name, "png"]))
            plt.savefig(fn)
#--

def aligned_reads_histogram(groups, metric_name):
    sample_names = sorted(groups.keys())
    benchmarks = get_benchmarks()
    colors = ["grey", "burlywood", "olive"]
    xtickslabels_fs = 7

    fig, ax = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(len(sample_names)+3, 5))
    fig.text(0.04, 0.5, 'Percent', va='center', rotation='vertical')
    idx = np.asarray([i for i in range(len(sample_names))])

    #ax.set_title(" ".join(metric_name.split("_")).title())
    ax.set_xticks(idx+.15)
    ax.set_xticklabels(sample_names, fontsize=xtickslabels_fs)
    ax.set_ylabel(benchmarks[metric_name]["desc"])
    ax.set_yticks(np.arange(0, 100, step=10))
    plt.ylim(0, 100)
    #ax.set_yticks(np.arange(0, 100, step=10), labels=benchmarks[metric_name]["desc"])
    data = defaultdict(lambda: [])
    for sample_name in sample_names:
        for i, sample in enumerate(groups[sample_name]):
            data[i].append(sample["stats"][metric_name]["seqd"])
    for i, k in enumerate(sorted(data.keys())):
        ax.bar(idx+(i*.3), data[k], width=0.2, color=colors[i])
    #ax.bar(idx, list(map(lambda s: samples[s][0]["stats"][metric_name]["seqd"], sample_names)), width=0.2, color=colors[0])
    #ax.bar(idx+.3, list(map(lambda s: samples[s][1]["stats"][metric_name]["seqd"], sample_names)), width=0.2, color=colors[1])
    for op, value in benchmarks[metric_name]["ops"]:
        ax.axhline(y=value, linewidth=1, color="peru", linestyle="--")
#--

def create_benchmarks_detail_histogram(sample, output_dn="."):
    colors = ["grey", "burlywood", "olive"]
    xtickslabels_fs = 7
    fig, axes = plt.subplots(1, 2, sharey=True, figsize=(15, 6))
    fig.text(0.04, 0.5, 'Percent', va='center', rotation='vertical')

    axes[0].set_yticks(np.arange(0, 100, step=10))
    plt.ylim(0, 100)

    cats = ["Alignment", "HiC"]
    for ci, cat in enumerate(cats):
        data = []
        metric_names = list(get_benchmark_names_for_category(cat.lower()))
        for i, metric_name in enumerate(metric_names):
            data.append(sample["stats"][metric_name]["seqd"])
        idx = np.asarray([i for i in range(len(metric_names))])
        axes[ci].set_title(f"{cat} Benchmarks")
        axes[ci].bar(idx, data, width=0.2, color=colors)
        axes[ci].set_xticks(idx, metric_names, fontsize=xtickslabels_fs, rotation=15)

    fn = os.path.join(output_dn, ".".join([sample["name"], "benchmarks", "png"]))
    plt.savefig(fn)
#--
