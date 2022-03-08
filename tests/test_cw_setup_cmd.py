import click, os, tempfile, unittest, yaml
from click.testing import CliRunner

from cw.conf import CromwellConf
from cw.setup_cmd import setup_cmd as cmd

class Cc1SetupCmdTest(unittest.TestCase):
    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_d.cleanup()

    def test_setup_cmd(self):
        runner = CliRunner()

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cmd, [], catch_exceptions=False)
        self.assertEqual(result.exit_code, 0)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = """Fill out and save the YAML configuration to a file. Then rerun this command.

CROMWELL_DIR: null
CROMWELL_PORT: null
LSF_DOCKER_VOLUMES: null
LSF_JOB_GROUP: null
LSF_QUEUE: null
LSF_USER_GROUP: null
"""
        self.assertEqual(result.output, expected_output)

        attrs = dict.fromkeys(CromwellConf.attribute_names(), "TEST")
        attrs["CROMWELL_DIR"] = self.temp_d.name
        yaml_fn = os.path.join(self.temp_d.name, "cromwell-attrs.yaml")
        with open(yaml_fn, "w") as f:
            f.write(yaml.dump(attrs))
        result = runner.invoke(cmd, [yaml_fn], catch_exceptions=False)
        self.assertEqual(result.exit_code, 0)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        #self.assertRegex(result.output, "^include")
        cc = CromwellConf(attrs)
        self.assertTrue(os.path.exists(cc.server_conf_fn))
        self.assertTrue(os.path.exists(cc.server_run_fn))
        self.assertTrue(os.path.exists(cc.server_start_fn))
        for attr_n in cc._attrs.keys():
            if not attr_n.endswith("_DIR"): continue
            self.assertTrue(os.path.exists(cc._attrs[attr_n]))
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
