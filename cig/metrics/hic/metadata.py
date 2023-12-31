import operator

def get_metadata():
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
