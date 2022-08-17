import click, os, tempfile, unittest
from click.testing import CliRunner
from unittest.mock import Mock, patch

from tests.test_cw_base import BaseWithDb
class CwWfTest(BaseWithDb):
    def _setUpClass(self):
        self.add_workflow_to_db(self)

    @patch("cw.server.server_factory")
    def test_status_cmd(self, server_p):
        from cw.wf_status import status_cmd as cmd
        runner = CliRunner()

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        server = Mock()
        server_p.return_value = server

        server.configure_mock(**{"status_for_workflow.return_value": None})
        result = runner.invoke(cmd, [str(self.wf.id)], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 1)
        except:
            print(result.output)
            raise
        expected_output = f"""Failed to get status for workflow {self.wf.wf_id} ... see above errors.
"""
        self.assertEqual(result.output, expected_output)
        self.assertEqual(server_p.call_count, 1)

        server.configure_mock(**{"status_for_workflow.return_value": "succeeded"})
        result = runner.invoke(cmd, [str(self.wf.id), "--update"], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""Workflow ID: {self.wf.wf_id}
Name:        {self.wf.name}
Status:      succeeded
"""
        self.assertEqual(result.output, expected_output)
        self.assertEqual(server_p.call_count, 2)
        self.assertEqual(self.wf.status, "succeeded")
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
