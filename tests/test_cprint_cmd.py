import click, os, tempfile, unittest, yaml
from click.testing import CliRunner

from cc1.cconf import CromwellConf
from cc1.cprint_cmd import cprint_cmd as cmd

class Cc1CprintCmdTest(unittest.TestCase):
    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_d.cleanup()

    def test_cprint_cmd(self):
        runner = CliRunner()

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cmd, [])
        self.assertEqual(result.exit_code, 2)

        data = dict.fromkeys(CromwellConf.attribute_names(), "TEST")
        yaml_fn = os.path.join(self.temp_d.name, "cromwell-attrs.yaml")
        with open(yaml_fn, "w") as f:
            f.write(yaml.dump(data))
        result = runner.invoke(cmd, [yaml_fn], catch_exceptions=False)
        self.assertEqual(result.exit_code, 0)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        self.assertRegex(result.output, "^include")
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
