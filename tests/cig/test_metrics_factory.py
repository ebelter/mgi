import os, unittest

class MetricsFactoryTest(unittest.TestCase):
    def test_known_types(self):
        from cig.metrics.factory import known_kinds
        kk = known_kinds()
        self.assertTrue(len(kk))

    def test_build(self):
        from cig.metrics.factory import build
        from cig.metrics.rnaseq.obj import RnaSeqMetrics
        kind = "unknown"
        with self.assertRaisesRegex(Exception, f"Unknown kind to build metrics: {kind}"):
            build(kind)
        kind = "rnaseq"
        m = build(kind)
        self.assertTrue(isinstance(m, RnaSeqMetrics))
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
