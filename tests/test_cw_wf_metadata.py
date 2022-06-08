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
    def test_metadata_for_wf(self, factory_p):
        from cw.wf_metadata import metadata_for_wf as fun

        server = Mock()
        server.configure_mock(**{"url.return_value": "__URL__", "is_running.return_value": False})
        factory_p.return_value = server
        with self.assertRaisesRegex(Exception, "Cromwell server is not running at <__URL__>"):
            fun(self.wf)
        factory_p.assert_called()
        factory_p.reset_mock()

        server.configure_mock(**{"url.return_value": "__URL__", "is_running.return_value": True, "query.return_value": None})
        with self.assertRaisesRegex(Exception, "Server error encountered getting metadata with <__URL__"):
            fun(self.wf)
        factory_p.assert_called_once()
        factory_p.reset_mock()

        server.configure_mock(**{"url.return_value": "__URL__", "is_running.return_value": True, "query.return_value": Mock(ok=False)})
        with self.assertRaisesRegex(Exception, "Server error encountered getting metadata with <__URL"):
            fun(self.wf)
        factory_p.assert_called_once()
        factory_p.reset_mock()

        server.configure_mock(**{"url.return_value": "__URL__", "is_running.return_value": True, "query.return_value": Mock(ok=True, content=self.metadata_str)})
        metadata = fun(self.wf)
        self.assertDictEqual(metadata, self.metadata)
        factory_p.assert_called_once()
        server.query.assert_called_once()

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
        expected_output = f"Failed to get metdata workflow <{self.wf.wf_id}>: Cromwell server is not running at <__URL__>\n"
        self.assertEqual(result.output, expected_output)
        factory_p.assert_called_once()
        factory_p.reset_mock()
        #server.is_running.assert_called_once()
        server.reset_mock()

        server.configure_mock(**{"url.return_value": "__URL__", "is_running.return_value": True, "query.return_value": Mock(ok=True, content=self.metadata_str)})
        result = runner.invoke(cmd, [f"{self.wf.wf_id}"])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"{self.metadata_str.decode()}"
        self.assertEqual(result.output, expected_output)
        factory_p.assert_called_once()
        server.is_running.assert_called_once()
        server.query.assert_called_once()
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
