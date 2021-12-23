import unittest
from click.testing import CliRunner

from mgi.cli import cli as mgi_cli
from mgi.samples.cli import samples_cli

class SamplesTest(unittest.TestCase):
    def test_samples_cli(self):
        runner = CliRunner()

        result = runner.invoke(samples_cli, [])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(samples_cli, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(mgi_cli, ["samples"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(mgi_cli, ["samples", "-h"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(mgi_cli, ["samples", "--help"])
        self.assertEqual(result.exit_code, 0)
# -- SamplesTest

if __name__ == '__main__':
    unittest.main(verbosity=2)
