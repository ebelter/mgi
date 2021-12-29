import os, unittest
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

        result = runner.invoke(cli, ["refs", "list", "-h"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["refs", "list", "--help"])
        self.assertEqual(result.exit_code, 0)


    def test_refs_add_cmd(self):
        from mgi.refs.cli import add_cmd as cmd
        runner = CliRunner()
        expected_output = "Added 1 of 1 refs."

    def test_list_cmd(self):
        from mgi.refs.cli import list_cmd as cmd
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
GRCh38"""
        self.assertEqual(result.output, expected_output)

    def test_refs_paths_cli(self):
        from mgi.cli import cli
        from mgi.refs.cli import refs_cli
        runner = CliRunner()

        result = runner.invoke(refs_cli, ["paths", "--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(refs_cli, ["paths"])
        self.assertEqual(result.exit_code, 0)
 
        result = runner.invoke(refs_cli, ["paths", "update", "--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(refs_cli, ["paths", "update"])
        self.assertEqual(result.exit_code, 2)

    def test_refs_paths_update_cmd(self):
        from mgi.refs.cli import refs_paths_update_cmd as cmd
        from mgi.models import EntityPath
        runner = CliRunner()

        fn = os.path.join(self.temp_d.name, "paths.tsv")
        value = "/mnt/data/ref_111.fasta"
        with open(fn, "w") as f:
            f.write("\t".join([value])+"\n")

        result = runner.invoke(cmd, [fn], catch_exceptions=False)
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

# -- RefsCliTestTest

if __name__ == '__main__':
    unittest.main(verbosity=2)
