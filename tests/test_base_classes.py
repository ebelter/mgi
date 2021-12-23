import os, shutil, tempfile, unittest

class TestBaseWithDb(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data")
        self.src_db_fn = os.path.join(self.data_dn, "test.db")
        self.temp_d = tempfile.TemporaryDirectory()
        self.db_fn = os.path.join(self.temp_d.name, "test.db")
        shutil.copyfile(self.src_db_fn, self.db_fn)
        self.db_url = "sqlite:///" + self.db_fn
        os.environ["SQLALCHEMY_DATABASE_URI"] = self.db_url

    def setUp(self):
        self.copy_db()

    def copy_db(self):
        shutil.copyfile(self.src_db_fn, self.db_fn)

    def cleanUp(self):
        self.temp_d.cleanup()

    @classmethod
    def tearDownClass(self):
        self.temp_d.cleanup()
#-- TestBaseWithDb

class TestBaseWithDbTest(TestBaseWithDb):
    def test1_setup(self):
        self.assertTrue(bool(self.temp_d))
        self.assertTrue(bool(self.data_dn))
        self.assertTrue(bool(self.src_db_fn))
        self.assertTrue(bool(self.db_fn))
        self.assertTrue(os.path.exists(self.db_fn))
        self.assertTrue(bool(os.environ.get("SQLALCHEMY_DATABASE_URI")))
#-- TestBaseWithDbTest

if __name__ == "__main__":
    unittest.main(verbosity=2)
