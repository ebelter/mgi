import click, io, os, sys, tempfile, unittest
from click.testing import CliRunner

class MetricsSeqlendistCmdTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "metrics")
        self.fastq_fn = os.path.join(self.data_dn, "test.25.fastq.gz")
        self.temp_d = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_d.cleanup()

    def test0_seqlendist_resolve_labels(self):
        from cig.metrics.seqlendist.cmd import resolve_labels as fun
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

    def test1_seqlendist_cmd(self):
        from cig.metrics.seqlendist.cmd import seqlendist_cmd as cmd
        runner = CliRunner()

        out_n = os.path.join(self.temp_d.name, "TEST")
        out_fns = dict()
        report_types = ("csv", "json", "png", "text", "yaml")
        report_params = []
        for report_type in report_types:
            out_fns[report_type] = os.path.join(out_n + "." + report_type)
            report_params.extend(["-r", report_type])
        for ext, fn in out_fns.items():
            self.assertFalse(os.path.exists(fn))

        result = runner.invoke(cmd, report_params + ["-o", out_n, self.fastq_fn], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        for ext, fn in out_fns.items():
            #print(f"{ext} {fn}")
            self.assertTrue(os.path.exists(fn))
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
