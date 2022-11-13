import unittest

from ancpbids import model_latest, model_v1_8_0, load_dataset, load_schema
from ..base_test_case import BaseTestCase, DS005_DIR, DS005_SMALL_DIR


class SchemaTestCase(BaseTestCase):
    def test_entitmatching(self):
        self.assertEqual('sub', model_latest.fuzzy_match_entity_key('sub'))
        self.assertEqual('sub', model_latest.fuzzy_match_entity_key('subject'))
        self.assertEqual('sub', model_latest.fuzzy_match_entity_key('subjects'))
        self.assertEqual('sub', model_latest.fuzzy_match_entity_key('subjs'))

        self.assertEqual('desc', model_latest.fuzzy_match_entity_key('des'))
        self.assertEqual('desc', model_latest.fuzzy_match_entity_key('dscr'))
        self.assertEqual('desc', model_latest.fuzzy_match_entity_key('descriptions'))

    def test_schema_versions(self):
        ds = load_dataset(DS005_DIR)
        schema = ds.get_schema()
        self.assertEqual(schema, model_latest)
        self.assertEqual('v1.8.0', schema.VERSION)

        ds = load_dataset(DS005_SMALL_DIR)
        schema = ds.get_schema()
        self.assertEqual(schema, model_v1_8_0)
        self.assertEqual('v1.8.0', schema.VERSION)

    def test_load_schema(self):
        schema_latest = load_schema(DS005_DIR)
        self.assertEqual(schema_latest, model_latest)
        self.assertEqual('v1.8.0', schema_latest.VERSION)

        schema_v180 = load_schema(DS005_SMALL_DIR)
        self.assertEqual(schema_v180, model_v1_8_0)
        self.assertEqual('v1.8.0', schema_v180.VERSION)

        # the classes of each schema are separate identities
        # FIXME enable assertion once v1.8.1 is generated
        #self.assertFalse(schema_v170.Model == schema_v171.Model)


if __name__ == '__main__':
    unittest.main()
