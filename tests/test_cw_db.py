import os, tempfile, unittest
from tests.test_cw_base import BaseWithDb
import cw.db

class DbTest(BaseWithDb):

    def test0_url_for_file(self):
        from cw.db import url_for_file as fun
        self.assertEqual(fun(self.db_fn), self.db_url)

    def test0_create(self):
        from cw.db import create as fun
        #self.assertEqual(fun(), self.db_url)

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
