import click, os, requests, tempfile, unittest
from click.testing import CliRunner
from unittest.mock import MagicMock, patch

from cw.conf import CromwellConf
import cw.wf

class CwWfTest(unittest.TestCase):
    def setUp(self):
        from cw.setup_cmd import setup_cmd as cmd
        self.temp_d = tempfile.TemporaryDirectory()
        os.chdir(self.temp_d.name)
        cc = CromwellConf(CromwellConf.default_attributes())
        self.server_host = "compute1-exec-225.ris.wustl.edu"
        self.server_port = "8888"
        cc.setattr("LSF_QUEUE", "general")
        cc.setattr("LSF_JOB_GROUP", "job")
        cc.setattr("LSF_USER_GROUP", "user")
        cc.setattr("CROMWELL_HOST", self.server_host)
        cc.setattr("CROMWELL_PORT", self.server_port)
        cc.save()

    def tearDown(self):
        self.temp_d.cleanup()

    @patch("requests.get")
    def test_metadata_cmd(self, requests_p):
        from cw.wf_metadata_cmd import metadata_cmd as cmd
        runner = CliRunner()

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        content = b'{"workflowName": "hic", "id": "9d5ffbbc-b246-449b-9685-9db84016c44e"}'
        response = MagicMock(ok=False, content=content)
        requests_p.return_value = response

        os.chdir(self.temp_d.name)
        result = runner.invoke(cmd, ["WF_ID"], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""Failed to get response from server at http://compute1-exec-225.ris.wustl.edu:8888/api/workflows/v1/WF_ID/metadata?excludeKey=submittedFiles&expandSubWorkflows=true
"""
        self.assertEqual(result.output, expected_output)
        requests_p.assert_called()

        response = MagicMock(ok=True, content=content)
        requests_p.return_value = response

        os.chdir(self.temp_d.name)
        result = runner.invoke(cmd, ["WF_ID"], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"{content.decode()}"
        self.assertEqual(result.output, expected_output)
        requests_p.assert_called()
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
