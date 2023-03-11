import os, unittest

from tests.cw.test_base import BaseWithDb
class ModelHelpersTest(BaseWithDb):

    def test_resolve_features(self):
        from cw.model_helpers import resolve_features, pipeline_features

        known_features = {
            "name":   {"desc": "name",   "type": str,     "required": True},
            "baller": {"desc": "baller", "type": bool, "required": True},
            "birth_cert": {"desc": "birth_cert", "type": "file", "required": True},
            }
        expected_features = {}
        features = resolve_features([], known_features)
        self.assertDictEqual(features, expected_features)

        expected_features = {"name": "Barack", "baller": True, "birth_cert": __file__}
        given_features = ["name=Barack", "baller=Y", f"birth_cert={__file__}"]
        features = resolve_features(given_features, known_features)
        self.assertDictEqual(features, expected_features)

        with self.assertRaisesRegex(Exception, "Unknown feature: foo"):
            resolve_features(given_features+["foo=bar"], known_features)

        with self.assertRaisesRegex(Exception, "No value given for feature: name"):
            resolve_features(["name="], known_features)

        with self.assertRaisesRegex(Exception, "Feature <birth_cert> is a file, but given value <blah> does not exist"):
            resolve_features(["birth_cert=blah"], known_features)

    def test01_pipeline_helpers(self):
        from cw import Pipeline
        from cw.model_helpers import get_pipeline

        p = Pipeline.query.get(1)
        self.assertTrue(bool(p))

        p1 = get_pipeline(p.id)
        self.assertTrue(p1)
        self.assertEqual(p1, p)
        p2 = get_pipeline(str(p.id))
        self.assertTrue(p2)
        self.assertEqual(p2, p)
        p3 = get_pipeline(p.name)
        self.assertTrue(p3)
        self.assertEqual(p3, p)
        pnone = get_pipeline("foo")
        self.assertFalse(pnone)

    def test02_wf_helpers(self):
        from cw import Workflow
        from cw.model_helpers import wf_features, wf_features_help, get_wf

        self.assertTrue(type(wf_features()), dict)
        self.assertTrue(type(wf_features_help()), str)

        wf = Workflow.query.get(1)
        self.assertTrue(wf)

        wf1 = get_wf(wf.wf_id)
        self.assertTrue(wf1)
        self.assertEqual(wf1, wf)
        wf2 = get_wf(str(wf.wf_id))
        self.assertTrue(wf2)
        self.assertEqual(wf2, wf)
        wf3 = get_wf(wf.name)
        self.assertTrue(wf3)
        self.assertEqual(wf3, wf)
        wf4 = get_wf(wf.name)
        self.assertTrue(wf4)
        self.assertEqual(wf4, wf)
        wfnone = get_wf("foo")
        self.assertFalse(wfnone)

if __name__ == '__main__':
    unittest.main(verbosity=2)
