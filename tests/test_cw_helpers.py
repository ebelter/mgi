import os, unittest

class HelpersTest(unittest.TestCase):

    def test_sqlite_uri(self):
        from cw.helpers import sqlite_uri_for_file
        db_fn = os.path.join(os.sep, "tmp", "newdb")
        db_uri = sqlite_uri_for_file(db_fn)
        self.assertEqual(sqlite_uri_for_file(db_fn), "sqlite:///"+os.path.join(os.sep, "tmp", "newdb"))
#-- 

if __name__ == '__main__':
    unittest.main(verbosity=2)
