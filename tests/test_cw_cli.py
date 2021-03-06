import click, unittest
from click.testing import CliRunner

from cw.cli import cli

class CwCliTest(unittest.TestCase):
    def test_cromulent_cli(self):
        runner = CliRunner()

        result = runner.invoke(cli, [])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["-h"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["heartbeat", "--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["outputs", "--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["outputs"])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(cli, ["printc", "--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["server", "--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["setup", "--help"])
        self.assertEqual(result.exit_code, 0)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
