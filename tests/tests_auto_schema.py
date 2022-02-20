import unittest

from ancpbids import model
from base_test_case import BaseTestCase


class SchemaTestCase(BaseTestCase):
    def test_entitmatching(self):
        self.assertEqual('sub', model.fuzzy_match_entity_key('sub'))
        self.assertEqual('sub', model.fuzzy_match_entity_key('subject'))
        self.assertEqual('sub', model.fuzzy_match_entity_key('subjects'))
        self.assertEqual('sub', model.fuzzy_match_entity_key('subjs'))

        self.assertEqual('desc', model.fuzzy_match_entity_key('des'))
        self.assertEqual('desc', model.fuzzy_match_entity_key('dscr'))
        self.assertEqual('desc', model.fuzzy_match_entity_key('descriptions'))


if __name__ == '__main__':
    unittest.main()
