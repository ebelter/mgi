import click, os, requests, subprocess, tempfile, time, unittest, yaml
from click.testing import CliRunner
from unittest.mock import MagicMock, patch

from tests.test_cw_base import BaseWithDb

class Pipelinestest(BaseWithDb):

    def setUp(self):
        self.pipeline_name = "__TESTER__"

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

        with self.assertRaisesRegex(Exception, f"Feature <wdl> is a file, but given value <blah.wdl> does not exist"):
            runner.invoke(cmd, ["name="+self.pipeline_name, "wdl=blah.wdl", "imports=blah.zip"], catch_exceptions=False)
        with self.assertRaisesRegex(Exception, f"Feature <imports> is a file, but given value <blah.zip> does not exist"):
            runner.invoke(cmd, ["name="+self.pipeline_name, "wdl="+__file__, "imports=blah.zip"], catch_exceptions=False)
        with self.assertRaisesRegex(Exception, f"Feature <outputs> is a file, but given value <blah.yaml> does not exist"):
            runner.invoke(cmd, ["name="+self.pipeline_name, "wdl="+__file__, "imports="+__file__, "outputs=blah.yaml"], catch_exceptions=False)

        result = runner.invoke(cmd, ["name="+self.pipeline_name, "wdl="+__file__, "imports="+__file__], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""Add pipeline {self.pipeline_name} {__file__} {__file__}
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
        expected_output = f"""NAME        WDL                                               IMPORTS
----------  ------------------------------------------------  ------------------------------------------------
__TESTER__  /home/ebelter/dev/mgi/tests/test_cw_pipelines.py  /home/ebelter/dev/mgi/tests/test_cw_pipelines.py
"""
        self.assertEqual(result.output, expected_output)

    def test14_update_cmd(self):
        from cw import db, Pipeline
        from cw.pipelines import update_cmd as cmd
        runner = CliRunner()
        os.chdir(self.temp_d.name)

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cmd, [])
        self.assertEqual(result.exit_code, 2)

        pipeline_id = "1"
        p = Pipeline.query.get(int(pipeline_id))
        self.assertTrue(p)
        self.assertEqual(p.name, self.pipeline_name)

        pipeline_new_name = "__NEW__"
        result = runner.invoke(cmd, [pipeline_id, f"name={pipeline_new_name}"], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""Update pipeline <1>
ATTR    FROM        TO
------  ----------  -------
name    __TESTER__  __NEW__
"""
        self.assertEqual(result.output, expected_output)
        db.session.refresh(p)
        self.assertEqual(p.name, pipeline_new_name)

if __name__ == '__main__':
    unittest.main(verbosity=2)
