import unittest

class MetricsAlignmentNormalizerTest(unittest.TestCase):
    def test_metric_names_mapper(self):
        from cig.metrics.alignment.normalizer import metric_names_mapper
        mapper = metric_names_mapper()
        self.assertFalse(mapper.empty)

    def test_normalize(self):
        from cig.metrics.alignment.normalizer import normalize
        metrics = {"sequences": 234250490, "reads mapped": 231187217, "reads unmapped": 3063273, "reads paired": 0, "non-primary alignments": 0, "average quality": 34.8,}
        expected = {"total": 234250490, "aligned": 231187217, "unmapped": 3063273, "paired": 0, "secondary": 0, "quality mean": 34.8, "aligned pct": 0.9869, "paired pct": 0.0, "unmapped pct": 0.0131,}
        self.assertDictEqual(normalize("samtools", metrics), expected)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
