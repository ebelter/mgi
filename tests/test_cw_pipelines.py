import click, os, requests, subprocess, tempfile, time, unittest, yaml
from click.testing import CliRunner
from unittest.mock import MagicMock, patch

from cw.conf import CromwellConf
from tests.test_cw_base import BaseWithDb

class CwServerTest(BaseWithDb):

    def test_pipelines_cli(self):
        runner = CliRunner()
        from cw.pipelines import cli

        result = runner.invoke(cli, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, [])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["add", "--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["add"])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(cli, ["list", "--help"])
        self.assertEqual(result.exit_code, 0)

    def test11_list_cmd(self):
        from cw.pipelines import list_cmd as cmd
        runner = CliRunner()

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cmd, [], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"No pipelines found in pipleines db"
        self.assertEqual(result.output, expected_output)

    def test12_add_cmd(self):
        from cw.pipelines import add_cmd as cmd
        runner = CliRunner()
        os.chdir(self.temp_d.name)

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cmd, [])
        self.assertEqual(result.exit_code, 2)

        with self.assertRaisesRegex(Exception, f"FAILED to add pipeline: WDL file <blah.wdl> does not exist"):
            runner.invoke(cmd, ["test", "blah.wdl", "-i", "blah.zip"], catch_exceptions=False)
        with self.assertRaisesRegex(Exception, f"FAILED to add pipeline: Imports file <blah.zip> does not exist"):
            runner.invoke(cmd, ["test", __file__, "-i", "blah.zip"], catch_exceptions=False)

        result = runner.invoke(cmd, ["test", __file__, "-i", __file__], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""Add pipeline test {__file__} {__file__}
"""

    def test13_list_cmd(self):
        from cw.pipelines import list_cmd as cmd
        runner = CliRunner()

        result = runner.invoke(cmd, [], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""NAME    WDL                                               IMPORTS
------  ------------------------------------------------  ---------
test    /home/ebelter/dev/mgi/tests/test_cw_pipelines.py
"""
        self.assertEqual(result.output, expected_output)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
