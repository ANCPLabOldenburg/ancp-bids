import unittest

from ancpbids import model_v1_7_0, model_v1_7_1, load_dataset, load_schema
from ..base_test_case import BaseTestCase, DS005_DIR, DS005_SMALL_DIR


class SchemaTestCase(BaseTestCase):
    def test_entitmatching(self):
        self.assertEqual('sub', model_v1_7_0.fuzzy_match_entity_key('sub'))
        self.assertEqual('sub', model_v1_7_0.fuzzy_match_entity_key('subject'))
        self.assertEqual('sub', model_v1_7_0.fuzzy_match_entity_key('subjects'))
        self.assertEqual('sub', model_v1_7_0.fuzzy_match_entity_key('subjs'))

        self.assertEqual('desc', model_v1_7_0.fuzzy_match_entity_key('des'))
        self.assertEqual('desc', model_v1_7_0.fuzzy_match_entity_key('dscr'))
        self.assertEqual('desc', model_v1_7_0.fuzzy_match_entity_key('descriptions'))

    def test_schema_versions(self):
        ds = load_dataset(DS005_DIR)
        schema = ds.get_schema()
        self.assertEqual(schema, model_v1_7_0)
        self.assertEqual('v1.7.0', schema.VERSION)

        ds = load_dataset(DS005_SMALL_DIR)
        schema = ds.get_schema()
        self.assertEqual(schema, model_v1_7_1)
        self.assertEqual('v1.7.1', schema.VERSION)

    def test_load_schema(self):
        schema_v170 = load_schema(DS005_DIR)
        self.assertEqual(schema_v170, model_v1_7_0)
        self.assertEqual('v1.7.0', schema_v170.VERSION)

        schema_v171 = load_schema(DS005_SMALL_DIR)
        self.assertEqual(schema_v171, model_v1_7_1)
        self.assertEqual('v1.7.1', schema_v171.VERSION)

        # the classes of each schema are separate identities
        self.assertFalse(schema_v170.Model == schema_v171.Model)


if __name__ == '__main__':
    unittest.main()
