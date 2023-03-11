import click, io, os, subprocess, sys, tempfile, unittest
from pathlib import Path
from click.testing import CliRunner
from unittest.mock import MagicMock, Mock, patch

from tests.cw.test_base import BaseWithDb
class CwWfTest(BaseWithDb):
    def setUp(self):
        import cw
        self.server_host = "compute1-exec-225.ris.wustl.edu"
        cw.appcon.set(group="server", name="host", value=self.server_host)
        self.server_port = "8888"
        cw.appcon.set(group="server", name="port", value=self.server_port)

        self.wf_name = "SAMPLE-align"
        self.p_name = "align"
        self.p_wdl = os.path.join(self.temp_d.name, "align.wdl")
        Path(self.p_wdl).touch()
        self.wf_inputs = os.path.join(self.temp_d.name, "align.inputs.json")
        Path(self.wf_inputs).touch()
        self.co_output = "[2022-05-18 10:56:51,19] [info] Slf4jLogger started\n[2022-05-18 10:56:52,14] [info] Workflow e933af86-b64c-43b2-abcc-1241e8d7e69a submitted to http://compute1-exec-226.ris.wustl.edu:8888\n".encode()
        self.wf_id = "e933af86-b64c-43b2-abcc-1241e8d7e69a"

    def test0_submit_fails(self):
        import cw
        from cw.wf_submit import submit_cmd as cmd
        runner = CliRunner()

        result = runner.invoke(cmd, [])
        self.assertEqual(result.exit_code, 2)
        result = runner.invoke(cmd, [self.wf_name])
        self.assertEqual(result.exit_code, 2)
        result = runner.invoke(cmd, [self.wf_name, self.p_name])
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(cmd, [self.wf_name, self.p_name, "INPUTS"])
        self.assertEqual(result.exit_code, 1)
        self.assertRegex(result.output, "Failed to find pipeline")

        p = cw.Pipeline(name=self.p_name, wdl=self.p_wdl)
        cw.db.session.add(p)
        cw.db.session.commit()

        result = runner.invoke(cmd, [self.wf_name, self.p_name, "INPUTS"])
        self.assertEqual(result.exit_code, 1)
        self.assertRegex(result.output, "Inputs json")

    @patch("subprocess.check_output")
    @patch("cw.server.server_factory")
    def test1_submit_wf(self, server_p, co_p):
        import cw
        from cw.wf_submit import submit_wf

        server = Mock()
        server_p.return_value = server
        co_p.return_value = True
        pipeline = cw.Pipeline.query.get(1)
        self.assertTrue(pipeline)

        # Server not running
        server.configure_mock(**{"is_running.return_value": False})
        out = io.StringIO()
        sys.stdout = out

        rv = submit_wf(pipeline, self.wf_inputs)
        self.assertEqual(rv, None)
        out.seek(0)
        self.assertRegex(f"{out.read()}", "Cromwell server is not running")
        co_p.assert_not_called()
        
        # Success
        server.configure_mock(**{"is_running.return_value": True, "url.return_value": "__URL__"})
        out.truncate(0)

        rv = submit_wf(pipeline, self.wf_inputs)
        self.assertEqual(rv, co_p.return_value)
        out.seek(0)
        self.assertEqual(f"{out.read()}", "")
        co_p.assert_called_once()
        co_p.assert_called_with(["java", "-jar", "/apps/cromwell/cromwell.jar", "submit", pipeline.wdl, "-i", self.wf_inputs, "--host", server.url()])
        sys.stdout = sys.__stdout__

    def test3_resolve_wf_id_from_submit_output(self):
        from cw.wf_submit import resolve_wf_id_from_submit_output
        wf_id = resolve_wf_id_from_submit_output(self.co_output)
        self.assertEqual(wf_id, self.wf_id)

    @patch("subprocess.check_output")
    @patch("cw.server.server_factory")
    def test4_submit_cmd(self, server_p, co_p):
        import cw
        from cw.wf_submit import submit_cmd as cmd
        runner = CliRunner()

        pipeline = cw.Pipeline.query.get(1)
        self.assertTrue(pipeline)
        server = Mock()
        server_p.return_value = server
        server.configure_mock(**{"is_running.return_value": True, "url.return_value": "__URL__", "status_for_workflow.return_value": "running"})
        co_p.return_value = self.co_output

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cmd, [self.wf_name, self.p_name, self.wf_inputs], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""Pipeline:    {self.p_name}
Inputs json: {self.wf_inputs}
{self.co_output.decode()}Workflow {self.wf_id} submitted, waiting for it to start...
Current workflow status: running
Workflow status: running
Workflow is running and saved DB!
"""
        self.assertEqual(result.output, expected_output)
        wf = cw.Workflow.query.filter(cw.Workflow.wf_id == self.wf_id).one_or_none()
        self.assertTrue(wf)
        self.assertEqual(wf.inputs, self.wf_inputs)
        self.assertEqual(server_p.call_count, 2)
        self.assertEqual(co_p.call_count, 1)

    @patch("time.sleep")
    @patch("cw.server.server_factory")
    def test4_wait_for_workflow_to_start(self, server_p, sleep_p):
        import sys, io
        from cw.wf_submit import wait_for_workflow_to_start as fun
        sys.stdout = io.StringIO()
        server = Mock()
        server_p.return_value = server

        # WF Never Runs
        server.configure_mock(**{"status_for_workflow.return_value": "submitted"})
        status = fun("__WF_ID__")
        self.assertEqual(status, "submitted")
        self.assertEqual(server.status_for_workflow.call_count, 10)
        self.assertEqual(sleep_p.call_count, 11)

        server.reset_mock()
        sleep_p.reset_mock()

        # WF is Running
        server.configure_mock(**{"status_for_workflow.return_value": "running"})
        status = fun("__WF_ID__")
        self.assertEqual(status, "running")
        self.assertEqual(server.status_for_workflow.call_count, 1)
        self.assertEqual(sleep_p.call_count, 1)
        sleep_p.reset_mock()

        sys.stdout = sys.__stdout__
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
