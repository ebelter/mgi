import unittest

from tests.test_base_classes import TestBaseWithDb

class ModelsTest(TestBaseWithDb):
    sample_name = "H_G002"

    def test1_entity(self):
        from mgi.models import Entity
        entities = Entity.query.all()
        self.assertEqual(len(entities), 2)
        self.assertEqual(entities[0].name, self.sample_name)
        self.assertEqual(entities[0].kind, "sample")
        self.assertEqual(len(entities[0].features), 1)
        self.assertEqual(len(entities[0].paths), 1)

    def test2_entity_features(self):
        from mgi.models import EntityFeature
        features = EntityFeature.query.filter_by(group="qc").all()
        self.assertTrue(features)
        self.assertEqual(len(features), 2)
        self.assertTrue(features[0].group)
        self.assertTrue(features[0].name)
        self.assertTrue(features[0].value)
        self.assertEqual(features[0].entity.name, self.sample_name)

    def test3_sample_path(self):
        from mgi.models import EntityPath
        fps = EntityPath.query.filter_by(kind="merged bam").all()
        self.assertEqual(len(fps), 1)
        self.assertTrue(fps[0].entity)
        self.assertEqual(fps[0].entity_id, 1)
        self.assertTrue(fps[0].group, "anaylsis1")
        self.assertEqual(fps[0].value, "/mnt/data/samples/HG002.merged.bam")
        self.assertEqual(fps[0].checksum, "checksum")
        self.assertEqual(fps[0].exists, True)
        self.assertEqual(fps[0].kind, "merged bam")
# -- ModelsTest

if __name__ == '__main__':
    unittest.main(verbosity=2)

#-- __main__
