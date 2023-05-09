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

        configs = ["docker_volumes=MINE", "user_group=MINE", "job_group=MINE"]
        with self.assertRaisesRegex(Exception, "Missing these configurations: queue"):
            runner.invoke(cmd, configs, catch_exceptions=False)

        result = runner.invoke(cmd, configs + ["--env"], catch_exceptions=False, env=dict(LSB_QUEUE="MINE-interactive"))
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        self.assertTrue(os.path.exists(os.path.join("server", "db")))
        configs = Config.query.all()
        self.assertEqual(len(configs), 16)
        queue_config = Config.query.filter(Config.group == "lsf", Config.name == "queue").one_or_none()
        self.assertTrue(bool(queue_config))
        self.assertEqual(queue_config.value, "MINE")
        self.assertTrue(os.path.exists(appcon.get(group="server", name="conf_fn")))
        self.assertTrue(os.path.exists(appcon.get(group="server", name="run_fn")))
        self.assertTrue(os.path.exists(appcon.get(group="server", name="start_fn")))
        for name in ["db", "logs", "runs", "server"]:
            self.assertTrue(os.path.exists(appcon.dn_for(name)))
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
