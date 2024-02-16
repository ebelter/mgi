from cig.metrics.helpers import str_to_number_if_number

# ## METRICS CLASS	picard.analysis.RnaSeqMetrics
# PF_BASES	PF_ALIGNED_BASES	RIBOSOMAL_BASES	CODING_BASES	UTR_BASES	INTRONIC_BASES	INTERGENIC_BASES	IGNORED_READS	CORRECT_STRAND_READS	INCORRECT_STRAND_READS	NUM_R1_TRANSCRIPT_STRAND_READS	NUM_R2_TRANSCRIPT_STRAND_READS	NUM_UNEXPLAINED_READS	PCT_R1_TRANSCRIPT_STRAND_READS	PCT_R2_TRANSCRIPT_STRAND_READS	PCT_RIBOSOMAL_BASES	PCT_CODING_BASES	PCT_UTR_BASES	PCT_INTRONIC_BASES	PCT_INTERGENIC_BASES	PCT_MRNA_BASES	PCT_USABLE_BASES	PCT_CORRECT_STRAND_READS	MEDIAN_CV_COVERAGE	MEDIAN_5PRIME_BIAS	MEDIAN_3PRIME_BIAS	MEDIAN_5PRIME_TO_3PRIME_BIAS	SAMPLE	LIBRARY	READ_GROUP
# 2254027839	2208982896	2705341	1498952801	661179144	33989567	12156043	0	0	0	3119637	21274	66550	0.993227	0.006773	0.001225	0.678571	0.299314	0.015387	0.005503	0.977885	0.958343	0	0.237791	0.853423	1.035128	0.800213
def parse(f):
    metrics = {}
    metrics_class = None
    while True:
        l = f.readline()
        if l.startswith("## METRICS CLASS"):
            metrics_class = l.split("\t")[1].rstrip()
            break
    if metrics_class is None:
        raise Exception("Failed to find metrics class line when parsing metrics file.")
    keys = list(map(str.lower, f.readline().rstrip().split("\t")))
    vals = list(map(lambda s: str_to_number_if_number(s), f.readline().rstrip().split("\t")))
    metrics = dict(zip(keys, vals))
    return metrics
#-- parse
