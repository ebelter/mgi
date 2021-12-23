import click, os, pathlib, tempfile, unittest
from click.testing import CliRunner

class UtilsTest(unittest.TestCase):
    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()
        self.db_fn = os.path.join(self.temp_d.name, "test.db")
        self.db_url = "sqlite:///" + self.db_fn
        os.environ["SQLALCHEMY_DATABASE_URI"] =  self.db_url

    def tearDown(self):
        self.temp_d.cleanup()

    def test_utils_cli(self):
        from mgi.cli import cli
        from mgi.utils import utils_cli

        runner = CliRunner()

        result = runner.invoke(cli, ["utils"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["utils", "-h"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["utils", "--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(utils_cli, [])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(utils_cli, ["--help"])
        self.assertEqual(result.exit_code, 0)

    def test_create_db(self):
        from mgi.utils import create_db
        create_db(self.db_url)
        self.assertTrue(os.path.exists(self.db_fn))

    def test_create_db_cmd(self):
        from mgi.cli import cli as cli
        from mgi.utils import create_db_cmd as cmd
        runner = CliRunner()

        result = runner.invoke(cli, ["utils", "create-db", "-h"])
        self.assertEqual(result.exit_code, 0)
        result = runner.invoke(cli, ["utils", "create-db", "--help"])
        self.assertEqual(result.exit_code, 0)

        result = runner.invoke(cmd, [])
        self.assertEqual(result.exit_code, 2)

        # Fails - Existing DB
        pathlib.Path(self.db_fn).touch()
        with self.assertRaisesRegex(Exception, "exists"):
            result = runner.invoke(cmd, [self.db_url], catch_exceptions=False)
            self.assertEqual(result.exit_code, 1)
        os.remove(self.db_fn)

        # Success
        result = runner.invoke(cmd, [self.db_url], catch_exceptions=False)
        try:
            self.assertEqual(result.exit_code, 0)
        except:
            print(result.output)
            raise
        expected_output = f"Created DB with {self.db_url}\n"
        self.assertEqual(result.output, expected_output)
        self.assertTrue(os.path.exists(self.db_fn))
# -- UtilsTest

if __name__ == '__main__':
    unittest.main(verbosity=2)
