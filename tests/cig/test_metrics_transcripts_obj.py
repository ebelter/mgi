import os, unittest

class MetricsTranscriptsObjTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "metrics")
        self.gtffile_100 = os.path.join(self.data_dn, "stringtie.denovo.100.gtf")
        self.gtffile_80 = os.path.join(self.data_dn, "stringtie.denovo.80.gtf")

    def test_init(self):
        from cig.metrics.transcripts.obj import TranscriptSummary
        m = TranscriptSummary()

    def test_load(self):
        from cig.metrics.transcripts.obj import TranscriptSummary
        m = TranscriptSummary()
        m.load("SAMP001 100", self.gtffile_100)
        self.assertFalse(bool(m.df.empty))
        self.assertEqual(list(m.df.index.values), ["SAMP001 100"])
        self.assertEqual(len(m.df.columns.values), 1)
        m.load("SAMP001 80", self.gtffile_80)
        self.assertEqual(list(m.df.index.values), ["SAMP001 100", "SAMP001 80"])
        self.assertEqual(len(m.df.columns.values), 1)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
import unittest
