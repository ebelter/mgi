import json, os, unittest

class MetricsHicObjTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "metrics")
        self.statsfile = os.path.join(self.data_dn, "hic.stats.json")

    def test_init(self):
        from cig.metrics.hic.obj import HiCMetrics
        m = HiCMetrics()

    def test_load(self):
        from cig.metrics.hic.obj import HiCMetrics
        m = HiCMetrics()
        m.load("sample1", self.statsfile)
        #print(m.df)
        self.assertFalse(bool(m.df.empty))
        self.assertEqual(list(m.df.index.values), ["sample1"])
        self.assertEqual(len(m.df.columns.values), 37)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
