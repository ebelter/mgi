import click, os, requests, tempfile, unittest
from click.testing import CliRunner
from unittest.mock import MagicMock, patch

from tests.test_cw_base import BaseWithDb
class CwWfTest(BaseWithDb):
    def setUp(self):
        from cw import appcon
        appcon.set(group="lsf", name="queue", value="general")
        appcon.set(group="lsf", name="job_group", value="job")
        appcon.set(group="lsf", name="user_group", value="user")
        self.server_host = "compute1-exec-225.ris.wustl.edu"
        self.server_port = "8888"
        appcon.set(group="server", name="host", value=self.server_host)
        appcon.set(group="server", name="port", value=self.server_port)

    def test_wf_cli(self):
        runner = CliRunner()
        from cw.wf import cli

        result = runner.invoke(cli, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, [])
        self.assertEqual(result.exit_code, 0)

#curl --connect-timeout 5 --max-time 10 -s http://compute1-exec-226.ris.wustl.edu:8888/api/workflows/v1/c808fe24-0edd-46c4-ba23-ff881725e297/status
#{"status":"Succeeded","id":"c808fe24-0edd-46c4-ba23-ff881725e297"}

    @patch("requests.get")
    def test_status_cmd(self, requests_p):
        from cw.wf_status_cmd import status_cmd as cmd
        runner = CliRunner()

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        response = MagicMock(ok=False, content=b'{"status":"Succeeded","id":"WF_ID"}')
        requests_p.return_value = response

        os.chdir(self.temp_d.name)
        result = runner.invoke(cmd, ["WF_ID"], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""URL: http://compute1-exec-225.ris.wustl.edu:8888/api/workflows/v1/WF_ID/status
Failed to get response from server at http://compute1-exec-225.ris.wustl.edu:8888/api/workflows/v1/WF_ID/status
"""
        self.assertEqual(result.output, expected_output)
        requests_p.assert_called()

        response = MagicMock(ok=True, content=b'{"status":"Succeeded","id":"WF_ID"}')
        requests_p.return_value = response

        os.chdir(self.temp_d.name)
        result = runner.invoke(cmd, ["WF_ID"], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""URL: http://compute1-exec-225.ris.wustl.edu:8888/api/workflows/v1/WF_ID/status
Workflow ID: WF_ID
Status:      Succeeded
"""
        self.assertEqual(result.output, expected_output)
        requests_p.assert_called()
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
