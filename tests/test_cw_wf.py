import click, os, tempfile, unittest
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

    def test_wf_cli(self):
        runner = CliRunner()
        from cw.wf import cli

        result = runner.invoke(cli, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, [])
        self.assertEqual(result.exit_code, 0)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
