import unittest

from ancpbids import model_v1_8_0, model_latest, load_dataset, load_schema
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
        self.assertEqual(schema_latest, model_latest)
        self.assertEqual('1.10.0', schema_latest.VERSION)

        ds_old = load_dataset(DS005_SMALL_DIR)
        schema_old = ds_old.get_schema()
        self.assertEqual(schema_old, model_v1_8_0)
        self.assertEqual('v1.8.0', schema_old.VERSION)

    def test_load_schema(self):
        schema_latest = load_schema(DS005_DIR)
        self.assertEqual(schema_latest, model_latest)
        self.assertEqual('1.10.0', schema_latest.VERSION)

        schema_v180 = load_schema(DS005_SMALL_DIR)
        self.assertEqual(schema_v180, model_v1_8_0)
        self.assertEqual('v1.8.0', schema_v180.VERSION)

        # The classes of each schema are separate identities
        # assert on arbitrary class
        self.assertFalse(schema_latest.DatatypeEnum == schema_v180.DatatypeEnum)

    def test_v190_motion_modality_exists(self):
        from ancpbids import model_v1_9_0
        # in 1.9.0 the motion modality was added
        self.assertTrue("motion" in [e.name for e in model_v1_9_0.ModalityEnum])

    def test_v110_mrs_modality_exists(self):
        from ancpbids import model_v1_10_0
        # in 1.10.0 the mrs modality was added
        self.assertTrue("motion" in [e.name for e in model_v1_10_0.ModalityEnum])



if __name__ == '__main__':
    unittest.main()
