import os, unittest

from tests.test_cw_base import BaseWithDb
class ModelHelpersTest(BaseWithDb):
    def setUp(self):
        self.pipeline_id = 10001
        self.pipeline_name = "__TESTER__"
        self.wf_id = 10001
        self.wf_name = "__SAMPLE__"
        self.wf_wf_id = "__WF__"

    def test_resolve_features(self):
        from cw.model_helpers import resolve_features, pipeline_features

        known_features = {
            "name":   {"desc": "name",   "type": str,     "required": True},
            "baller": {"desc": "baller", "type": bool, "required": True},
            }
        expected_features = {}
        features = resolve_features([], known_features)
        self.assertDictEqual(features, expected_features)

        expected_features = {"name": "Barack", "baller": True}
        given_features = ["name=Barack", "baller=Y"]
        features = resolve_features(given_features, known_features)
        self.assertDictEqual(features, expected_features)

        with self.assertRaisesRegex(Exception, "Unknown feature: foo"):
            resolve_features(given_features+["foo=bar"], known_features)

        with self.assertRaisesRegex(Exception, "No value given for feature: name"):
            resolve_features(["name="], known_features)

    def test01_pipeline_helpers(self):
        from cw import db, Pipeline
        from cw.model_helpers import get_pipeline

        p = Pipeline(id=self.pipeline_id, name=self.pipeline_name, wdl="wdl", imports=None)
        db.session.add(p)
        db.session.commit()
        self.assertEqual(p.id, self.pipeline_id)

        p2 = get_pipeline(self.pipeline_id)
        self.assertTrue(p2)
        self.assertEqual(p2, p)
        p2 = get_pipeline(str(self.pipeline_id))
        self.assertTrue(p2)
        self.assertEqual(p2, p)
        p3 = get_pipeline(self.pipeline_name)
        self.assertTrue(p3)
        self.assertEqual(p3, p)
        pnone = get_pipeline("foo")
        self.assertFalse(pnone)

    def test02_wf_helpers(self):
        from cw import db, Pipeline, Workflow
        from cw.model_helpers import wf_features, wf_features_help, get_wf

        self.assertTrue(type(wf_features()), dict)
        self.assertTrue(type(wf_features_help()), str)

        p = Pipeline.query.get(self.pipeline_id)
        self.assertTrue(p)
        wf = Workflow(id=self.wf_id, name=self.wf_name, wf_id=self.wf_wf_id, pipeline=p, status="succeeded")
        db.session.add(wf)
        db.session.commit()

        wf2 = get_wf(self.wf_id)
        self.assertTrue(wf2)
        self.assertEqual(wf2, wf)
        wf2 = get_wf(str(self.wf_id))
        self.assertTrue(wf2)
        self.assertEqual(wf2, wf)
        wf3 = get_wf(self.wf_name)
        self.assertTrue(wf3)
        self.assertEqual(wf3, wf)
        wf4 = get_wf(self.wf_name)
        self.assertTrue(wf4)
        self.assertEqual(wf4, wf)
        wfnone = get_wf("foo")
        self.assertFalse(wfnone)

if __name__ == '__main__':
    unittest.main(verbosity=2)
