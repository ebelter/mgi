import click, os, tempfile, unittest
from io import StringIO

class MetricsAlignemntReportsTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "metrics")
        self.samtools_statsfile = os.path.join(self.data_dn, "samtools.stat")
        self.vg_statsfile = os.path.join(self.data_dn, "vgstat.stat")

    def test_write_summary_report(self):
        self.maxDiff = 10000
        from cig.metrics.alignment.reports import write_summary_report_csv, write_summary_report_mw, write_summary_report_table
        from cig.metrics.alignment.obj import AlignmentMetrics
        am = AlignmentMetrics()
        am.load("sample1", self.samtools_statsfile)
        am.load("sample1", self.vg_statsfile)

        # csv
        out_h = StringIO()
        write_summary_report_csv(out_h, am)
        out_h.seek(0)
        expected_output = """LABEL,KIND,TOTAL,ALIGNED,ALIGNED PCT,SECONDARY,PAIRED,PAIRED PCT,UNMAPPED,UNMAPPED PCT,QUALITY MEAN
sample1,samtools,234250490,231187217,98.69%,0,0,0.0%,3063273,1.31%,34.8
sample1,vg,234250490,233298848,99.59%,0,232260512,99.15%,951642,0.41%,53.91
"""
        self.assertEqual(out_h.read(), expected_output)

        # mediawiki
        out_h = StringIO()
        write_summary_report_mw(out_h, am)
        out_h.seek(0)
        self.assertRegex(out_h.read(), r'class="wikitable"')

        # table
        out_h = StringIO()
        write_summary_report_table(out_h, am)
        out_h.seek(0)
        #print(f"{out_h.read()}")
        #out_h.seek(0)
        expected_output = """LABEL    KIND          TOTAL    ALIGNED  ALIGNED PCT      SECONDARY     PAIRED  PAIRED PCT      UNMAPPED  UNMAPPED PCT      QUALITY MEAN
-------  --------  ---------  ---------  -------------  -----------  ---------  ------------  ----------  --------------  --------------
sample1  samtools  234250490  231187217  98.69%                   0          0  0.0%             3063273  1.31%                    34.8
sample1  vg        234250490  233298848  99.59%                   0  232260512  99.15%            951642  0.41%                    53.91"""
        self.assertEqual(out_h.read(), expected_output)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
