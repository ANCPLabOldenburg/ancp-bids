import pandas

from base_test_case import *
from bids.schema import Schema
import bids.model as model


class BasicTestCase(BaseTestCase):
    def test_ds005_basic_structure(self):
        bids_schema = Schema()
        ds005 = bids_schema.load_dataset(DS005_DIR)
        self.assertEqual("ds005", ds005.name)
        subjects = ds005.get_subjects()
        self.assertEqual(16, len(subjects))

        first_subject = subjects[0]
        self.assertEqual("sub-01", first_subject.name)
        last_subject = subjects[-1]
        self.assertEqual("sub-16", last_subject.name)

        sessions = first_subject.get_sessions()
        self.assertEqual(0, len(sessions))

        datatypes = first_subject.get_datatypes()
        self.assertEqual(3, len(datatypes))

        anat_datatype = datatypes[0]
        self.assertEqual("anat", anat_datatype.name)
        func_datatype = datatypes[-1]
        self.assertEqual("func", func_datatype.name)

        artifacts = func_datatype.get_artifacts()
        self.assertEqual(7, len(artifacts))
        self.assertEqual("sub-01_task-mixedgamblestask_run-01_bold.nii.gz", artifacts[0].name)
        self.assertEqual("sub-01_task-mixedgamblestask_run-03_events.tsv", artifacts[-1].name)

    def test_json_file_contents(self):
        bids_schema = Schema()
        ds005 = bids_schema.load_dataset(DS005_DIR)
        dataset_description = ds005.load_file_contents("dataset_description.json")
        self.assertTrue(isinstance(dataset_description, dict), "Expected a dictionary")
        self.assertEqual("1.0.0rc2", dataset_description['BIDSVersion'])
        self.assertEqual("Mixed-gambles task", dataset_description['Name'])

    def test_tsv_file_contents(self):
        bids_schema = Schema()
        ds005 = bids_schema.load_dataset(DS005_DIR)
        participants = ds005.load_file_contents("participants.tsv")
        self.assertTrue(isinstance(participants, pandas.DataFrame), "Expected a pandas.DataFrame")
        self.assertListEqual(['participant_id', 'sex', 'age'], list(participants.columns))
        self.assertEqual(16, participants.shape[0])

    def test_parse_entities_in_filenames(self):
        bids_schema = Schema()
        ds005 = bids_schema.load_dataset(DS005_DIR)
        # get first artifact in func datatype of first subject/session:
        # sub-16_task-mixedgamblesatask_run-01_bold.nii.gz
        artifact = ds005.get_subjects()[0].get_datatypes()[-1].get_artifacts()[0]
        self.assertTrue(isinstance(artifact, model.Artifact))

        self.assertEqual("bold", artifact.get_suffix())
        self.assertEqual(".nii.gz", artifact.get_extension())

        entities = artifact.get_entities()
        self.assertTrue(isinstance(entities, list))
        self.assertEqual(3, len(entities))

        entity = entities[0]
        self.assertEqual("sub", entity.get_key())
        self.assertEqual("01", entity.get_value())

        entity = entities[1]
        self.assertEqual("task", entity.get_key())
        self.assertEqual("mixedgamblestask", entity.get_value())

        entity = entities[2]
        self.assertEqual("run", entity.get_key())
        self.assertEqual("01", entity.get_value())


if __name__ == '__main__':
    unittest.main()
