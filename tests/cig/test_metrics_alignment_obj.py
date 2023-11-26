import os, unittest

class MetricsAlignmentObjTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "metrics")
        self.samtools_statsfile = os.path.join(self.data_dn, "samtools.stat")
        self.vg_statsfile = os.path.join(self.data_dn, "vgstat.stat")

    def tearDown(self):
        pass
        #self.temp_d.cleanup()

    def test_init(self):
        from cig.metrics.alignment.obj import AlignmentMetrics
        am = AlignmentMetrics()

    def test_load(self):
        from cig.metrics.alignment.obj import AlignmentMetrics
        am = AlignmentMetrics()
        am.load("sample1", self.samtools_statsfile)
        self.assertFalse(bool(am.dfs["normalized"].empty))
        self.assertEqual(list(am.dfs["normalized"].index.values), [("sample1", "samtools")])
        self.assertEqual(list(am.dfs["normalized"].columns.values), ['total', 'aligned', 'secondary', 'paired', 'unmapped', 'quality mean', 'aligned pct', 'paired pct', 'unmapped pct'])
        self.assertFalse(bool(am.dfs["samtools"].empty))
        self.assertEqual(list(am.dfs["samtools"].index.values), ["sample1"])
        self.assertEqual(len(am.dfs["samtools"].columns.values), 40)
        am.load("sample2", self.vg_statsfile)
        self.assertEqual(list(am.dfs["normalized"].index.values), [("sample1", "samtools"), ("sample2", "vg")])
        self.assertFalse(bool(am.dfs["vg"].empty))
        self.assertEqual(len(am.dfs["vg"].columns.values), 27)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
import unittest
