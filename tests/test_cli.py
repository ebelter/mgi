import click, unittest
from click.testing import CliRunner

from mgi.cli import cli

@click.command()
def the_test_cmd():
    print("Hello World!")
cli.add_command(the_test_cmd, "test")

class CliTest(unittest.TestCase):
    def test_cli(self):
        runner = CliRunner()

        result = runner.invoke(cli, [])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["-h"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cli, ["test"])
        try: 
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        self.assertEqual(result.output, "Hello World!\n")

        result = runner.invoke(cli, ["test"])
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        self.assertEqual(result.output, "Hello World!\n")
# -- CliTest

if __name__ == '__main__':
    unittest.main(verbosity=2)
