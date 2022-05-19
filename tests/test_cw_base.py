import os, tempfile, unittest
from cw import db, create_db
from cw.helpers import sqlite_uri_for_file

class BaseWithDb(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.temp_d = tempfile.TemporaryDirectory()
        os.chdir(self.temp_d.name)
        os.makedirs("server")
        self.db_fn = os.path.join(self.temp_d.name, "server", "db")
        self.db_uri = sqlite_uri_for_file(self.db_fn)
        db.uri(self.db_uri)
        create_db()

    def setUp(self):
        pass

    def tearDown(self):
        pass
#-- BaseWithDb

class BaseWithDbTest(BaseWithDb):
    def test1_setup(self):
        from cw import flask_app
        self.assertTrue(bool(self.temp_d))
        self.assertTrue(bool(self.db_fn))
        self.assertTrue(os.path.exists(self.db_fn))
        self.assertEqual(flask_app.config["SQLALCHEMY_DATABASE_URI"], self.db_uri)
#-- BaseWithDbTest

if __name__ == '__main__':
    unittest.main(verbosity=2)
