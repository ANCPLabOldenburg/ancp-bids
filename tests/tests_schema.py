import unittest

from ancpbids import Schema
from tests.base_test_case import BaseTestCase


class SchemaTestCase(BaseTestCase):
    def test_entitmatching(self):
        schema = Schema()
        self.assertEqual('sub', schema.fuzzy_match_entity_key('sub'))
        self.assertEqual('sub', schema.fuzzy_match_entity_key('subject'))
        self.assertEqual('sub', schema.fuzzy_match_entity_key('subjects'))
        self.assertEqual('sub', schema.fuzzy_match_entity_key('subjs'))

        self.assertEqual('desc', schema.fuzzy_match_entity_key('des'))
        self.assertEqual('desc', schema.fuzzy_match_entity_key('dscr'))
        self.assertEqual('desc', schema.fuzzy_match_entity_key('descriptions'))



if __name__ == '__main__':
    unittest.main()
