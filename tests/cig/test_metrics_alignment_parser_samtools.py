import os, unittest

class CigMetricsAlignmentSamtoolsTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "metrics")
        self.statsfile = os.path.join(self.data_dn, "samtools.stat")

    def test_parse(self):
        from cig.metrics.alignment.parser.samtools import parse
        with open(self.statsfile, "r") as f:
            metrics = parse(f)
        expected_metrics = {'raw total sequences': '234250490', 'filtered sequences': '0', 'sequences': '234250490', 'is sorted': '0', '1st fragments': '234250490', 'last fragments': '0', 'reads mapped': '231187217', 'reads mapped and paired': '0', 'reads unmapped': '3063273', 'reads properly paired': '0', 'reads paired': '0', 'reads duplicated': '0', 'reads MQ0': '10290474', 'reads QC failed': '0', 'non-primary alignments': '0', 'total length': '35371823990', 'total first fragment length': '35371823990', 'total last fragment length': '0', 'bases mapped': '34909269767', 'bases mapped (cigar)': '34405850376', 'bases trimmed': '0', 'bases duplicated': '0', 'mismatches': '0', 'error rate': '0.000000e+00', 'average length': '151', 'average first fragment length': '151', 'average last fragment length': '0', 'maximum length': '151', 'maximum first fragment length': '151', 'maximum last fragment length': '0', 'average quality': '34.8', 'insert size average': '0.0', 'insert size standard deviation': '0.0', 'inward oriented pairs': '0', 'outward oriented pairs': '0', 'pairs with other orientation': '0', 'pairs on different chromosomes': '0', 'percentage of properly paired reads': '0.0', 'read length': '151', 'read count': '234250490'}
        self.assertDictEqual(metrics, expected_metrics)

    def test_parse_SN(self):
        from cig.metrics.alignment.parser.samtools import parse_SN_line
        l = "\t".join(["SN", "raw total sequences:", "62943876", "# excluding supplementary and secondary reads"])
        stat = parse_SN_line(l)
        self.assertDictEqual(stat, {"raw total sequences": "62943876"})
        l = "\t".join(["SN", "filtered sequences:", "0"])
        stat = parse_SN_line(l)
        self.assertDictEqual(stat, {"filtered sequences": "0"})

    def test_parse_RL(self):
        from cig.metrics.alignment.parser.samtools import parse_RL_line
        l = "\t".join(["RL", "75", "62943876"])
        stat = parse_RL_line(l)
        self.assertDictEqual(stat, {"read length": "75", "read count": "62943876"})

if __name__ == '__main__':
    unittest.main(verbosity=2)
