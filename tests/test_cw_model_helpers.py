import os, unittest

from tests.test_cw_base import BaseWithDb
class ModelHelpersTest(BaseWithDb):

    def test_pipeline_helpers(self):
        from cw import db, Pipeline
        from cw.model_helpers import get_pipeline

        p = Pipeline(name="align", wdl="wdl", imports=None)
        db.session.add(p)
        db.session.commit()
        self.assertEqual(p.id, 1)
        p2 = get_pipeline(1)
        self.assertTrue(p2)
        self.assertEqual(p2, p)
        p2 = get_pipeline("1")
        self.assertTrue(p2)
        self.assertEqual(p2, p)
        p3 = get_pipeline("align")
        self.assertTrue(p3)
        self.assertEqual(p3, p)
        pnone = get_pipeline("foo")
        self.assertFalse(pnone)

if __name__ == '__main__':
    unittest.main(verbosity=2)
