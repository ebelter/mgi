import click, os, tempfile, unittest
from click.testing import CliRunner

class MetricsRnaseqCmdTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "metrics")
        self.statsfile = os.path.join(self.data_dn, "rnaseq.metrics")
        self.statsfile_dep = os.path.join(self.data_dn, "rnaseq.dep.metrics")
        self.temp_d = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_d.cleanup()

    def test1_cmd(self):
        from cig.metrics.rnaseq.cmd import rnaseq_cmd as cmd
        runner = CliRunner()

        out_n = os.path.join(self.temp_d.name, "PAN001")
        result = runner.invoke(cmd, ["-r", "table", "-l", "PAN001,PAN001", "-o", out_n, self.statsfile, self.statsfile_dep], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        self.assertTrue(os.path.exists(out_n+".table"))
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
