import os, unittest

from tests.test_cw_base import BaseWithDb
class ModelHelpersTest(BaseWithDb):

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
