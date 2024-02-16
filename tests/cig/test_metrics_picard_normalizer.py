import unittest

class MetricsRnaseqNormalizerTest(unittest.TestCase):
    def test_normalize(self):
        self.maxDiff = 10000
        from cig.metrics.picard.normalizer import normalize
        metrics = {'pf_bases': 2254027839, 'pf_aligned_bases': 2208982896, 'ribosomal_bases': 2705341, 'coding_bases': 1498952801, 'utr_bases': 661179144, 'intronic_bases': 33989567, 'intergenic_bases': 12156043, 'ignored_reads': 0, 'correct_strand_reads': 0, 'incorrect_strand_reads': 0, 'num_r1_transcript_strand_reads': 3119637, 'num_r2_transcript_strand_reads': 21274, 'num_unexplained_reads': 66550, 'pct_r1_transcript_strand_reads': 0.99, 'pct_r2_transcript_strand_reads': 0.01, 'pct_ribosomal_bases': 0.0, 'pct_coding_bases': 0.68, 'pct_utr_bases': 0.3, 'pct_intronic_bases': 0.02, 'pct_intergenic_bases': 0.01, 'pct_mrna_bases': 0.98, 'pct_usable_bases': 0.96, 'pct_correct_strand_reads': 0, 'median_cv_coverage': 0.24, 'median_5prime_bias': 0.85, 'median_3prime_bias': 1.04, 'median_5prime_to_3prime_bias': 0.8}
        expected = {'pf_bases': 2254027839, 'pf_aligned_bases': 2208982896, 'ribosomal_bases': 2705341, 'coding_bases': 1498952801, 'utr_bases': 661179144, 'intronic_bases': 33989567, 'intergenic_bases': 12156043, 'ignored_reads': 0, 'correct_strand_reads': 0, 'incorrect_strand_reads': 0, 'num_r1_transcript_strand_reads': 3119637, 'num_r2_transcript_strand_reads': 21274, 'num_unexplained_reads': 66550, 'pct_r1_transcript_strand_reads': "99%", 'pct_r2_transcript_strand_reads': "1%", 'pct_ribosomal_bases': "0%", 'pct_coding_bases': "68%", 'pct_utr_bases': "30%", 'pct_intronic_bases': "2%", 'pct_intergenic_bases': "1%", 'pct_mrna_bases': "98%", 'pct_usable_bases': "96%", 'pct_correct_strand_reads': "0%", 'median_cv_coverage': 0.24, 'median_5prime_bias': 0.85, 'median_3prime_bias': 1.04, 'median_5prime_to_3prime_bias': 0.8}
        got = normalize(metrics)
        self.assertDictEqual(got, expected)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
