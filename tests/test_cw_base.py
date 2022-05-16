import os, tempfile, unittest
import cw.db

class BaseWithDb(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.temp_d = tempfile.TemporaryDirectory()
        os.chdir(self.temp_d.name)
        self.db_fn = os.path.join(self.temp_d.name, "db")
        self.db_url = "sqlite:///" + os.path.join(self.temp_d.name, "db")
        cw.db.set_url(self.db_url)
        cw.db.create(self.db_url)

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
        self.assertEqual(cw.db.app.config["SQLALCHEMY_DATABASE_URI"], self.db_url)
#-- BaseWithDbTest

if __name__ == '__main__':
    unittest.main(verbosity=2)
