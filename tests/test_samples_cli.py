import unittest
from click.testing import CliRunner

from tests.test_base_classes import TestBaseWithDb

class SamplesCliTest(TestBaseWithDb):
    def test_samples_cli(self):
        from mgi.cli import cli
        from mgi.samples.cli import samples_cli

        runner = CliRunner()

        result = runner.invoke(samples_cli, [])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(samples_cli, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["samples"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["samples", "-h"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["samples", "--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["samples", "add", "-h"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["samples", "add", "--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["samples", "add"])
        self.assertEqual(result.exit_code, 2)

    def test_samples_add_cmd(self):
        from mgi.samples.cli import add_cmd as cmd
        runner = CliRunner()
        expected_output = "Added 1 of 1 samples."

# -- SamplesCliTestTest

if __name__ == '__main__':
    unittest.main(verbosity=2)
