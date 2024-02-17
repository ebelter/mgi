import os, unittest

class CigMetricsPicardParserTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "metrics")
        self.statsfile = os.path.join(self.data_dn, "picard.rnaseq.metrics")

    def test_parse(self):
        from cig.metrics.picard.parser import parse
        with open(self.statsfile, "r") as f:
            metrics = parse(f)
        expected = {'pf_bases': 2254027839, 'pf_aligned_bases': 2208982896, 'ribosomal_bases': 2705341, 'coding_bases': 1498952801, 'utr_bases': 661179144, 'intronic_bases': 33989567, 'intergenic_bases': 12156043, 'ignored_reads': 0, 'correct_strand_reads': 0, 'incorrect_strand_reads': 0, 'num_r1_transcript_strand_reads': 3119637, 'num_r2_transcript_strand_reads': 21274, 'num_unexplained_reads': 66550, 'pct_r1_transcript_strand_reads': 0.993227, 'pct_r2_transcript_strand_reads': 0.006773, 'pct_ribosomal_bases': 0.001225, 'pct_coding_bases': 0.678571, 'pct_utr_bases': 0.299314, 'pct_intronic_bases': 0.015387, 'pct_intergenic_bases': 0.005503, 'pct_mrna_bases': 0.977885, 'pct_usable_bases': 0.958343, 'pct_correct_strand_reads': 0, 'median_cv_coverage': 0.237791, 'median_5prime_bias': 0.853423, 'median_3prime_bias': 1.035128, 'median_5prime_to_3prime_bias': 0.800213}
        self.maxDiff = 10000
        self.assertDictEqual(metrics, expected)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
