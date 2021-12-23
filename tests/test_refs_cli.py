import unittest
from click.testing import CliRunner

from tests.test_base_classes import TestBaseWithDb

class RefsCliTest(TestBaseWithDb):
    def test_refs_cli(self):
        from mgi.cli import cli
        from mgi.refs.cli import refs_cli

        runner = CliRunner()

        result = runner.invoke(refs_cli, [])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(refs_cli, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["refs"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["refs", "-h"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["refs", "--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["refs", "add", "-h"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["refs", "add", "--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["refs", "add"])
        self.assertEqual(result.exit_code, 2)

    def test_refs_add_cmd(self):
        from mgi.refs.cli import add_cmd as cmd
        runner = CliRunner()
        expected_output = "Added 1 of 1 refs."

# -- RefsCliTestTest

if __name__ == '__main__':
    unittest.main(verbosity=2)
