import glob, os, tempfile, unittest
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
        labels = fun("a-b", ["seqfile1"])
        self.assertEqual(labels, ["a-b"])
        labels = fun("a,b", ["seqfile1", "seqfile2"])
        self.assertEqual(labels, ["a", "b"])
        labels = fun(None, ["/data/a.fasta", "/data/b.fastq", "/data/a.fastq.gz"])
        self.assertEqual(labels, ["a", "b", "a"])

    def test1_seqlendist_cmd(self):
        from cig.metrics.seqlendist.cmd import seqlendist_cmd as cmd
        from cig.metrics.seqlendist.reports import available_reports
        runner = CliRunner()

        out_n = os.path.join(self.temp_d.name, "TEST")
        out_fns = dict()
        report_params = []
        for report_type in available_reports():
            out_fns[report_type] = os.path.join(out_n + "." + report_type)
            report_params.extend(["-r", report_type])
        self.assertEqual(0, len(glob.glob(out_n+"*")))

        result = runner.invoke(cmd, report_params + ["-o", out_n, self.fastq_fn], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        self.assertEqual(len(glob.glob(out_n+"*")), len(available_reports()))
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
