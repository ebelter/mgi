import click, os, unittest

class MetricsAlignmentParserTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "metrics")
        self.samtools_statsfile = os.path.join(self.data_dn, "samtools.stat")
        self.vg_statsfile = os.path.join(self.data_dn, "vgstat.stat")
        self.unknown_statsfile = os.path.join(self.data_dn, "sample.fasta")

    def test_get_parser(self):
        from cig.metrics.alignment.parser.obj import get_parser
        from cig.metrics.alignment.parser.samtools import parse as samtools_parse
        from cig.metrics.alignment.parser.vg import parse as vg_parse

        kind, parser = get_parser(self.samtools_statsfile)
        self.assertEqual(kind, "samtools")
        self.assertEqual(parser, samtools_parse)
        kind, parser = get_parser(self.vg_statsfile)
        self.assertEqual(kind, "vg")
        self.assertEqual(parser, vg_parse)

        with self.assertRaisesRegex(Exception, f"Failed to determine stats file kind for {self.unknown_statsfile}"):
            get_parser(self.unknown_statsfile)

    def test_init(self):
        from cig.metrics.alignment.parser.obj import StatsfileParser
        parser = StatsfileParser(self.samtools_statsfile)
        self.assertTrue(bool(parser))
        self.assertEqual(parser.statsfile, self.samtools_statsfile)
        self.assertEqual(parser.kind, "samtools")
        self.assertTrue(bool(parser.parser))

    def test_parse(self):
        from cig.metrics.alignment.parser.obj import StatsfileParser
        parser = StatsfileParser(self.samtools_statsfile)
        self.assertTrue(bool(parser))
        metrics = parser.parse()
        self.assertTrue(bool(metrics))
        self.assertEqual(type(metrics), dict)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
