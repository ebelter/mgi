from cig.metrics.hic.metadata import get_metadata

def normalize(incoming_metrics):
    md = get_metadata()

    # Add Aligned
    incoming_metrics["pct_sequenced_2_alignments"] = incoming_metrics["pct_2_alignments"] + incoming_metrics["pct_3_or_more_alignments"]
    incoming_metrics["pct_unique_2_alignments"] = None
    incoming_metrics["pct_unique_aligned"] = None
    # Add Chimeric
    incoming_metrics["pct_sequenced_chimera_ambiguous"] = round(incoming_metrics["no_chimera_found"] * 100 / incoming_metrics["sequenced_read_pairs"], 2)
    incoming_metrics["pct_unique_chimera_ambiguous"] = None
    incoming_metrics["pct_sequenced_chimera_paired"] = round(incoming_metrics["2_alignments_a1_a2b_a1b2_b1a2"] * 100 / incoming_metrics["sequenced_read_pairs"], 2)
    incoming_metrics["pct_unique_chimera_paired"] = round(incoming_metrics["2_alignments_a1_a2b_a1b2_b1a2"] * 100 / incoming_metrics["total_unique"], 2)
    # Add short range sum
    incoming_metrics["pct_sequenced_short_range"] = sum(list(map(lambda r: incoming_metrics["_".join(["pct_sequenced_short_range", r])], ["less_than_500bp", "500bp_to_5kb", "5kb_to_20kb"])))
    incoming_metrics["pct_unique_short_range"] = sum(list(map(lambda r: incoming_metrics["_".join(["pct_unique_short_range", r])], ["less_than_500bp", "500bp_to_5kb", "5kb_to_20kb"])))

    new_metrics = {
            "sequenced": incoming_metrics["sequenced_read_pairs"],
            "unique": incoming_metrics["total_unique"],
            #"multimapped_pct": incoming_metrics["pct_3_or_more_alignments"],
            }
    for name in sorted(md.keys()):
        original_name = name
        if "original_name" in md[name]:
            original_name = md[name]["original_name"]
        seqd_k = "_".join(["pct", "sequenced", original_name])
        seqd_pct = incoming_metrics[seqd_k]
        seqd_v = int(round(seqd_pct * incoming_metrics['sequenced_read_pairs']))
        uniq_k = "_".join(["pct", "unique", original_name])
        uniq_pct = incoming_metrics[uniq_k]
        if uniq_pct is not None:
            uniq_v = int(round(seqd_pct * incoming_metrics['total_unique']))
        else:
            uniq_v = None
        # Some of these stats may be flipped, sequenced v. unique
        if uniq_pct is None or uniq_pct > seqd_pct:
            new_metrics[name] = seqd_v 
            new_metrics[name+"_pct"] = f"{seqd_pct}%"
            if uniq_pct is not None:
                new_metrics[name+"_uniq"] = uniq_v
                new_metrics[name+"_uniq_pct"] = f"{uniq_pct}%"
        else: # flipped
            new_metrics[name] = uniq_v 
            new_metrics[name+"_pct"] = f"{uniq_pct}%"
            new_metrics[name+"_uniq"] = seqd_v
            new_metrics[name+"_uniq_pct"] = f"{seqd_pct}%"
    return new_metrics
#--
