import click, os, sys, unittest

class MetricsHelpersTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "metrics")

    def test_str_to_number_if_number(self):
        from cig.metrics.helpers import str_to_number_if_number as fun
        self.assertEqual(fun("NUM"), "NUM")
        self.assertEqual(fun("2"), 2)
        self.assertEqual(fun("2.2"), 2.20)
        self.assertEqual(fun("2.229"), 2.23)

    def test_str_to_number(self):
        from cig.metrics.helpers import str_to_number
        # FIXME test passing non numbers?
        self.assertEqual(str_to_number("2"), 2)
        self.assertEqual(str_to_number("2.2"), 2.20)
        self.assertEqual(str_to_number("2.229"), 2.23)

    def test_str_to_number(self):
        from cig.metrics.helpers import number_to_str as fun
        self.assertEqual(fun("2"), "2")
        self.assertEqual(fun("2.2"), "2.2")
        self.assertEqual(fun(2), "2")
        self.assertEqual(fun(2.00), "2")
        self.assertEqual(fun(2.01), "2.01")

    def test_resolve_labels(self):
        from cig.metrics.helpers import resolve_labels as fun
        labels = fun("a-b", ["seqfile1"], None)
        self.assertEqual(labels, ["a-b"])
        labels = fun("a,b", ["seqfile1", "seqfile2"], None)
        self.assertEqual(labels, ["a", "b"])
        # Get labels from out
        labels = fun(None, ["/data/a.txt", "/data/b.txt", "/data/a.txt"], "test")
        self.assertEqual(labels, ["test", "test", "test"])
        # Get labels from seqfile basename
        labels = fun(None, ["/data/a.txt", "/data/b.txt", "/data/a.txt"], None)
        self.assertEqual(labels, ["a", "b", "a"])

        with self.assertRaisesRegex(Exception, "ERROR Unequal number of labels"):
            fun("a-b", ["seqfile1", "seqfile2"], None)

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
