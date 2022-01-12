import click, requests, unittest
from click.testing import CliRunner
from unittest.mock import MagicMock, patch

from cw.cli import cli

class CwCliTest(unittest.TestCase):
    def test_cromulent_cli(self):
        runner = CliRunner()

        result = runner.invoke(cli, [])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["-h"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["heartbeat", "--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["printc", "--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["server", "--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["setup", "--help"])
        self.assertEqual(result.exit_code, 0)

    @patch("requests.get")
    def test_cw_heartbeat_cmd(self, requests_p):
        from cw.cli import cw_heartbeat_cmd as cmd
        runner = CliRunner()

        result = runner.invoke(cmd, [])
        self.assertEqual(result.exit_code, 1)
        expected_output = """No server given or found in environment 'CROMWELL_SERVER' variable.
"""
        self.assertEqual(result.output, expected_output)

        requests_p.return_value = MagicMock(ok=True, content="1")
        result = runner.invoke(cmd, ["server1"], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = """Cromwell server is up and running version 1.
"""
        self.assertEqual(result.output, expected_output)

    @patch("subprocess.call")
    @patch("os.path.exists")
    def test_cw_server_cmd(self, exists_p, call_p):
        from cw.cli import server_cmd as cmd
        runner = CliRunner()

        # failures
        exists_p.return_value = False
        result = runner.invoke(cmd, [], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 1)
        except:
            print(result.output)
            raise
        expected_output = f"""Can not find cromwell server 
"""
        call_p.assert_not_called()
        exists_p.return_value = True
 
        # launch (start)
        result = runner.invoke(cmd, [], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        fn =  "cromwell/server/start"
        expected_output = f"""RUNNING: {fn}
"""
        self.assertEqual(result.output, expected_output)
        call_p.assert_any_call([fn])

        # local (run)
        result = runner.invoke(cmd, ["--local"], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        fn =  "cromwell/server/run"
        expected_output = f"""RUNNING: {fn}
"""
        self.assertEqual(result.output, expected_output)
        call_p.assert_any_call([fn])
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
