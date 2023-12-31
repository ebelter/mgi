import json, os, unittest

class MetricsHicNormalizerTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "metrics")
        self.statsfile = os.path.join(self.data_dn, "hic.stats.json")

    def test_normalize(self):
        self.maxDiff = 10000
        from cig.metrics.hic.normalizer import normalize
        with open(self.statsfile, "r") as f:
            metrics = json.load(f)
        expected = {'sequenced': 509819970, 'unique': 24593715353, 'aligned': 50314132839, 'aligned_pct': '98.69%', 'chimeric': 5878224254, 'chimeric_pct': '11.53%', 'chimeric_uniq': 2835578481, 'chimeric_uniq_pct': '23.91%', 'duplicates': 10390130989, 'duplicates_pct': '20.38%', 'duplicates_uniq': 5012063264, 'duplicates_uniq_pct': '29.7%', 'hic_contacts': 21172823354, 'hic_contacts_pct': '41.53%', 'hic_contacts_uniq': 10213493001, 'hic_contacts_uniq_pct': '86.1%', 'inter_chromosomal': 4124443557, 'inter_chromosomal_pct': '8.09%', 'inter_chromosomal_uniq': 1989577616, 'inter_chromosomal_uniq_pct': '16.77%', 'intra_chromosomal': 17053477997, 'intra_chromosomal_pct': '33.45%', 'intra_chromosomal_uniq': 8226374690, 'intra_chromosomal_uniq_pct': '69.33%', 'long_range': 11761546708, 'long_range_pct': '23.07%', 'long_range_uniq': 5673616266, 'long_range_uniq_pct': '47.83%', 'short_range': 5286833089, 'short_range_pct': '10.37%', 'short_range_uniq': 2550299119, 'short_range_uniq_pct': '21.51%', 'unique_pct': '48.24%', 'unique_uniq': 11863686548, 'unique_uniq_pct': '70.3%', 'unmapped': 667864161, 'unmapped_pct': '1.31%'}
        got = normalize(metrics)
        #print(got)
        self.assertDictEqual(got, expected)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
