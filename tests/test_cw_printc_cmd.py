import click, unittest
from click.testing import CliRunner

from tests.test_cw_base import BaseWithDb

class PrintConfCmdTest(BaseWithDb):
    def test_cprint_cmd(self):
        from cw.printc_cmd import printc_cmd as cmd
        runner = CliRunner()

        result = runner.invoke(cmd, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cmd, [], catch_exceptions=False)
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
