import click, os, requests, subprocess, tempfile, time, unittest, yaml
from click.testing import CliRunner
from unittest.mock import MagicMock, patch
from pathlib import Path
from unittest.mock import MagicMock, patch

from tests.cw.test_base import BaseWithDb
class Pipelinestest(BaseWithDb):

    def setUp(self):
        self.pipeline_name = "hello-world"

    @patch("subprocess.check_output")
    def test_validate_cmd(self, co_patch):
        from cw.pipelines.validate import validate_cmd as cmd
        from cw import Pipeline
        runner = CliRunner()
        os.chdir(self.temp_d.name)

        co_patch.return_value = "Success!\n"

        p = Pipeline.query.first()
        result = runner.invoke(cmd, [f"{p.id}"], catch_exceptions=False)
        #try:
        #    self.assertEqual(result.exit_code, 0)
        #except:
        #    print(result.output)
        #    raise
        expected_output = f"""Pipeline:        {p.id} {p.name}
Inputs json:     NONE
WOMTOOL output:
"""
        #self.assertEqual(result.output, expected_output)
#--

if __name__ == '__main__':
    unittest.main(verbosity=2)
