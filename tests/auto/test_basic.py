import numpy

from ancpbids import load_dataset, ENTITIES_PATTERN
from ..base_test_case import *


class BasicTestCase(BaseTestCase):
    def test_naming_scheme(self):
        valid_names = ["sub-11_task-mixedgamblestask_run-02_events.tsv", "sub-11_dwi.nii.gz", "x-01_y-02_z-03_xyz.abc", "sub-01_task-mixedgamblestask_run-01_bold.nii.gz"]
        for name in valid_names:
            self.assertTrue(ENTITIES_PATTERN.match(name))

        invalid_names = ["sub-04_T1w_bias.nii.gz", "cat.jpg", "readme.txt"]
        for name in invalid_names:
            self.assertFalse(ENTITIES_PATTERN.match(name))

    def test_ds005_basic_structure(self):
        ds005 = load_dataset(DS005_DIR)
        self.assertEqual("ds005", ds005.name)

        ds_descr = ds005.dataset_description
        self.assertTrue(isinstance(ds_descr, ds005.get_schema().DatasetDescriptionFile))
        self.assertEqual('dataset_description.json', ds_descr.name)
        self.assertEqual("1.0.0rc2", ds_descr.BIDSVersion)
        self.assertEqual("Mixed-gambles task", ds_descr.Name)
        self.assertTrue(ds_descr.License.startswith(
            "This dataset is made available under the Public Domain Dedication and License"))
        self.assertEqual([
            "Tom, S.M., Fox, C.R., Trepel, C., "
            "Poldrack, R.A. (2007). "
            "The neural basis of loss aversion in decision-making under risk. "
            "Science, 315(5811):515-8"],
            ds_descr.ReferencesAndLinks)

        subjects = ds005.subjects
        self.assertEqual(16, len(subjects))

        first_subject = subjects[0]
        self.assertEqual("sub-01", first_subject.name)
        last_subject = subjects[-1]
        self.assertEqual("sub-16", last_subject.name)

        sessions = first_subject.sessions
        self.assertEqual(0, len(sessions))

        datatypes = first_subject.datatypes
        self.assertEqual(3, len(datatypes))

        anat_datatype = datatypes[0]
        self.assertEqual("anat", anat_datatype.name)
        func_datatype = datatypes[-1]
        self.assertEqual("func", func_datatype.name)

        artifacts = func_datatype.artifacts
        self.assertEqual(6, len(artifacts))
        self.assertEqual("sub-01_task-mixedgamblestask_run-01_bold.nii.gz", artifacts[0].name)
        self.assertEqual("sub-01_task-mixedgamblestask_run-03_events.tsv", artifacts[-1].name)

        metadatafiles = func_datatype.metadatafiles
        self.assertEqual(1, len(metadatafiles))
        self.assertEqual("sub-01_task-mixedgamblestask_run-01_events.json", metadatafiles[0].name)

    def test_json_file_contents(self):
        ds005 = load_dataset(DS005_DIR)
        dataset_description = ds005.load_file_contents("dataset_description.json")
        self.assertTrue(isinstance(dataset_description, dict), "Expected a dictionary")
        self.assertEqual("1.0.0rc2", dataset_description['BIDSVersion'])
        self.assertEqual("Mixed-gambles task", dataset_description['Name'])

    def test_tsv_file_contents(self):
        ds005 = load_dataset(DS005_DIR)
        participants = ds005.load_file_contents("participants.tsv")
        self.assertTrue(isinstance(participants, numpy.ndarray), "Expected a numpy.ndarray")
        self.assertListEqual(['participant_id', 'sex', 'age'], list(participants.dtype.names))
        self.assertEqual(16, participants.shape[0])

    def test_parse_entities_in_filenames(self):
        ds005 = load_dataset(DS005_DIR)
        # get first artifact in func datatype of first subject/session:
        # sub-16_task-mixedgamblesatask_run-01_bold.nii.gz
        artifact = ds005.subjects[0].datatypes[-1].artifacts[0]
        self.assertTrue(isinstance(artifact, ds005.get_schema().Artifact))

        self.assertEqual("bold", artifact.suffix)
        self.assertEqual(".nii.gz", artifact.extension)

        entities = artifact.entities
        self.assertTrue(isinstance(entities, list))
        self.assertEqual(3, len(entities))

        entity = entities[0]
        self.assertEqual("sub", entity.key)
        self.assertEqual("01", entity.value)

        entity = entities[1]
        self.assertEqual("task", entity.key)
        self.assertEqual("mixedgamblestask", entity.value)

        entity = entities[2]
        self.assertEqual("run", entity.key)
        self.assertEqual("1", entity.value)


if __name__ == '__main__':
    unittest.main()
