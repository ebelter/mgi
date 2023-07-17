import click, os, requests, subprocess, tempfile, time, unittest, yaml
from click.testing import CliRunner
from unittest.mock import MagicMock, patch

from tests.cw.test_base import BaseWithDb
class Pipelinestest(BaseWithDb):

    def setUp(self):
        self.pipeline_name = "hello-world"

    def test12_add_cmd(self):
        from cw.pipelines.cli import add_cmd as cmd
        from cw import Pipeline
        runner = CliRunner()
        os.chdir(self.temp_d.name)

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cmd, [])
        self.assertEqual(result.exit_code, 2)

        with self.assertRaisesRegex(Exception, f"Feature <wdl> is a file, but given value <blah.wdl> does not exist"):
            runner.invoke(cmd, ["name="+self.pipeline_name, "wdl=blah.wdl", "imports=blah.zip"], catch_exceptions=False)
        with self.assertRaisesRegex(Exception, f"Feature <imports> is a file, but given value <blah.zip> does not exist"):
            runner.invoke(cmd, ["name="+self.pipeline_name, "wdl="+__file__, "imports=blah.zip"], catch_exceptions=False)
        with self.assertRaisesRegex(Exception, f"Feature <outputs> is a file, but given value <blah.yaml> does not exist"):
            runner.invoke(cmd, ["name="+self.pipeline_name, "wdl="+__file__, "imports="+__file__, "outputs=blah.yaml"], catch_exceptions=False)

        name = "__TESTER__"
        result = runner.invoke(cmd, ["name="+name, "wdl="+__file__, "imports="+__file__], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""Name:     __TESTER__
ID:       2
WDL:      /home/ebelter/dev/mgi/tests/cw/test_pipelines_add.py
Imports:  /home/ebelter/dev/mgi/tests/cw/test_pipelines_add.py
Inputs:   None
Outputs:  None
"""
        self.assertEqual(result.output, expected_output)
        p = Pipeline.query.filter(Pipeline.name == name).first()
        self.assertTrue(p)
        self.assertEqual(p.name, name)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
