import click, os, tempfile, unittest
from click.testing import CliRunner
from unittest.mock import MagicMock, patch

from cw.conf import CromwellConf
import cw.wf
from tests.test_cw_base import BaseWithDb

class CwWfTest(BaseWithDb):

    def test_wf_cli(self):
        runner = CliRunner()
        from cw.wf import cli

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
        from cw.wf import list_cmd as cmd
        runner = CliRunner()

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cmd, [], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"No workflows found in db"
        self.assertEqual(result.output, expected_output)

    def test12_add_cmd(self):
        from cw.wf import add_cmd as cmd
        runner = CliRunner()
        os.chdir(self.temp_d.name)

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cmd, [])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(cmd, ["d10d2b6b-7f7e-4b20-a5dc-d4d0388e6d1a", "sample1"], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""Add workflow test {__file__} {__file__}
"""

    def test13_list_cmd(self):
        from cw.wf import list_cmd as cmd
        runner = CliRunner()

        result = runner.invoke(cmd, [], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""WF_ID                                 NAME     STATUS      PIPELINE
------------------------------------  -------  --------  ----------
d10d2b6b-7f7e-4b20-a5dc-d4d0388e6d1a  sample1  new                0
"""
        self.assertEqual(result.output, expected_output)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
