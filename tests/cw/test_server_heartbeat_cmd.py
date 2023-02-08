import click, os, requests, tempfile, unittest, yaml
from click.testing import CliRunner
from unittest.mock import MagicMock, patch

from tests.test_cw_base import BaseWithDb

class CwHeartbeatCmdTest(BaseWithDb):

    @patch("requests.get")
    def test_cw_heartbeat_cmd(self, requests_p):
        from cw import appcon
        from cw.heartbeat_cmd import heartbeat_cmd as cmd
        runner = CliRunner()

        result = runner.invoke(cmd, [])
        try:
            self.assertEqual(result.exit_code, 1)
        except:
            print(result.output)
            raise
        expected_output = f"Can't find server 'host' in application configuration.\n"

        host = "server1"
        appcon.set(group="server", name="host", value=host)

        result = runner.invoke(cmd, [])
        try:
            self.assertEqual(result.exit_code, 1)
        except:
            print(result.output)
            raise
        expected_output = f"Can't find server 'port' in application configuration.\n"

        port = "8888"
        appcon.set(group="server", name="port", value=port)
        requests_p.return_value = MagicMock(ok=True, content="1")
        os.chdir(self.temp_d.name)
        result = runner.invoke(cmd, [], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""Checking host <{host}> listening on <{port}> ...
URL: http://{host}:{port}/engine/v1/version
Cromwell server is up and running! Response: 1
"""
        self.assertEqual(result.output, expected_output)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
