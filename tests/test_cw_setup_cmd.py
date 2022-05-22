import click, os, tempfile, unittest, yaml
from click.testing import CliRunner

class CwSetupCmdTest(unittest.TestCase):
    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_d.cleanup()

    def test_setup_cmd(self):
        os.chdir(self.temp_d.name)
        from cw import appcon, Config
        from cw.setup_cmd import setup_cmd as cmd
        runner = CliRunner()

        result = runner.invoke(cmd, [], catch_exceptions=False)
        self.assertEqual(result.exit_code, 2)

        configs = ["docker_volumes=MINE", "job_group=MINE", "queue=MINE"]
        with self.assertRaisesRegex(Exception, "Missing"):
            runner.invoke(cmd, configs, catch_exceptions=False)

        configs.append("user_group=MINE")
        result = runner.invoke(cmd, configs, catch_exceptions=False)
        self.assertEqual(result.exit_code, 0)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        self.assertTrue(os.path.exists(os.path.join("server", "db")))
        configs = Config.query.all()
        self.assertEqual(len(configs), 15)
        self.assertTrue(os.path.exists(appcon.get(group="server", name="conf_fn")))
        self.assertTrue(os.path.exists(appcon.get(group="server", name="run_fn")))
        self.assertTrue(os.path.exists(appcon.get(group="server", name="start_fn")))
        for name in ["db", "logs", "runs", "server"]:
            self.assertTrue(os.path.exists(appcon.dn_for(name)))
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
