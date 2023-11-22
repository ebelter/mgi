import click, os, tempfile, unittest
from io import StringIO

class MetricsAlignmentObjTest(unittest.TestCase):
    def setUp(self):
        #self.temp_d = tempfile.TemporaryDirectory()
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "metrics")
        self.samtools_statsfile = os.path.join(self.data_dn, "samtools.stat")
        self.vg_statsfile = os.path.join(self.data_dn, "vgstat.stat")

    def tearDown(self):
        pass
        #self.temp_d.cleanup()

    def test_init(self):
        from cig.metrics.alignment.obj import AlignmentMetrics
        am = AlignmentMetrics()
        #print(f"{am.df}")
        #self.assertFalse(am.df.empty)

    def test_load(self):
        from cig.metrics.alignment.obj import AlignmentMetrics
        am = AlignmentMetrics()
        am.load("sample1", self.samtools_statsfile)
        self.assertFalse(bool(am.dfs["normalized"].empty))
        self.assertEqual(list(am.dfs["normalized"].columns.values), ["sample1"])
        self.assertFalse(bool(am.dfs["samtools"].empty))
        self.assertEqual(list(am.dfs["samtools"].columns.values), ["sample1"])
        am.load("sample2", self.vg_statsfile)
        self.assertEqual(list(am.dfs["normalized"].columns.values), ["sample1", "sample2"])
        self.assertFalse(bool(am.dfs["vg"].empty))
        self.assertEqual(list(am.dfs["vg"].columns.values), ["sample2"])


    def Xtest_complete(self):
        from cig.metrics.seqlendist.obj import SeqLenDist
        sld = SeqLenDist("lr")
        sld.load(self.fastq_fn, "test")
        sld.complete()
        self.assertEqual(len(sld.lengths_df), 25)
        self.assertFalse(sld.summary_df.empty)
        expected = """min         214.00
max         922.00
mean        513.84
length    12846.00
count        25.00
n50         593.00
Name: test, dtype: float64"""
        #print(f"{sld.summary_df.loc['test']}")
        #print(f"||{sld.bins_df.xs('test')}||")
        self.assertEqual(f"{sld.summary_df.loc['test']}", expected)
        expected = """     min  max        mean  length  count
bin                                     
1    214  500  385.857143    5402     14
2    554  922  676.727273    7444     11"""
        self.assertEqual(f"{sld.bins_df.xs('test')}", expected)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
import unittest
