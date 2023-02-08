import os, unittest

from tests.test_base_classes import TestBaseWithDb
from mgi.entity.list import list_entities

class EntityListTest(TestBaseWithDb):
    def test_list_entities(self):
        rows = list_entities({})
        self.assertEqual(rows, [["H_G002", "hic"], ["GRCh38", ""]])
        rows = list_entities({"kind": "sample"})
        self.assertEqual(rows, [["H_G002", "hic"]])
        rows = list_entities({"sets": "hic"})
        self.assertEqual(rows, [["H_G002", "hic"]])

# -- EntityListTest

if __name__ == '__main__':
    unittest.main(verbosity=2)
