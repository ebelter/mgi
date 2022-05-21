import click, os, subprocess, unittest
from click.testing import CliRunner
from unittest.mock import patch

from tests.test_cw_base import BaseWithDb

class CwServerStopTest(BaseWithDb):
    def setUp(self):
        self.server_job_id = "1234"
        self.server_host = "compute1-exec-225.ris.wustl.edu"
        self.server_port = "8888"
        self.server_url = f"http://{self.server_host}:{self.server_port}"

    @patch("subprocess.call")
    def test_stop_cmd(self, call_p):
        from cw import appcon
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

        appcon.set(group="server", name="job_id", value=self.server_job_id)
        appcon.set(group="server", name="host", value=self.server_host)
        appcon.set(group="server", name="post", value=self.server_port)
        appcon.set(group="server", name="url", value=self.server_url)

        # stop
        result = runner.invoke(cmd, [], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""Server URL: <{self.server_url}>
Stopping job <{self.server_job_id}>
Updating application configuration...
"""
        self.assertEqual(result.output, expected_output)
        self.assertEqual(appcon.get(group="server", name="job_id"), None)
        self.assertEqual(appcon.get(group="server", name="host"), None)
        self.assertEqual(appcon.get(group="server", name="url"), None)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
