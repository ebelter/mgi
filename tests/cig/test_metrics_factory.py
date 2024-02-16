import os, unittest

class MetricsFactoryTest(unittest.TestCase):
    def test_known_types(self):
        from cig.metrics.factory import known_kinds
        kk = known_kinds()
        self.assertTrue(len(kk))

    def test_build(self):
        from cig.metrics.factory import build
        from cig.metrics.picard.obj import PicardMetrics
        kind = "unknown"
        with self.assertRaisesRegex(Exception, f"Unknown kind to build metrics: {kind}"):
            build(kind)
        kind = "picard"
        m = build(kind)
        self.assertTrue(isinstance(m, PicardMetrics))
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
