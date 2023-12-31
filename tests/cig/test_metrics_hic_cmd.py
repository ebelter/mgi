import click, os, tempfile, unittest
from click.testing import CliRunner

class MetricsHicCmdTest(unittest.TestCase):
    def setUp(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data", "metrics")
        self.statsfile = os.path.join(self.data_dn, "hic.stats.json")
        self.temp_d = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_d.cleanup()

    def test1_cmd(self):
        from cig.metrics.hic.cmd import hic_cmd as cmd
        runner = CliRunner()

        out_n = os.path.join(self.temp_d.name, "PAN001")
        result = runner.invoke(cmd, ["-r", "csv", "-l", "sample1,sample1", "-o", out_n, self.statsfile, self.statsfile], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        self.assertTrue(os.path.exists(out_n+".csv"))
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
