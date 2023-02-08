import unittest

from mgi.helpers import resolve_features

class HelpersTest(unittest.TestCase):
    def test_resolve_features(self):
        expected_features = {}
        features = resolve_features([], [])
        self.assertDictEqual(features, expected_features)

        expected_features = {"name": "Barack", "baller": "Y"}
        given_features = list(map(lambda i: "=".join(i), expected_features.items()))

        features = resolve_features(given_features) 
        self.assertDictEqual(features, expected_features)

        features = resolve_features(given_features, expected_features.keys())
        self.assertDictEqual(features, expected_features)

        features = resolve_features(given_features, boolean_features=["baller"]) 
        expected_features["baller"] = True
        self.assertDictEqual(features, expected_features)

        with self.assertRaisesRegex(Exception, "Unknown feature: name"):
            resolve_features(given_features, ["not_name"])

        with self.assertRaisesRegex(Exception, "No value given for feature: name"):
            resolve_features(["name="], ["name"])

# -- HelpersTest

if __name__ == '__main__':
    unittest.main(verbosity=2)
#-- __main__
