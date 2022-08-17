import click, json, os, tempfile, unittest
from click.testing import CliRunner
from unittest.mock import MagicMock, Mock, patch
import cw.server

from tests.test_cw_base import BaseWithDb
class CwWfTest(BaseWithDb):
    def _setUpClass(self):
        self.metadata_str = b'{\n    "workflowName": "hic",\n    "id": "9d5ffbbc-b246-449b-9685-9db84016c44e"\n}'
        self.metadata = json.loads(self.metadata_str.decode())
        self.add_workflow_to_db(self)
        self.add_pipeline_to_db(self)
        with open(self.pipeline.inputs, "w") as f:
            f.write("""{\n  "t.sample": "{{_S_}}"\n}""")

    def test_inputs_cmd(self):
        from cw.pl_inputs import inputs_cmd as cmd

        runner = CliRunner()
        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        output_fn = os.path.join(self.temp_d.name, "t.inputs.json")
        result = runner.invoke(cmd, [self.pipeline.name, "_S_=HG002", "-o", output_fn], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"""Wrote pipeline <{self.pipeline.name}> inputs to {output_fn}
"""
        self.assertEqual(result.output, expected_output)
        self.assertTrue(os.path.exists(output_fn))
        with open(output_fn, "r") as f:
            output = f.read()
        expected_output = """{\n  "t.sample": "HG002"\n}"""
        self.assertEqual(output, expected_output)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
