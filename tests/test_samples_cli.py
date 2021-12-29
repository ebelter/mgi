import os, unittest
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

        result = runner.invoke(cli, ["samples", "list", "-h"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["samples", "list", "--help"])
        self.assertEqual(result.exit_code, 0)

    def test_add_cmd(self):
        from mgi.samples.cli import add_cmd as cmd
        runner = CliRunner()
        expected_output = "Added 1 of 1 samples."

    def _filter_failures(self, list_cmd):
        runner = CliRunner()

        result = runner.invoke(list_cmd, ["blah=blah"])
        self.assertEqual(result.exit_code, 1)
        self.assertTrue(result.exception)

        result = runner.invoke(list_cmd, ["name"])
        self.assertEqual(result.exit_code, 1)
        self.assertTrue(result.exception)

        result = runner.invoke(list_cmd, ["name="])
        self.assertEqual(result.exit_code, 1)
        self.assertTrue(result.exception)

    def test_list_cmd(self):
        from mgi.samples.cli import list_cmd as cmd
        runner = CliRunner()

        result = runner.invoke(cmd, ["blah=blah"])
        self.assertEqual(result.exit_code, 1)
        self.assertTrue(result.exception)

        # FILTER FAILURES
        result = runner.invoke(cmd, ["blah=blah"])
        self.assertEqual(result.exit_code, 1)
        self.assertTrue(result.exception)

        result = runner.invoke(cmd, ["name"])
        self.assertEqual(result.exit_code, 1)
        self.assertTrue(result.exception)

        result = runner.invoke(cmd, ["name="])
        self.assertEqual(result.exit_code, 1)
        self.assertTrue(result.exception)

        # ALL
        result = runner.invoke(cmd, [])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = """NAME    SETS
------  ------
H_G002  hic"""
        self.assertEqual(result.output, expected_output)

    def test_samples_paths_cli(self):
        from mgi.cli import cli
        from mgi.samples.cli import samples_cli
        runner = CliRunner()

        result = runner.invoke(samples_cli, ["paths", "--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(samples_cli, ["paths"])
        self.assertEqual(result.exit_code, 0)
 
        result = runner.invoke(samples_cli, ["paths", "update", "--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(samples_cli, ["paths", "update"])
        self.assertEqual(result.exit_code, 2)

    def test_samples_paths_update_cmd(self):
        from mgi.samples.cli import samples_paths_update_cmd as cmd
        from mgi.models import EntityPath
        runner = CliRunner()

        fn = os.path.join(self.temp_d.name, "paths.tsv")
        value = "/mnt/data/sample_111.bam"
        with open(fn, "w") as f:
            f.write("\t".join([value])+"\n")

        result = runner.invoke(cmd, [fn])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = """Done. Added 1 and updated 0 of 1 given paths.
"""
        self.assertEqual(result.output, expected_output)
        ep = EntityPath.query.filter(EntityPath.value == value).one_or_none()
        self.assertTrue(ep)

# -- SamplesCliTestTest

if __name__ == '__main__':
    unittest.main(verbosity=2)
