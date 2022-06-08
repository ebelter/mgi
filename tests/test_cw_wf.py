import click, os, tempfile, unittest
from click.testing import CliRunner
from unittest.mock import MagicMock, patch

from tests.test_cw_base import BaseWithDb
class CwWfTest(BaseWithDb):

    def _setUpClass(self):
        from cw import db, Pipeline
        self.wf_id = 10001
        self.wf_name = "__SAMPLE__"
        self.wf_wf_id = "__WFID__"

        p = Pipeline(name="__TESTER__", wdl=__file__, imports=None, outputs=None)
        db.session.add(p)
        db.session.commit()
        self.pipeline = p

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

        result = runner.invoke(cli, ["outputs", "--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["update", "--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["update"])
        self.assertEqual(result.exit_code, 2)

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

        result = runner.invoke(cmd, [f"wf_id={self.wf_wf_id}", f"name={self.wf_name}", f"pipeline={str(self.pipeline.id)}"], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""Add workflow 1 {self.wf_wf_id} {self.wf_name} new {self.pipeline.name}
"""
        self.assertEqual(result.output, expected_output)

    def test13_list_cmd(self):
        from cw.wf import list_cmd as cmd
        runner = CliRunner()

        result = runner.invoke(cmd, [], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""WF_ID     NAME        STATUS    PIPELINE
--------  ----------  --------  ----------
{self.wf_wf_id}  {self.wf_name}  new       {self.pipeline.name}
"""
        self.assertEqual(result.output, expected_output)

    def test14_update_cmd(self):
        from cw import db, Workflow
        from cw.wf import update_cmd as cmd
        runner = CliRunner()
        #os.chdir(self.temp_d.name)

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cmd, [])
        self.assertEqual(result.exit_code, 2)

        wf = Workflow.query.get(1)
        self.assertTrue(wf)

        new_name = "__SAMPLE2__"
        result = runner.invoke(cmd, [str(wf.id), f"name={new_name}"], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""Update workflow <1>
ATTR    FROM        TO
------  ----------  -----------
name    {self.wf_name}  {new_name}
"""
        self.assertEqual(result.output, expected_output)
        db.session.refresh(wf)
        self.assertEqual(wf.name, new_name)

if __name__ == '__main__':
    unittest.main(verbosity=2)
