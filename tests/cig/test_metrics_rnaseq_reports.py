import os, unittest
from io import StringIO

class MetricsRnaseqReportsTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "metrics")
        self.statsfile = os.path.join(self.data_dn, "rnaseq.metrics")
        self.statsfile_dep = os.path.join(self.data_dn, "rnaseq.dep.metrics")

    def test_write_summary_report(self):
        self.maxDiff = 10000
        from cig.metrics.rnaseq.reports import write_report_csv, write_report_mw, write_report_table
        from cig.metrics.rnaseq.obj import RnaSeqMetrics
        m = RnaSeqMetrics()
        m.load("PAN001", self.statsfile)
        m.load("PAN001-DEP", self.statsfile_dep)

        # csv
        out_h = StringIO()
        write_report_csv(out_h, m)
        out_h.seek(0)
        expected_output = """PF_BASES,PF_ALIGNED_BASES,RIBOSOMAL_BASES,CODING_BASES,UTR_BASES,INTRONIC_BASES,INTERGENIC_BASES,IGNORED_READS,CORRECT_STRAND_READS,INCORRECT_STRAND_READS,NUM_R1_TRANSCRIPT_STRAND_READS,NUM_R2_TRANSCRIPT_STRAND_READS,NUM_UNEXPLAINED_READS,PCT_R1_TRANSCRIPT_STRAND_READS,PCT_R2_TRANSCRIPT_STRAND_READS,PCT_RIBOSOMAL_BASES,PCT_CODING_BASES,PCT_UTR_BASES,PCT_INTRONIC_BASES,PCT_INTERGENIC_BASES,PCT_MRNA_BASES,PCT_USABLE_BASES,PCT_CORRECT_STRAND_READS,MEDIAN_CV_COVERAGE,MEDIAN_5PRIME_BIAS,MEDIAN_3PRIME_BIAS,MEDIAN_5PRIME_TO_3PRIME_BIAS
PAN001,2254027839,2208982896,2705341,1498952801,661179144,33989567,12156043,0,0,0,3119637,21274,66550,99%,1%,0%,68%,30%,2%,1%,98%,96%,0%,0.24,0.85,1.04,0.8
PAN001-DEP,5975622876,5850251047,21268635,3303541050,2103739837,296667095,125034430,0,0,0,3036392,87867,291711,97%,3%,0%,56%,36%,5%,2%,92%,90%,0%,0.22,0.87,1.02,0.85
"""
        self.assertEqual(out_h.read(), expected_output)

        # mediawiki
        out_h = StringIO()
        write_report_mw(out_h, m)
        out_h.seek(0)
        self.assertRegex(out_h.read(), r'class="wikitable"')

        # table
        out_h = StringIO()
        write_report_table(out_h, m)
        #out_h.seek(0)
        #print(f"{out_h.read()}")
        out_h.seek(0)
        expected_output = """              PF_BASES    PF_ALIGNED_BASES    RIBOSOMAL_BASES    CODING_BASES    UTR_BASES    INTRONIC_BASES    INTERGENIC_BASES    IGNORED_READS    CORRECT_STRAND_READS    INCORRECT_STRAND_READS    NUM_R1_TRANSCRIPT_STRAND_READS    NUM_R2_TRANSCRIPT_STRAND_READS    NUM_UNEXPLAINED_READS  PCT_R1_TRANSCRIPT_STRAND_READS    PCT_R2_TRANSCRIPT_STRAND_READS    PCT_RIBOSOMAL_BASES    PCT_CODING_BASES    PCT_UTR_BASES    PCT_INTRONIC_BASES    PCT_INTERGENIC_BASES    PCT_MRNA_BASES    PCT_USABLE_BASES    PCT_CORRECT_STRAND_READS      MEDIAN_CV_COVERAGE    MEDIAN_5PRIME_BIAS    MEDIAN_3PRIME_BIAS    MEDIAN_5PRIME_TO_3PRIME_BIAS
----------  ----------  ------------------  -----------------  --------------  -----------  ----------------  ------------------  ---------------  ----------------------  ------------------------  --------------------------------  --------------------------------  -----------------------  --------------------------------  --------------------------------  ---------------------  ------------------  ---------------  --------------------  ----------------------  ----------------  ------------------  --------------------------  --------------------  --------------------  --------------------  ------------------------------
PAN001      2254027839          2208982896            2705341      1498952801    661179144          33989567            12156043                0                       0                         0                           3119637                             21274                    66550  99%                               1%                                0%                     68%                 30%              2%                    1%                      98%               96%                 0%                                          0.24                  0.85                  1.04                            0.8
PAN001-DEP  5975622876          5850251047           21268635      3303541050   2103739837         296667095           125034430                0                       0                         0                           3036392                             87867                   291711  97%                               3%                                0%                     56%                 36%              5%                    2%                      92%               90%                 0%                                          0.22                  0.87                  1.02                            0.85"""
        self.assertEqual(out_h.read(), expected_output)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
