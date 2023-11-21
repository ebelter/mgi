import os, unittest

class CigMetricsAlignmentFactoryTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "metrics")
        self.statsfile = os.path.join(self.data_dn, "vgstat.stat")

    def test_get_metrics(self):
        self.maxDiff =10000
        from cig.metrics.alignment.factory import get_metrics
        metrics = get_metrics(self.statsfile)
        self.assertEqual(metrics["kind"], "vg")
        expected = {'alignments': 234250490, 'primary': 234250490, 'secondary': 0, 'aligned': 233298848, 'perfect': 157466185, 'gapless': 231210021, 'paired': 234250490, 'properly paired': 232260512, 'time': 120136, 'speed': 1949.87, "alignment score mean": 153.64, "alignment score median": 161, "alignment score stdev": 20.34, "alignment score max": 161, 'mapping quality mean': 53.91, 'mapping quality median': 60, 'mapping quality stdev': 16.89, 'mapping quality max': 60, 'insertions bp': 4765256, 'insertions events': 1371925, 'deletions bp': 4579379, 'deletions events': 1446051, 'substitutions bp': 228290883, 'substitutions events': 228290883, 'softclips bp': 504180376, 'softclips events': 10170091, 'unmapped': 951642,}
        self.assertDictEqual(metrics["original"], expected)
        expected = {"total": 234250490, "aligned": 233298848, "paired": 232260512, "secondary": 0, "quality mean": 53.91, "unmapped": 951642, "aligned pct": 0.9959, "paired pct": 0.9915, "unmapped pct": 0.0041}
        self.assertDictEqual(metrics["normalized"], expected)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
