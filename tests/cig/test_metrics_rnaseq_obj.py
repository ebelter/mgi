import os, unittest

class MetricsRnaseqObjTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "metrics")
        self.statsfile = os.path.join(self.data_dn, "rnaseq.metrics")

    def test_init(self):
        from cig.metrics.rnaseq.obj import RnaSeqMetrics
        am = RnaSeqMetrics()

    def test_load(self):
        from cig.metrics.rnaseq.obj import RnaSeqMetrics
        m = RnaSeqMetrics()
        m.load("sample1", self.statsfile)
        self.assertFalse(bool(m.df.empty))
        self.assertEqual(list(m.df.index.values), ["sample1"])
        self.assertEqual(len(m.df.columns.values), 27)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
import unittest
