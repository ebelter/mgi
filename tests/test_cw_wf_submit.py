import click, io, os, requests, subprocess, sys, tempfile, unittest
from pathlib import Path
from click.testing import CliRunner
from unittest.mock import MagicMock, patch

from tests.test_cw_base import BaseWithDb
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
    @patch("requests.get")
    def test1_submit_wf(self, requests_p, co_p):
        import cw
        from cw.wf_submit import submit_wf

        pipeline = cw.Pipeline.query.get(1)
        self.assertTrue(pipeline)

        # Server not running
        out = io.StringIO()
        sys.stdout = out
        co_p.return_value = True
        requests_p.return_value = MagicMock(ok=False, content="1")

        rv = submit_wf(pipeline, self.wf_inputs)
        self.assertEqual(rv, None)
        out.seek(0)
        self.assertRegex(f"{out.read()}", "Cromwell server is not running")
        co_p.assert_not_called()
        
        # Success
        out = io.StringIO()
        sys.stdout = out
        requests_p.return_value = MagicMock(ok=True, content="1")

        rv = submit_wf(pipeline, self.wf_inputs)
        out.seek(0)
        self.assertEqual(bool(rv), co_p.return_value)
        self.assertEqual(f"{out.read()}", "")
        server = cw.server.server_factory()
        co_p.assert_called_with(["java", "-jar", "/apps/cromwell/cromwell.jar", "submit", pipeline.wdl, "-i", self.wf_inputs, "--host", server.url()])

        sys.stdout = sys.__stdout__

    def test3_resolve_wf_id_from_submit_output(self):
        from cw.wf_submit import resolve_wf_id_from_submit_output
        wf_id = resolve_wf_id_from_submit_output(self.co_output)
        self.assertEqual(wf_id, self.wf_id)

    @patch("subprocess.check_output")
    @patch("requests.get")
    def test4_submit_cmd(self, requests_p, co_p):
        import cw
        from cw.wf_submit import submit_cmd as cmd
        runner = CliRunner()

        pipeline = cw.Pipeline.query.get(1)
        self.assertTrue(pipeline)
        co_p.return_value = self.co_output
        requests_p.return_value = MagicMock(ok=True, content="1")

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cmd, [self.wf_name, self.p_name, self.wf_inputs], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""
"""
        #self.assertEqual(result.output, expected_output)
        # 2022-07-04 21:22:30,283 cromwell-system-akka.dispatchers.api-dispatcher-49 INFO  - Unspecified type (Unspecified version) workflow 5724eb84-cbf5-422b-ac77-4b6790a26bdc submitted

        requests_p.assert_called()
        co_p.assert_called()
        wf = cw.Workflow.query.filter(cw.Workflow.wf_id == self.wf_id).one_or_none()
        self.assertTrue(wf)
        self.assertEqual(wf.inputs, self.wf_inputs)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
