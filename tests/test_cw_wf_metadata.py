import click, json, os, tempfile, unittest
from click.testing import CliRunner
from unittest.mock import MagicMock, Mock, patch
import cw.server

from tests.test_cw_base import BaseWithDb
class CwWfTest(BaseWithDb):
    def _setUpClass(self):
        self.metadata_str = b'{\n    "workflowName": "hic",\n    "id": "9d5ffbbc-b246-449b-9685-9db84016c44e"\n}'
        self.metadata = json.loads(self.metadata_str.decode())
        self.add_workflow_to_db(self)

    @patch("cw.server.server_factory")
    def test_metadata_cmd(self, factory_p):
        from cw.wf_metadata import metadata_cmd as cmd

        runner = CliRunner()
        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cmd, ["BLAH"])
        try:
            self.assertEqual(result.exit_code, 1)
        except:
            print(result.output)
            raise
        expected_output = """Failed to get workflow for <BLAH>
"""
        self.assertEqual(result.output, expected_output)

        server = Mock()
        server.configure_mock(**{"url.return_value": "__URL__", "is_running.return_value": False})
        factory_p.return_value = server
        result = runner.invoke(cmd, [f"{self.wf.wf_id}"])
        try:
            self.assertEqual(result.exit_code, 1)
        except:
            print(result.output)
            raise
        expected_output = f"Cromwell server is not running\n"
        self.assertEqual(result.output, expected_output)
        factory_p.assert_called_once()
        factory_p.reset_mock()
        #server.is_running.assert_called_once()
        server.reset_mock()

        server.configure_mock(**{"url.return_value": "__URL__", "is_running.return_value": True, "metadata_for_wf.return_value": self.metadata})
        result = runner.invoke(cmd, [f"{self.wf.wf_id}"])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"{self.metadata_str.decode()}"
        self.assertEqual(result.output, json.dumps(self.metadata, indent=4))
        factory_p.assert_called_once()
        server.is_running.assert_called_once()
        server.metadata_for_wf.assert_called_once()
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
