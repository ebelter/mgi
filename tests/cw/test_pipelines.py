import click, os, requests, subprocess, tempfile, time, unittest, yaml
from click.testing import CliRunner
from unittest.mock import MagicMock, patch

from tests.cw.test_base import BaseWithDb
class Pipelinestest(BaseWithDb):

    def setUp(self):
        self.pipeline_name = "hello-world"

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

        result = runner.invoke(cli, ["detail", "--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["detail"])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(cli, ["inputs", "--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["inputs"])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(cli, ["list", "--help"])
        self.assertEqual(result.exit_code, 0)

    def test111_detail_cmd(self):
        from cw.pipelines import detail_cmd as cmd
        runner = CliRunner()

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cmd, ["1"], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        self.maxDiff = 100000
        expected_output = f"""Name:     hello-world
WDL:      /home/ebelter/dev/mgi/wdl/hello-world/hello_world.wdl
Inputs:   /home/ebelter/dev/mgi/wdl/hello-world/hello_world.inputs.json
Outputs:  /home/ebelter/dev/mgi/wdl/hello-world/hello_world.outputs.yaml
"""
        self.assertEqual(result.output, expected_output)

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
        expected_output = f"""NAME         WDL
-----------  -----------------------------------------------------
hello-world  /home/ebelter/dev/mgi/wdl/hello-world/hello_world.wdl
"""
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

        new_name = "__TESTER__"
        result = runner.invoke(cmd, ["name="+new_name, "wdl="+__file__, "imports="+__file__], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""Add pipeline {new_name} {__file__} {__file__}
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
        expected_output = f"""NAME\s+WDL\n"""
        self.assertRegex(result.output, expected_output)

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

        new_name = "hello_world"
        result = runner.invoke(cmd, ["hello-world", f"name={new_name}"], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""Update pipeline <hello-world>
ATTR    FROM         TO
------  -----------  -----------
name    hello-world  {new_name}
"""
        self.assertEqual(result.output, expected_output)
        db.session.refresh(p)
        self.assertEqual(p.name, new_name)

if __name__ == '__main__':
    unittest.main(verbosity=2)
