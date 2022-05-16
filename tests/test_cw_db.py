import os, tempfile, unittest
import cw.db

class DbTest(unittest.TestCase):
    def setUp(self):
        self.temp_d = tempfile.TemporaryDirectory()
        os.chdir(self.temp_d.name)
        self.db_fn = os.path.join(self.temp_d.name, "db")
        self.db_url = "sqlite:///" + os.path.join(self.temp_d.name, "db")
        cw.db.set_url(self.db_url)
        cw.db.create(self.db_url)

    def tearDown(self):
        self.temp_d.cleanup()

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

if __name__ == '__main__':
    unittest.main(verbosity=2)
