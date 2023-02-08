import os, unittest

from tests.test_base_classes import TestBaseWithDb

class EntityAddTest(TestBaseWithDb):

    def test_help(self):
        pass

    def test_get_and_add_entity(self):
        from mgi.models import Entity
        from mgi.entity.add import add_entity, get_entity

        e = get_entity(name="hulk", kind="sample")
        self.assertEqual(e, None)
        e = add_entity(name="hulk", kind="sample")
        self.assertTrue(e)
        e2 = get_entity(name="hulk", kind="sample")
        self.assertTrue(e)

    def test_entities_add(self):
        from mgi.models import Entity
        from mgi.entity.add import add_entities

        e = Entity.query.filter_by(name="hulk", kind="sample").one_or_none()
        self.assertEqual(e, None)

        created, existed = add_entities(names=["hulk"], kind="sample")
        self.assertEqual(len(created), 1)
        self.assertTrue("hulk" in created)
        self.assertEqual(len(existed), 0)
        e = Entity.query.filter_by(name="hulk", kind="sample").one_or_none()
        self.assertTrue(bool(e))

# -- EntityAddTest

if __name__ == '__main__':
    unittest.main(verbosity=2)
