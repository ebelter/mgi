import unittest

class MetricsHicMetadataTest(unittest.TestCase):
    def test_get_metadata(self):
        from cig.metrics.hic.metadata import get_metadata
        md = get_metadata()
        self.assertEqual(type(md), dict)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
