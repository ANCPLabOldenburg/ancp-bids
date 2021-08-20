import unittest
import tempfile

from ancpbids.schema import Schema
from tests.base_test_case import BaseTestCase, DS005_DIR


class MyTestCase(BaseTestCase):
    def test_writing_ds005(self):
        bids_schema = Schema()
        ds005_original = bids_schema.load_dataset(DS005_DIR)

        target_dir = tempfile.TemporaryDirectory()
        bids_schema.save_dataset(ds005_original, target_dir)
        ds005_copy = bids_schema.load_dataset(target_dir)

        etree_orig = ds005_original.to_etree()
        etree_copy = ds005_copy.to_etree()



if __name__ == '__main__':
    unittest.main()
