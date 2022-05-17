import os, tempfile, unittest
import cw.app

class BaseWithDb(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.temp_d = tempfile.TemporaryDirectory()
        os.chdir(self.temp_d.name)
        os.makedirs("server")
        self.db_fn = os.path.join(self.temp_d.name, "server", "db")
        self.db_uri = cw.app.sqlite_uri_for_file(self.db_fn)
        cw.app.connect(self.db_uri)
        cw.app.create()

    def setUp(self):
        pass

    def tearDown(self):
        pass
#-- BaseWithDb

class BaseWithDbTest(BaseWithDb):
    def test1_setup(self):
        self.assertTrue(bool(self.temp_d))
        self.assertTrue(bool(self.db_fn))
        self.assertTrue(os.path.exists(self.db_fn))
        self.assertEqual(cw.app.app.config["SQLALCHEMY_DATABASE_URI"], self.db_uri)
#-- BaseWithDbTest

if __name__ == '__main__':
    unittest.main(verbosity=2)
