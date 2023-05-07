import click, io, json, os, requests, subprocess, sys, tempfile, time, unittest, yaml
from pathlib import Path
from click.testing import CliRunner
from unittest.mock import MagicMock, Mock, patch

from tests.cw.test_base import BaseWithDb

class CwServerTest(BaseWithDb):
    def setUp(self):
        self.server_job_id = "1234"
        self.server_host = "compute1-exec-225.ris.wustl.edu"
        self.server_port = "8888"
        self.server_url = f"http://{self.server_host}:{self.server_port}"

    @patch("requests.get")
    def test_server(self, requests_p):
        from cw.server import server_factory

        server = server_factory()
        self.assertTrue(bool(server))

        # is_running
        # no host
        url = "http://host:port"
        self.assertFalse(server.is_running())
        requests_p.assert_not_called()
        # has host, but not running
        server.host = self.server_host
        requests_p.return_value = MagicMock(ok=False, content="1")
        self.assertFalse(server.is_running())
        requests_p.assert_called_with(server.url())
        # running
        requests_p.return_value = MagicMock(ok=True, content="1")
        self.assertTrue(server.is_running())
        requests_p.assert_called_with(server.url())

    @patch("requests.get")
    def test_server_abort_workflow(self, requests_p):
        from cw.server import server_factory
        server = server_factory()
        self.assertTrue(bool(server))

        stderr = io.StringIO()
        sys.stderr = stderr

        wf_id = "__WF_ID__"
        url = f"{server.url()}/api/workflows/v1/{wf_id}/abort"

        requests_p.return_value = Mock(ok=False)
        with self.assertRaisesRegex(Exception, f"Server error encountered aborting workflow with <{url}>"):
            server.abort_workflow(wf_id)
        requests_p.assert_called_with(url)
        stderr.seek(0, 0)

        stderr.truncate(0)
        response = Mock(ok=True)
        response.configure_mock(**{"json.return_value": {"status": "Aborting", "id": "__WF_ID__"},})
        requests_p.return_value = response
        result = server.abort_workflow(wf_id)
        self.assertEqual(result, "aborting")
        requests_p.assert_called_with(url)
        self.assertEqual(requests_p.call_count, 2)
        stderr.seek(0, 0)
        self.assertEqual(stderr.read(), f"")

    @patch("requests.get")
    def test_server_status_for_workflow(self, requests_p):
        from cw.server import server_factory
        server = server_factory()
        self.assertTrue(bool(server))

        stderr = io.StringIO()
        sys.stderr = stderr

        wf_id = "__WF_ID__"
        url = f"{server.url()}/api/workflows/v1/{wf_id}/status"

        requests_p.return_value = Mock(ok=False)
        status = server.status_for_workflow(wf_id)
        self.assertEqual(status, None)
        requests_p.assert_called_with(url)
        stderr.seek(0, 0)
        self.assertEqual(stderr.read(), f"Failed to get response from server at {url}\n")

        stderr.truncate(0)
        response = Mock(ok=True)
        response.configure_mock(**{"json.return_value": {"status": "Succeeded", "id": "__WF_ID__"},})
        requests_p.return_value = response
        status = server.status_for_workflow(wf_id)
        self.assertEqual(status, "succeeded")
        requests_p.assert_called_with(url)
        self.assertEqual(requests_p.call_count, 2)
        stderr.seek(0, 0)
        self.assertEqual(stderr.read(), f"")

    @patch("requests.get")
    def test_metadata_for_workflow(self, requests_p):
        from cw.server import server_factory
        server = server_factory()
        self.assertTrue(bool(server))
        stderr = io.StringIO()
        sys.stderr = stderr
        wf_id = "__WF_ID__"

        requests_p.return_value = Mock(ok=False)
        status = server.status_for_workflow(wf_id)
        self.assertEqual(status, None)
        requests_p.assert_called()
        stderr.seek(0, 0)

        server.host = self.server_host
        server.port = self.server_port
        requests_p.return_value = None
        with self.assertRaisesRegex(Exception, f"Server error encountered getting metadata with <{server.url()}"):
            server.metadata_for_workflow(wf_id)
        requests_p.assert_called()
        requests_p.reset_mock()

        response = Mock(ok=False)
        response.configure_mock(**{"json.return_value": {"status": "Succeeded", "id": "__WF_ID__"},})
        requests_p.return_value = response
        with self.assertRaisesRegex(Exception, f"Server error encountered getting metadata with <{server.url()}"):
            server.metadata_for_workflow(wf_id)
        requests_p.assert_called()
        requests_p.reset_mock()

        response = Mock(ok=True)
        with open(os.path.join(self.data_dn, "wf", "67c1c73d-9b92-408e-9f7a-5ad0c9df2a36.md"), "r") as f:
            expected_md_s = f.read()
            expected_md = json.loads(expected_md_s)
        response.configure_mock(**{"json.return_value": expected_md})
        requests_p.return_value = response
        metadata = server.metadata_for_workflow(wf_id)
        self.assertDictEqual(metadata, expected_md)
        requests_p.assert_called()

    def test_server_cli(self):
        from cw.server import cli
        runner = CliRunner()
        os.chdir(self.temp_d.name)

        result = runner.invoke(cli, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, [])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["heartbeat", "--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["heartbeat"], catch_exceptions=False)
        self.assertEqual(result.exit_code, 1)

    @patch("subprocess.check_output")
    def test_start_server(self, co_p):
        from cw.server import start_server as fun
        co_p.return_value = f"Job <{self.server_job_id}> is submitted to queue <general>.\n".encode()
        self.assertEqual(fun(), self.server_job_id)
        co_p.return_value = b"Job not submitted"
        with self.assertRaisesRegex(Exception, "Failed to parse LSF bsub command output to get job id: "):
            fun()

    @patch("subprocess.check_output")
    @patch("time.sleep")
    def test_wait_on_host(self, sleep_p, co_p):
        from cw.server import wait_for_host as fun
        co_p.return_value = b"JOBID   USER    STAT  QUEUE      FROM_HOST   EXEC_HOST   JOB_NAME   SUBMIT_TIME\n1234   user RUN   general       compute1-client-3.ris.wustl.edu compute1-exec-225.ris.wustl.edu bash /storage1/fs1/group/user/cw/server/run Mar  7 10:10\n"
        host = fun(self.server_job_id)
        self.assertEqual(host, "compute1-exec-225.ris.wustl.edu")

        co_p.return_value = b"JOBID   USER    STAT  QUEUE      FROM_HOST   EXEC_HOST   JOB_NAME   SUBMIT_TIME\n1234   user PEND   general       compute1-client-3.ris.wustl.edu compute1-exec-225.ris.wustl.edu bash /storage1/fs1/group/user/cw/server/run Mar  7 10:10\n"
        with self.assertRaisesRegex(Exception, "Seems server job is not starting. Fix and try again."):
            fun(self.server_job_id)

        co_p.return_value = b"JOBID   USER    STAT  QUEUE      FROM_HOST   EXEC_HOST   JOB_NAME   SUBMIT_TIME\n1234   user EXIT   general       compute1-client-3.ris.wustl.edu compute1-exec-225.ris.wustl.edu bash /storage1/fs1/group/user/cw/server/run Mar  7 10:10\n"
        with self.assertRaisesRegex(Exception, f"Seems server <{self.server_job_id}> IS DONE/EXIT. Fix and try again!"):
            fun(self.server_job_id)

    @patch("cw.server.server_factory")
    @patch("cw.server.start_server")
    @patch("cw.server.wait_for_host")
    def test_start_cmd(self, wait_p, start_p, factory_p):
        import cw
        from cw import appcon
        from cw.server import start_cmd as cmd
        runner = CliRunner()

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        cw.DN = self.temp_d.name
        os.chdir(self.temp_d.name)
        Path(appcon.get(group="server", name="server_start_fn")).touch()
        server = MagicMock(host=self.server_host, port=self.server_port, url=self.server_url, **{"is_running.return_value": False})
        factory_p.return_value = server
        start_p.return_value = self.server_job_id
        wait_p.return_value = self.server_host
        url = f"http://{self.server_host}:{self.server_port}"
        appcon.set(group="server", name="port", value=self.server_port)

        result = runner.invoke(cmd, [], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""Waiting for job <{self.server_job_id}> to start to obtain HOST...
Server running on <{self.server_host}> port <{self.server_port}>
Updating application configuration...
Server ready!
"""
        self.assertEqual(result.output, expected_output)

        self.assertEqual(appcon.get(group="server", name="job_id"), self.server_job_id)
        self.assertEqual(appcon.get(group="server", name="host"), self.server_host)
        self.assertEqual(appcon.get(group="server", name="url"), self.server_url)

        # Try to run while server already running
        server.is_running.return_value = True
        result = runner.invoke(cmd, [], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""Server is already up and running at <{url}>
"""
        self.assertEqual(result.output, expected_output)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
