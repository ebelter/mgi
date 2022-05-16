import os, tempfile, unittest
from tests.test_cw_base import BaseWithDb
import cw.db

class DbTest(BaseWithDb):

    def test0(self):
        from cw.db import app, connect, create, sqlite_uri_for_file
        db_fn = os.path.join(self.temp_d.name, "newdb")
        db_uri = sqlite_uri_for_file(db_fn)
        self.assertEqual(sqlite_uri_for_file(db_fn), "sqlite:///"+os.path.join(self.temp_d.name, "newdb"))

        self.assertFalse(os.path.exists(db_fn))
        connect(db_uri)
        self.assertEqual(app.config["SQLALCHEMY_DATABASE_URI"], db_uri)
        self.assertFalse(app.config["SQLALCHEMY_TRACK_MODIFICATIONS"])
        self.assertFalse(os.path.exists(db_fn))
        connect(db_uri)
        create()
        self.assertTrue(os.path.exists(db_fn))

    def test1_db(self):
        from cw.db import db
        self.assertTrue(db)

    def test2_pipeline(self):
        from cw.db import db, Pipeline
        p = Pipeline(name="align", kind="mgi", wdl="wdl", imports=None)
        db.session.add(p)
        db.session.commit()
        pipelines = Pipeline.query.all()
        self.assertTrue(pipelines)
        self.assertEqual(len(pipelines), 1)
        self.assertTrue(pipelines[0].name)
        self.assertTrue(pipelines[0].kind)
        self.assertTrue(pipelines[0].wdl)
        self.assertFalse(pipelines[0].imports)
        self.assertEqual(len(pipelines[0].workflows.all()), 0)

    def test3_workflow(self):
        from cw.db import db, Workflow
        wf = Workflow(name="SAMPLE", pipeline_id=0)
        db.session.add(wf)
        db.session.commit()
        wfs = Workflow.query.all()
        self.assertTrue(wfs)
        self.assertEqual(len(wfs), 1)
        self.assertEqual(wfs[0].name, "SAMPLE")
        self.assertEqual(wfs[0].pipeline_id, 0)
        self.assertEqual(wfs[0].pipeline, None)

if __name__ == '__main__':
    unittest.main(verbosity=2)
