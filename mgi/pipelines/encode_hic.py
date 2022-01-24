import json, operator, tabulate

def get_benchmarks():
    return {
        # alignable >.9; .75-.9; <.75
        "aligned": [[[operator.ge, 75], [operator.gt, 90]], ["fail", "marginal", "pass"], ">90% (<75%)"],
        # chimera ambiguous <.1 typical
        "chimera_ambiguous": [[[operator.le, 10]], ["atypical", "typical"], "<10%"],
        # chimera paired    .1-.3 typical
        "chimera_paired": [[[operator.ge, 10], [operator.le, .3]], ["atypical", "typical", "atypical"], "10-30%"],
        # duplicates       <.4 pass
        "duplicates": [[[operator.lt, 40]], ["marginal", "pass"], "<40%"],
        # hic contacts >.5; .2-.5; <.2
        "hic_contacts": [[[operator.ge, 20], [operator.gt, 50]], ["fail", "marginal", "pass"], ">50% (<20%)"],
        # inter chromosomal <.4 typical
        "inter_chromosomal": [[[operator.lt, 40]], ["atypical", "typical"], "<40%"],
        # intra chromsomal  >.4 typical
        "intra_chromosomal": [[[operator.gt, 40]], ["atypical", "typical"], ">40%"],
        # intra fragment   <.1; .1-.2; >.2
        #"intra_fragment": [[[operator.lt, .1], [operator.lt, .2], [operator.lt, 1]], ["fail", "marginal", "pass"], ">40%"],
        #ligations #fail < .05 #marginal .05 .25 #pass > .25
        # intra short range <.3; .3-.6; >.6
        "short_range": [[[operator.lt, 30], [operator.le, 60]], ["fail", "marginal", "pass"], "<30% (>60%)"],
        #intra long range >.35; .2-.35; <.2
        "long_range": [[[operator.gt, 35], [operator.ge, 20]], ["fail", "marginal", "pass"], ">35% (<20%)"],
            }
#--

def load_stats(stats_fn):
    # Load the original stats
    with open(stats_fn, "r") as f:
        stats = json.load(f)

    # Add Aligned to Orig Stats
    stats["pct_sequenced_aligned"] = stats["pct_2_alignments"]
    stats["pct_unique_aligned"] = None
    # Add Chimeric Stats
    stats["pct_sequenced_chimera_ambiguous"] = stats["no_chimera_found"] * 100 / stats["sequenced_read_pairs"]
    stats["pct_unique_chimera_ambiguous"] = None
    stats["pct_sequenced_chimera_paired"] = stats["2_alignments_a1_a2b_a1b2_b1a2"] * 100 / stats["sequenced_read_pairs"]
    stats["pct_unique_chimera_paired"] = None
    # Add short range sum
    stats["pct_sequenced_short_range"] = sum(list(map(lambda r: stats["_".join(["pct_sequenced_short_range", r])], ["less_than_500bp", "500bp_to_5kb", "5kb_to_20kb"])))
    stats["pct_unique_short_range"] = sum(list(map(lambda r: stats["_".join(["pct_unique_short_range", r])], ["less_than_500bp", "500bp_to_5kb", "5kb_to_20kb"])))
    # Collect and Fix
    # Some of these stats are reversed sequenced v. unique
    names = ["aligned", "chimera_ambiguous", "chimera_paired", "duplicates", "hic_contacts", "inter_chromosomal", "intra_chromosomal", "short_range", "long_range"]
    orig_names = {"duplicates": "total_duplicates", "long_range": "long_range_greater_than_20kb"}
    new_stats = {}
    for name in names:
        orig_name = name
        if name in orig_names:
            orig_name = orig_names[name]
        seqd_k = "_".join(["pct", "sequenced", orig_name])
        seqd_v = stats[seqd_k]
        uniq_k = "_".join(["pct", "unique", orig_name])
        uniq_v = stats[uniq_k]
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

def get_benchmarks_table(stats_fn):
    new_stats = load_stats(stats_fn)
    rows = []
    benchmarks = get_benchmarks()
    for name in sorted(new_stats.keys()):
        ops, statuses, desc = benchmarks[name]
        row = [name, desc]
        for subn in ("seqd", "uniq"):
            stats_v = new_stats[name][subn]
            if stats_v is not None:
                value = "{:.2%}".format(stats_v/100)
                ops_evals = list(map(lambda op: op[0](stats_v, op[1]), ops))
                status = statuses[ops_evals.count(True)]
            else:
                value = "N/A"
                status = "N/A"
            row += [value, status]
        rows.append(row)
    return tabulate.tabulate(rows, headers=["STAT", "DESC", "ALL%", "STATUS", "UNIQ%", "STATUS"])
#--

def get_benchmarks_histograms(stats_fns):
    pass
#--
