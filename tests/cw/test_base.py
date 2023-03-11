import os, shutil, tempfile, unittest

class BaseWithDb(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.data_dn = os.path.join(os.path.dirname(__file__), "data")
        self.temp_d = tempfile.TemporaryDirectory()
        os.chdir(self.temp_d.name)
        os.makedirs("server")
        shutil.copy(os.path.join(self.data_dn, "server", "db"), os.path.join(self.temp_d.name, "server", "db"))
        self._setUpClass(self)

    def _setUpClass(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass
#-- BaseWithDb

class BaseWithDbTest(BaseWithDb):
    def test1_setup(self):
        from cw import flask_app
        import cw
        self.assertTrue(bool(self.temp_d))
        self.assertTrue(os.getcwd(), self.temp_d.name)
        self.assertTrue(os.path.exists(cw.DN))
        db_fn = cw.DB_URI.replace("sqlite:///", "")
        self.assertTrue(os.path.exists(db_fn))
#-- BaseWithDbTest

class CwTest(BaseWithDb):
    def test_db(self):
        from cw import db
        self.assertTrue(db)

    def test_appcon_get_and_set(self):
        from cw import appcon, Config
        self.assertTrue(appcon)
        v = appcon.get("foo")
        self.assertEqual(v, None)
        v = appcon.set("foo", "bar")
        self.assertEqual(v, "bar")
        c = Config.query.filter(Config.group == "general", Config.name == "foo").one_or_none()
        self.assertEqual(c.value, "bar")
        v = appcon.set("foo", "baz")
        self.assertEqual(v, "baz")
        c = Config.query.filter(Config.group == "general", Config.name == "foo").one_or_none()
        self.assertEqual(c.value, "baz")

    def test_appcon_server_fns(self):
        from cw import appcon
        for n in ["conf", "run", "start"]:
            fn = appcon.get(group="resources", name=f"{n}_template_fn")
            self.assertTrue(os.path.exists(fn))
            fn = appcon.get(group="server", name=f"{n}_fn")
            self.assertTrue(os.path.join(appcon.dn, "server", "{f}"))

    def test_appcon_known_directories(self):
        from cw import appcon
        self.assertTrue(appcon.known_directories)
        for n in appcon.known_directories:
            self.assertTrue(appcon.dn_for(n))
        with self.assertRaisesRegex(Exception, "Unknown directory"):
            appcon.dn_for("blah")
#-- CwTest

if __name__ == '__main__':
    unittest.main(verbosity=2)
