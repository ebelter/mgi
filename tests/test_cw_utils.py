import click, unittest
from click.testing import CliRunner

from tests.test_cw_base import BaseWithDb
class UtilsTest(BaseWithDb):
    def test0_cli(self):
        from cw.utils import cli
        runner = CliRunner()

        result = runner.invoke(cli, [])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["printr", "--help"])
        self.assertEqual(result.exit_code, 0)

    def test1_printr_cmd(self):
        from cw.utils import printr_cmd as cmd
        runner = CliRunner()

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cmd, [], catch_exceptions=False)
        self.assertEqual(result.exit_code, 2)

        result = runner.invoke(cmd, ["conf"], catch_exceptions=False)
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
