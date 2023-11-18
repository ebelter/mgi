import os, unittest

class CigMetricsAlignmentVgTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "metrics")
        self.statsfile = os.path.join(self.data_dn, "vgstat.stat")

    def test_parse(self):
        from cig.metrics.alignment.vg import parse
        with open(self.statsfile, "r") as f:
            metrics = parse(f)
        expected = {'alignments': 234250490, 'primary': 234250490, 'secondary': 0, 'aligned': 233298848, 'perfect': 157466185, 'gapless': 231210021, 'paired': 234250490, 'properly paired': 232260512, 'time': 120136, 'speed': 1949.87, "alignment score mean": 153.64, "alignment score median": 161, "alignment score stdev": 20.34, "alignment score max": 161, 'mapping quality mean': 53.91, 'mapping quality median': 60, 'mapping quality stdev': 16.89, 'mapping quality max': 60, 'insertions bp': 4765256, 'insertions events': 1371925, 'deletions bp': 4579379, 'deletions events': 1446051, 'substitutions bp': 228290883, 'substitutions events': 228290883, 'softclips bp': 504180376, 'softclips events': 10170091, 'unaligned': 951642, 'aligned pct': 99.59, 'paired pct': 99.55}
        self.maxDiff = 10000
        self.assertDictEqual(metrics, expected)

    def test_parse_events(self):
        from cig.metrics.alignment.vg import parse_events
        expected = {"insertions bp": 4765256, "insertions events": 1371925,}
        self.assertEqual(parse_events("insertions", "4765256 bp in 1371925 read events"), expected)

    def test_parse_multi(self):
        from cig.metrics.alignment.vg import parse_multi
        v = "mean 153.643, median 161, stdev 20.3432, max 161 (157466185 reads)"
        expected = {"alignment score mean": 153.64, "alignment score median": 161, "alignment score stdev": 20.34, "alignment score max": 161}
        self.assertEqual(parse_multi("alignment score", v), expected)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
