import unittest

from ancpbids import utils, model_v1_7_0 as schema
from ..base_test_case import BaseTestCase


class SchemaTestCase(BaseTestCase):
    def test_entitmatching(self):
        self.assertEqual('sub', utils.fuzzy_match_entity_key(schema, 'sub'))
        self.assertEqual('sub', utils.fuzzy_match_entity_key(schema, 'subject'))
        self.assertEqual('sub', utils.fuzzy_match_entity_key(schema, 'subjects'))
        self.assertEqual('sub', utils.fuzzy_match_entity_key(schema, 'subjs'))

        self.assertEqual('desc', utils.fuzzy_match_entity_key(schema, 'des'))
        self.assertEqual('desc', utils.fuzzy_match_entity_key(schema, 'dscr'))
        self.assertEqual('desc', utils.fuzzy_match_entity_key(schema, 'descriptions'))

    def test_schema_versions(self):
        pass


if __name__ == '__main__':
    unittest.main()
