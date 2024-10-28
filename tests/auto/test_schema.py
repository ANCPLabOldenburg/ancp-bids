import unittest

from ancpbids import model_v1_8_0, model_v1_9_0 as model_latest, load_dataset, load_schema
from ..base_test_case import BaseTestCase, DS005_DIR, DS005_SMALL_DIR


class SchemaTestCase(BaseTestCase):
    def test_entity_matching(self):
        self.assertEqual('sub', model_latest.fuzzy_match_entity_key('sub'))
        self.assertEqual('sub', model_latest.fuzzy_match_entity_key('subject'))
        self.assertEqual('sub', model_latest.fuzzy_match_entity_key('subjects'))
        self.assertEqual('sub', model_latest.fuzzy_match_entity_key('subjs'))

        self.assertEqual('desc', model_latest.fuzzy_match_entity_key('des'))
        self.assertEqual('desc', model_latest.fuzzy_match_entity_key('dscr'))
        self.assertEqual('desc', model_latest.fuzzy_match_entity_key('descriptions'))

    def test_schema_versions(self):
        ds_latest = load_dataset(DS005_DIR)
        schema_latest = ds_latest.get_schema()
        print("Latest schema version:", schema_latest.VERSION)  # Print the schema version
        self.assertEqual(schema_latest, model_latest)
        self.assertEqual('1.9.0', schema_latest.VERSION)  # Change expected to '1.9.0'

        ds_old = load_dataset(DS005_SMALL_DIR)
        schema_old = ds_old.get_schema()
        print("Old schema version:", schema_old.VERSION)  # Print the old schema version
        self.assertEqual(schema_old, model_v1_8_0)
        self.assertEqual('v1.8.0', schema_old.VERSION)

    def test_load_schema(self):
        schema_latest = load_schema(DS005_DIR)
        print("Loaded latest schema version:", schema_latest.VERSION)  # Print the loaded schema version
        self.assertEqual(schema_latest, model_latest)
        self.assertEqual('1.9.0', schema_latest.VERSION)  # Change expected to '1.9.0'

        schema_v180 = load_schema(DS005_SMALL_DIR)
        print("Loaded old schema version:", schema_v180.VERSION)  # Print the loaded old schema version
        self.assertEqual(schema_v180, model_v1_8_0)
        self.assertEqual('v1.8.0', schema_v180.VERSION)

        # The classes of each schema are separate identities
        # FIXME enable assertion once v1.8.1 is generated
        # self.assertFalse(schema_v170.Model == schema_v171.Model)


if __name__ == '__main__':
    unittest.main()
