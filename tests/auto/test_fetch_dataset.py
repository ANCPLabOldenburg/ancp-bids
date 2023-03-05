import os.path
import unittest
import tempfile

from ancpbids import utils, load_dataset
from ..base_test_case import BaseTestCase


class FetchDatasetTestCase(BaseTestCase):
    def test_fetch_dataset(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            ds_path = utils.fetch_dataset('ds003483', output_dir=temp_dir)
            self.assertEqual(os.path.join(temp_dir, 'ds003483'), ds_path)
            dataset = load_dataset(ds_path)

            # some basic checks to make sure the dataset is downloaded and unzipped as expected
            self.assertEqual('ds003483', dataset.name)

            entities = dataset.query_entities()
            self.assertEqual(21, len(entities["subject"]))
            suffixes = dataset.query(target="suffixes")
            self.assertEqual(['channels', 'coordsystem', 'events', 'meg', 'scans'], suffixes)


if __name__ == '__main__':
    unittest.main()
