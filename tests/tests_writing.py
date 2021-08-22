import filecmp
import tempfile
import unittest
from xml.etree import ElementTree

from ancpbids import load_dataset, save_dataset, to_etree
from tests.base_test_case import BaseTestCase, DS005_DIR, RESOURCES_FOLDER


class MyTestCase(BaseTestCase):
    def test_writing_ds005(self):
        ds005_original = load_dataset(RESOURCES_FOLDER + "/ds005")

        target_dir = tempfile.TemporaryDirectory().name
        ds005_copy = save_dataset(ds005_original, target_dir)

        # diff = filecmp.dircmp(DS005_DIR, ds005_copy)
        # diff.report_full_closure()
        # print(diff)


if __name__ == '__main__':
    unittest.main()
