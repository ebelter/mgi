import click, os, sys, unittest

class MetricsHelpersTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "metrics")

    def test_seqfile(self):
        from cig.metrics.helpers import SeqFile
        fastq = os.path.join(self.data_dn, "sample.fastq.gz")
        with SeqFile(fastq) as sf:
            self.assertTrue(sf)
            self.assertEqual(sf.fn, fastq)
            self.assertEqual(sf.type, "fastq")
            self.assertEqual(sf.is_gzipped, True)
            count = 0
            for e in sf:
                count += 1
            self.assertEqual(count, 3)
        fasta = os.path.join(self.data_dn, "sample.fasta")
        with SeqFile(f"{fasta}") as sf:
            self.assertTrue(sf)
            self.assertEqual(sf.fn, fasta)
            self.assertEqual(sf.type, "fasta")
            self.assertEqual(sf.is_gzipped, False)
            count = 0
            for e in sf:
                count += 1
            self.assertEqual(count, 3)
    def test_out_handle(self):
        from cig.metrics.helpers import OutHandle 
        with OutHandle() as out_h:
            self.assertTrue(bool(out_h.fh))
            self.assertEqual(out_h.fh, sys.stdout)
            self.assertEqual(out_h.bn, "-")
            self.assertEqual(out_h.ext, "txt")
            self.assertEqual(out_h.mode, "w")
            self.assertEqual(out_h.fn, "STDOUT")
        with OutHandle(bn="plot", ext="png") as out_h:
            self.assertTrue(bool(out_h.fh))
            self.assertEqual(out_h.bn, "plot")
            self.assertEqual(out_h.ext, "png")
            self.assertEqual(out_h.mode, "wb")
            self.assertEqual(out_h.fn, "plot.png")
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
