import os, unittest
from tests.test_cw_base import BaseWithDb

class AppTest(BaseWithDb):

    def test0(self):
        from cw.app import app, connect, create, sqlite_uri_for_file
        db_fn = os.path.join(self.temp_d.name, "newdb")
        db_uri = sqlite_uri_for_file(db_fn)
        self.assertEqual(sqlite_uri_for_file(db_fn), "sqlite:///"+os.path.join(self.temp_d.name, "newdb"))

        self.assertFalse(os.path.exists(db_fn))
        connect(db_uri)
        self.assertEqual(app.config["SQLALCHEMY_DATABASE_URI"], db_uri)
        self.assertFalse(app.config["SQLALCHEMY_TRACK_MODIFICATIONS"])
        self.assertFalse(os.path.exists(db_fn))
        db = connect(db_uri)
        self.assertTrue(db)
        create()
        self.assertTrue(os.path.exists(db_fn))

    def test0_db(self):
        from cw.app import db
        self.assertTrue(db)

if __name__ == '__main__':
    unittest.main(verbosity=2)
