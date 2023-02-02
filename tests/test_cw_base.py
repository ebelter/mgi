import os, tempfile, unittest
from cw.helpers import sqlite_uri_for_file

class BaseWithDb(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        import cw
        self.data_dn = os.path.join(os.path.dirname(__file__), "data")
        self.temp_d = tempfile.TemporaryDirectory()
        os.chdir(self.temp_d.name)
        os.makedirs("server")
        self.pipelines_dn = os.path.join(self.temp_d.name, "pipelines")
        os.makedirs(self.pipelines_dn)
        self.db_fn = os.path.join(self.temp_d.name, "server", "db")
        self.db_uri = sqlite_uri_for_file(self.db_fn)
        cw.appcon.dn = self.temp_d.name
        cw.db.uri(self.db_uri)
        cw.create_db()
        self._setUpClass(self)

    def _setUpClass(self):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def add_pipeline_to_db(self):
        if getattr(self, "pipeline", None) is not None:
            return
        from cw import db, Pipeline
        p = Pipeline(
                id=10001, name="__TESTER__",
                wdl=os.path.join(self.pipelines_dn, "t.wdl"),
                inputs=os.path.join(self.pipelines_dn, "t.inputs.yaml"),
                outputs=os.path.join(self.pipelines_dn, "t.outputs.yaml"),
                imports=os.path.join(self.pipelines_dn, "t.imports.zip"),
                )
        db.session.add(p)
        db.session.commit()
        self.pipeline = p

    def add_workflow_to_db(self):
        if getattr(self, "wf", None) is not None:
            return
        from cw import db, Workflow
        self.add_pipeline_to_db(self)
        wf = Workflow(id=10001, wf_id="__WF_ID__", name="__SAMPLE__", pipeline=self.pipeline)
        self.wf = wf

    def add_lsf_config_to_db(self):
        configs = ["docker_volumes=MINE", "job_group=MINE", "queue=MINE", "user_group=MINE"]
        for c in configs:
            n, v = c.split("=")
            cw.appcon.set(group="lsf", name=n, value=v)
#-- BaseWithDb

class BaseWithDbTest(BaseWithDb):
    def test1_setup(self):
        from cw import flask_app
        self.assertTrue(bool(self.temp_d))
        self.assertTrue(bool(self.db_fn))
        self.assertTrue(os.path.exists(self.db_fn))
        self.assertEqual(flask_app.config["SQLALCHEMY_DATABASE_URI"], self.db_uri)
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

    def test_add_objectgs_to_db(self):
        self.assertFalse(getattr(self, "pipeline", None))
        self.add_pipeline_to_db()
        self.assertTrue(self.pipeline)
        self.assertFalse(getattr(self, "wf", None))
        self.add_workflow_to_db()
        self.assertTrue(self.wf)
#-- CwTest

if __name__ == '__main__':
    unittest.main(verbosity=2)
