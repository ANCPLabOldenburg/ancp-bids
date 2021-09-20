import tempfile
import unittest

from ancpbids import load_dataset, save_dataset, model
from base_test_case import BaseTestCase, RESOURCES_FOLDER


class WritingTestCase(BaseTestCase):
    def test_writing_ds005(self):
        ds005_original = load_dataset(RESOURCES_FOLDER + "/ds005-small")

        target_dir = tempfile.TemporaryDirectory().name
        ds005_copy_path = save_dataset(ds005_original, target_dir)
        self.assertTrue(isinstance(ds005_copy_path, str))

        ds005_copy = load_dataset(ds005_copy_path)
        subjects = ds005_copy.subjects
        self.assertEqual(1, len(subjects))
        first_subject = subjects[0]
        self.assertEqual("sub-01", first_subject.name)
        datatypes = first_subject.datatypes
        self.assertEqual(2, len(datatypes))
        self.assertEqual("anat", datatypes[0].name)
        self.assertEqual("func", datatypes[1].name)
        self.assertEqual(1, len(datatypes[0].artifacts))
        self.assertEqual(1, len(datatypes[1].artifacts))
        self.assertEqual(1, len(datatypes[1].metadatafiles))

        ds_descr = ds005_copy.dataset_description
        self.assertTrue(isinstance(ds_descr, model.DatasetDescriptionFile))
        self.assertEqual('dataset_description.json', ds_descr.name)
        self.assertEqual("1.0.0rc2", ds_descr.BIDSVersion)
        self.assertEqual("Mixed-gambles task", ds_descr.Name)

        # TODO more exhaustive comparison/assertions



if __name__ == '__main__':
    unittest.main()
