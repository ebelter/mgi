import click, unittest
from click.testing import CliRunner

from cw.cli import cli

class CwCliTest(unittest.TestCase):
    def test_cw_cli(self):
        runner = CliRunner()

        result = runner.invoke(cli, [])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["-h"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["pipelines", "--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["pipelines",])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["server", "--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["server",])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["setup", "--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["setup"])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(cli, ["wf", "--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["wf",])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["utils", "--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["utils",])
        self.assertEqual(result.exit_code, 0)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
