import unittest

from ancpbids import load_dataset, DatasetOptions
from tests.base_test_case import DS005_DIR_IGNORED_RESOURCES


class IgnoredResourcesTestCase(unittest.TestCase):
    def test_ignore_file(self):
        ds = load_dataset(DS005_DIR_IGNORED_RESOURCES, DatasetOptions(ignore=True))
        assert ds.get_folder("models") is None
        assert ds.get_folder("stimuli") is None
        assert ds.get_file(".dummy") is None
        assert ds.query(sub="01", suffix="bold") is not None
        assert ds.dataset_description is not None

        assert ds.get_file(".bidsignore") is None

    def test_ignore_file_dynamic(self):
        ds = load_dataset(DS005_DIR_IGNORED_RESOURCES, DatasetOptions(ignore=["models", "stimuli", ".*"]))
        assert ds.get_folder("models") is None
        assert ds.get_folder("stimuli") is None
        assert ds.get_file(".dummy") is None
        assert ds.query(sub="01", suffix="bold") is not None
        assert ds.dataset_description is not None

        assert ds.get_file(".bidsignore") is None


if __name__ == '__main__':
    unittest.main()
