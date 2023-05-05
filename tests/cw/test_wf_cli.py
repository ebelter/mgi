import click, os, tempfile, unittest
from click.testing import CliRunner
from unittest.mock import MagicMock, patch

from tests.cw.test_base import BaseWithDb
class CwWfTest(BaseWithDb):

    def _setUpClass(self):
        from cw import db, Workflow
        wf = Workflow.query.get(1)
        self.wf_name = wf.name
        self.wf_wf_id = wf.wf_id
        self.wf_inputs = wf.inputs

    def test_wf_cli(self):
        runner = CliRunner()
        from cw.wf_cli import cli

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

        result = runner.invoke(cli, ["list", "--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["outputs", "--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["status", "--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["status"])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(cli, ["update", "--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["update"])
        self.assertEqual(result.exit_code, 2)

    @patch("cw.server.server_factory")
    def test11_list_cmd(self, factory_p):
        from cw import appcon, db, Workflow
        from cw.wf_cli import list_cmd as cmd
        runner = CliRunner()

        server_host = "compute1-exec-225.ris.wustl.edu"
        server_port = "8888"
        appcon.set(group="server", name="host", value=server_host)
        appcon.set(group="server", name="port", value=server_port)
        server = MagicMock(host=server_host, port=server_port, server_url=f"http://{server_host}:{server_port}", **{"is_running.return_value": True, "status_for_workflow": "Running"})
        factory_p.return_value = server

        wf = Workflow.query.get(1)
        db.session.delete(wf)
        db.session.commit()

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
        from cw import Pipeline
        from cw.wf_cli import add_cmd as cmd
        runner = CliRunner()
        pipeline = Pipeline.query.get(1)

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cmd, [])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(cmd, [f"wf_id={self.wf_wf_id}", f"name={self.wf_name}", f"pipeline={str(pipeline.id)}", f"inputs={__file__}"], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""Add workflow 1 {self.wf_wf_id} {self.wf_name} new {pipeline.name}
"""
        self.assertEqual(result.output, expected_output)

    @patch("cw.server.server_factory")
    def test13_list_cmd(self, factory_p):
        from cw import appcon, Workflow
        from cw.wf_cli import list_cmd as cmd
        runner = CliRunner()

        server_host = "compute1-exec-225.ris.wustl.edu"
        server_port = "8888"
        appcon.set(group="server", name="host", value=server_host)
        appcon.set(group="server", name="port", value=server_port)
        server = MagicMock(host=server_host, port=server_port, server_url=f"http://{server_host}:{server_port}", **{"is_running.return_value": True, "status_for_workflow.return_value": "new"})
        factory_p.return_value = server

        wf = Workflow.query.get(1)
        self.assertTrue(wf)

        result = runner.invoke(cmd, [], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""WF_ID                                 NAME              STATUS    PIPELINE     INPUTS
------------------------------------  ----------------  --------  -----------  ---------------------------------------------
{self.wf_wf_id}  {self.wf_name}  new       hello-world  {__file__}
"""
        self.assertEqual(result.output, expected_output)

    def test14_update_cmd(self):
        from cw import db, Workflow
        from cw.wf_cli import update_cmd as cmd
        runner = CliRunner()

        wf = Workflow.query.get(1)
        self.assertTrue(wf)

        old_name = wf.name
        new_name = "test.hello_world"
        result = runner.invoke(cmd, [str(wf.id), f"name={new_name}"], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""Update workflow <1>
ATTR    FROM              TO
------  ----------------  ----------------
name    {old_name}  {new_name}
"""
        self.assertEqual(result.output, expected_output)
        db.session.refresh(wf)
        self.assertEqual(wf.name, new_name)

if __name__ == '__main__':
    unittest.main(verbosity=2)
