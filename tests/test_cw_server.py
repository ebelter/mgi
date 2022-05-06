import click, os, requests, subprocess, tempfile, time, unittest, yaml
from click.testing import CliRunner
from unittest.mock import MagicMock, patch

from cw.conf import CromwellConf
import cw.cromshell, cw.server, subprocess

class CwServerTest(unittest.TestCase):
    def setUp(self):
        from cw.setup_cmd import setup_cmd as cmd
        self.temp_d = tempfile.TemporaryDirectory()
        os.chdir(self.temp_d.name)
        cc = CromwellConf(CromwellConf.default_attributes())
        cc.setattr("LSF_QUEUE", "general")
        cc.setattr("LSF_JOB_GROUP", "job")
        cc.setattr("LSF_USER_GROUP", "user")
        cc.save()
        self.cc = cc
        cc.setup()
        self.server_job_id = "1234"
        self.server_host = "compute1-exec-225.ris.wustl.edu"
        self.server_url = f"http://{self.server_host}:8888"

    def tearDown(self):
        self.temp_d.cleanup()

    def test_server_cli(self):
        runner = CliRunner()
        from cw.server import cli

        result = runner.invoke(cli, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, [])
        self.assertEqual(result.exit_code, 0)

    @patch("requests.get")
    def test_server_is_running(self, requests_p):
        from cw.server import server_is_running as fun
        requests_p.return_value = MagicMock(ok=True, content="1")
        url = "http://host:port"
        self.cc.setattr("CROMWELL_URL", url)
        rv = fun(self.cc)
        requests_p.assert_called_with(url)
        self.assertTrue(rv)

        requests_p.return_value = MagicMock(ok=False, content="1")
        rv = fun(self.cc)
        self.assertFalse(rv)

    @patch("subprocess.check_output")
    def test_start_server(self, co_p):
        from cw.server import start_server as fun
        co_p.return_value = f"Job <{self.server_job_id}> is submitted to queue <general>.\n".encode()
        self.assertEqual(fun(self.cc), self.server_job_id)
        co_p.return_value = b"Job not submitted"
        with self.assertRaisesRegex(Exception, "Failed to parse LSF bsub command output to get job id: "):
            fun(self.cc)

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

    @patch("cw.server.server_is_running")
    @patch("cw.server.start_server")
    @patch("cw.server.wait_for_host")
    @patch("cw.cromshell.config_dn")
    def test_start_cmd(self, dn_p, wait_p, start_p, running_p):
        from cw.server import start_cmd as cmd
        runner = CliRunner()

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        running_p.return_value = False
        start_p.return_value = self.server_job_id
        host = "compute1-exec-225.ris.wustl.edu"
        wait_p.return_value = host
        url = f"http://{host}:8888"
        dn_p.return_value = "/blah"

        os.chdir(self.temp_d.name)
        result = runner.invoke(cmd, [], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""Waiting for job <{self.server_job_id}> to start to obtain HOST...
Server running on <{host}> port <8888>
Updating YAML file <cw.yaml>
No cromshell directory at </blah> detected, not updating url
Server ready!
"""
        self.assertEqual(result.output, expected_output)

        with open(self.cc.yaml_fn(), "r") as f:
            updated_attrs = yaml.safe_load(f)
        self.assertEqual(updated_attrs["CROMWELL_JOB_ID"], self.server_job_id)
        self.assertEqual(updated_attrs["CROMWELL_HOST"], host)
        self.assertEqual(updated_attrs["CROMWELL_URL"], url)

        # Try to run while server already running
        running_p.return_value = True
        result = runner.invoke(cmd, [], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""Server is already up and running at <{url}>
"""
        self.assertEqual(result.output, expected_output)

    @patch("subprocess.call")
    def test_stop_cmd(self, call_p):
        from cw.server import stop_cmd as cmd
        runner = CliRunner()

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        # no job id in config
        os.chdir(self.temp_d.name)
        result = runner.invoke(cmd, [], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""No job id found in configuration, cannot stop server
"""
        self.assertEqual(result.output, expected_output)

        self.cc.setattr("CROMWELL_JOB_ID", self.server_job_id)
        self.cc.setattr("CROMWELL_HOST", self.server_host)
        self.cc.setattr("CROMWELL_URL", self.server_url)
        self.cc.save()

        # stop
        result = runner.invoke(cmd, [], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""Server URL: <{self.server_url}>
Stopping job <{self.server_job_id}>
Updating YAML file <{self.cc.yaml_fn()}>
"""
        self.assertEqual(result.output, expected_output)

        with open(self.cc.yaml_fn(), "r") as f:
            updated_attrs = yaml.safe_load(f)
        self.assertEqual(updated_attrs["CROMWELL_JOB_ID"], None)
        self.assertEqual(updated_attrs["CROMWELL_HOST"], None)
        self.assertEqual(updated_attrs["CROMWELL_URL"], None)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
