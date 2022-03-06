import os.path
import unittest
import tempfile

from ancpbids import utils, BIDSLayout
from ..base_test_case import BaseTestCase


class FetchDatasetTestCase(BaseTestCase):
    def test_fetch_dataset(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            ds_path = utils.fetch_dataset('ds003483', output_dir=temp_dir)
            self.assertEqual(os.path.join(temp_dir, 'ds003483'), ds_path)
            layout = BIDSLayout(ds_path)

            # some basic checks to make sure the dataset is downloaded and unzipped as expected
            self.assertEqual('ds003483', layout.dataset.name)
            self.assertEqual(21, len(layout.get_subjects()))
            self.assertEqual(['channels', 'coordsystem', 'events', 'meg', 'scans'], layout.get_suffixes())


if __name__ == '__main__':
    unittest.main()
