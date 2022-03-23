import click, os, requests, tempfile, unittest, yaml
from click.testing import CliRunner
from unittest.mock import MagicMock, patch

from cw.conf import CromwellConf

class CwHeartbeatCmdTest(unittest.TestCase):
    def setUp(self):
        from cw.setup_cmd import setup_cmd as cmd
        self.temp_d = tempfile.TemporaryDirectory()
        cw_attrs = dict.fromkeys(CromwellConf.attribute_names(), "NULL")
        cw_attrs["CROMWELL_DIR"] = self.temp_d.name
        cw_attrs["CROMWELL_HOST"] = "compute1-exec-200"
        cw_attrs["CROMWELL_PORT"] = "8888"
        cw_attrs["LSF_QUEUE"] = "general"
        cw_attrs["LSF_JOB_GROUP"] = "job"
        cw_attrs["LSF_USER_GROUP"] = "user"
        self.cw_yaml_fn = os.path.join(self.temp_d.name, "cw.yaml")
        with open(self.cw_yaml_fn, "w") as f:
            f.write(yaml.dump(cw_attrs))
        self.cc = CromwellConf(cw_attrs)
        self.cc.setup()

    def tearDown(self):
        self.temp_d.cleanup()

    @patch("requests.get")
    def test_cw_heartbeat_cmd(self, requests_p):
        from cw.heartbeat_cmd import heartbeat_cmd as cmd
        runner = CliRunner()

        requests_p.return_value = MagicMock(ok=True, content="1")
        os.chdir(self.temp_d.name)
        result = runner.invoke(cmd, [], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        host = self.cc._attrs['CROMWELL_HOST']
        port = self.cc._attrs['CROMWELL_PORT']
        expected_output = f"""Checking host <{host}> listening on <{port}> ...
URL: http://{host}:{port}/engine/v1/version
Cromwell server is up and running! Response: 1
"""
        self.assertEqual(result.output, expected_output)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
