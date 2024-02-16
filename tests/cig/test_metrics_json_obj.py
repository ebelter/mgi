import os, unittest

class MetricsJsonObjTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "metrics")

    def test_star(self):
        from cig.metrics.json.obj import StarMetrics
        m = StarMetrics()
        statsfile = os.path.join(self.data_dn, "star_log.json")
        m.load("sample1", statsfile)
        self.assertFalse(bool(m.df.empty))
        self.assertEqual(list(m.df.index.values), ["sample1"])
        self.assertEqual(len(m.df.columns.values), 32)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
import unittest
