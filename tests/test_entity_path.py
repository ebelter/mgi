import os, unittest
from click.testing import CliRunner

from tests.test_base_classes import TestBaseWithDb

class EntityPathTest(TestBaseWithDb):
    def test_get_and_add_functions(self):
        from mgi.entity.path import get_entity, add_entity, get_entity_path, add_entity_path
        from mgi.models import db

        e = get_entity(name="Iron Man", kind="Avenger")
        self.assertFalse(e)
        e = add_entity(name="Iron Man", kind="Avenger")
        self.assertTrue(e)
        db.session.add(e)
        db.session.flush()
        db.session.commit()

        e2 = get_entity(name="Iron Man", kind="Avenger")
        self.assertTrue(e2)
        self.assertEqual(e2.id, e.id)

        ep_d = {"entity_id": e.id, "group": "gems", "kind": "infinity", "value": "soul"}
        ep = get_entity_path(ep_d)
        self.assertFalse(ep)
        ep = add_entity_path(ep_d)
        self.assertTrue(ep)
        db.session.add(ep)
        db.session.flush()
        db.session.commit()

        ep2 = get_entity_path(ep_d)
        self.assertEqual(ep2.id, ep.id)

    def test_ep_update_cmd(self):
        from mgi.entity.path import update_entities_paths, get_entity, get_entity_path
        from mgi.entity.path_factory import rdr_factory

        fn = os.path.join(self.temp_d.name, "paths.tsv")
        value = "/mnt/data/sample_111.bam"
        with open(fn, "w") as f:
            f.write("\t".join([value])+"\n")

        rdr = rdr_factory(fn)
        update_entities_paths(rdr, {"group": "prod"}, entity_kind="ref")
        e = get_entity(name="sample_111", kind="ref")
        self.assertTrue(e)
        ep = get_entity_path({"entity_id": e.id, "value": value})

# -- EntityPathTest

if __name__ == '__main__':
    unittest.main(verbosity=2)
