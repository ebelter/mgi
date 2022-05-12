import click, os, requests, subprocess, tempfile, time, unittest, yaml
from click.testing import CliRunner
from unittest.mock import MagicMock, patch

from cw.conf import CromwellConf

class CwServerTest(unittest.TestCase):
    def setUp(self):
        from cw.setup_cmd import setup_cmd as cmd
        self.temp_d = tempfile.TemporaryDirectory()
        os.chdir(self.temp_d.name)
        cc = CromwellConf(CromwellConf.default_attributes())
        cc.setattr("LSF_QUEUE", "general")
        cc.setattr("LSF_JOB_GROUP", "job")
        cc.setattr("LSF_USER_GROUP", "user")
        cc.save()
        self.cc = cc
        cc.setup()

    def tearDown(self):
        self.temp_d.cleanup()

    def test_pipelines_db(self):
        from cw.pipelines import PipelinesDb

        pdb = PipelinesDb(fn=self.cc.server_pipelines_fn())
        self.assertTrue(pdb)

        pipelines = pdb.get_pipelines()
        self.assertEqual(type(pipelines), list)

        #align_pnew = {"name": "align", "wdl": "align.wdl", "imports": None}
        align_attrs = ["align.wdl", None]
        pdb.add_pipeline("align", align_attrs)
        pipelines = pdb.get_pipelines()
        self.assertEqual(pipelines[0], ["align"]+align_attrs)

    def test_pipelines_cli(self):
        runner = CliRunner()
        from cw.pipelines import cli

        result = runner.invoke(cli, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, [])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["list", "--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["add", "--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["add"])
        self.assertEqual(result.exit_code, 2)

    def test_add_cmd(self):
        #from cw.pipelines import list_cmd as cmd
        pass

    def test_add_cmd(self):
        from cw.pipelines import add_cmd as cmd
        runner = CliRunner()

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cmd, [""])
        self.assertEqual(result.exit_code, 2)

        name = "align"
        wdl = "align.wdl"
        imports = "align.wdl.zip"
        os.chdir(self.temp_d.name)
        result = runner.invoke(cmd, [name, wdl, "-i", imports], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""Add pipeline {name} {wdl} {imports}
"""
        self.assertEqual(result.output, expected_output)

    def test_list_cmd(self):
        from cw.pipelines import list_cmd as cmd
        runner = CliRunner()

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        os.chdir(self.temp_d.name)
        result = runner.invoke(cmd, [], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""NAME     WDL    IMPORTS
-------  -----  ---------
rna-seq  wdl    imports
"""
        self.assertEqual(result.output, expected_output)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
