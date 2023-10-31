import click, io, os, sys, tempfile, unittest
from click.testing import CliRunner

class MetricsSeqlendistCmdTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "metrics")
        self.fastq_fn = os.path.join(self.data_dn, "test.25.fastq.gz")
        self.temp_d = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_d.cleanup()

    def test_seqlendist_cmd(self):
        from cig.metrics.seqlendist.cmd import seqlendist_cmd as cmd
        runner = CliRunner()

        out_n = os.path.join(self.temp_d.name, "TEST")
        out_fns = dict()
        for ext in ("csv", "txt", "png"):
            out_fns[ext] = os.path.join(out_n + "." + ext)
        for ext, fn in out_fns.items():
            self.assertFalse(os.path.exists(fn))

        result = runner.invoke(cmd, ["-o", out_n, "-r", "csv", "-r", "plot", "-r", "text", self.fastq_fn], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        for ext, fn in out_fns.items():
            print(f"{ext} {fn}")
            self.assertTrue(os.path.exists(fn))
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
