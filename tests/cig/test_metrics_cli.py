import click, unittest
from click.testing import CliRunner

class MetricsCliTest(unittest.TestCase):
    def test_metrics_cli(self):
        runner = CliRunner()
        from cig.metrics.cli import cli

        result = runner.invoke(cli, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, [])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["alignment", "--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["alignment"])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(cli, ["collate", "--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["collate"])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(cli, ["seqlendist", "--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["seqlendist"])
        self.assertEqual(result.exit_code, 2)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
