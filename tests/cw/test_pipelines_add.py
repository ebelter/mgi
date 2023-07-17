import click, os, requests, subprocess, tempfile, time, unittest, yaml
from click.testing import CliRunner
from pathlib import Path
from unittest.mock import MagicMock, patch

from tests.cw.test_base import BaseWithDb
class Pipelinestest(BaseWithDb):

    def setUp(self):
        self.pipeline_name = "hello-world"

    def test_add_cmd(self):
        from cw.pipelines.add import cmd
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
        for ext in ("wdl", "inputs.json", "outputs.yaml", "outputs.yml", "imports.zip"):
            fn = os.path.join(self.temp_d.name, f"__TESTER__.{ext}")
            Path(fn).touch()
        result = runner.invoke(cmd, [f"name={name}", "wdl="+os.path.join(self.temp_d.name, "__TESTER__.wdl"), "outputs="+os.path.join(self.temp_d.name, "__TESTER__.outputs.yml")], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""Name:     __TESTER__
ID:       2
WDL:      {os.path.join(self.temp_d.name, '__TESTER__.wdl')}
Inputs:   {os.path.join(self.temp_d.name, '__TESTER__.inputs.json')}
Outputs:  {os.path.join(self.temp_d.name, '__TESTER__.outputs.yml')}
Imports:  {os.path.join(self.temp_d.name, '__TESTER__.imports.zip')}
"""
        self.assertEqual(result.output, expected_output)
        p = Pipeline.query.filter(Pipeline.name == name).first()
        self.assertTrue(p)
        self.assertEqual(p.name, name)
        self.assertEqual(p.wdl, os.path.join(self.temp_d.name, "__TESTER__.wdl"))
        self.assertEqual(p.inputs, os.path.join(self.temp_d.name, "__TESTER__.inputs.json"))
        self.assertEqual(p.outputs, os.path.join(self.temp_d.name, "__TESTER__.outputs.yml"))
        self.assertEqual(p.imports, os.path.join(self.temp_d.name, "__TESTER__.imports.zip"))
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
