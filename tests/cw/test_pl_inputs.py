import click, json, os, tempfile, unittest
from click.testing import CliRunner
from unittest.mock import MagicMock, Mock, patch

from tests.cw.test_base import BaseWithDb
class CwWfTest(BaseWithDb):
    def test_inputs_cmd(self):
        from cw.pipeline.inputs import inputs_cmd as cmd

        runner = CliRunner()
        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        output_fn = os.path.join(self.temp_d.name, "t.inputs.json")
        pl_name = "hello-world"
        result = runner.invoke(cmd, [pl_name, "NAME=Bart", "-o", output_fn], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""Wrote pipeline <{pl_name}> inputs to {output_fn}
"""
        self.assertEqual(result.output, expected_output)
        self.assertTrue(os.path.exists(output_fn))
        with open(output_fn, "r") as f:
            output = f.read()
        expected_output = """{\n  "hw.name": "Bart"\n}"""
        self.assertEqual(output, expected_output)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
