import click, os, tempfile, unittest, yaml
from click.testing import CliRunner

class Cc1SetupCmdTest(unittest.TestCase):
    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_d.cleanup()

    def test_setup_cmd_no_yaml(self):
        from cw.setup_cmd import setup_cmd as cmd
        from cw.conf import CromwellConf
        runner = CliRunner()

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        os.chdir(self.temp_d.name)
        result = runner.invoke(cmd, [], catch_exceptions=False)
        self.assertEqual(result.exit_code, 0)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = """Saved YAML configuration to <cw.yaml>.\nFill out the 'LSF' attributes, then rerun this command.
"""
        self.assertEqual(result.output, expected_output)
        self.assertTrue(os.path.exists("cw.yaml"))
        with open(CromwellConf.yaml_fn(), "r") as f:
            attrs = yaml.safe_load(f)
        self.assertTrue(attrs["CROMWELL_DIR"], self.temp_d.name)

    def test_setup_cmd(self):
        os.chdir(self.temp_d.name)
        from cw import appcon, Config
        from cw.setup_cmd import setup_cmd as cmd
        from cw.conf import CromwellConf
        runner = CliRunner()

        attrs = dict.fromkeys(CromwellConf.attribute_names(), "TEST")
        attrs["CROMWELL_DIR"] = self.temp_d.name
        yaml_fn = "cw.yaml"
        with open(yaml_fn, "w") as f:
            f.write(yaml.dump(attrs))

        result = runner.invoke(cmd, [], catch_exceptions=False)
        self.assertEqual(result.exit_code, 0)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        #self.assertRegex(result.output, "^include")
        cc = CromwellConf(attrs)
        self.assertTrue(os.path.exists(appcon.get(group="server", name="conf_fn")))
        self.assertTrue(os.path.exists(appcon.get(group="server", name="run_fn")))
        self.assertTrue(os.path.exists(appcon.get(group="server", name="start_fn")))
        for attr_n in cc._attrs.keys():
            if not attr_n.endswith("_DIR"): continue
            self.assertTrue(os.path.exists(cc._attrs[attr_n]))
        self.assertTrue(os.path.exists(os.path.join("server", "db")))
        configs = Config.query.all()
        self.assertEqual(len(configs), 10)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
