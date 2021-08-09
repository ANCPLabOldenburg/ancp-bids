import unittest
from bids import schema, dataset, validator
import os
import pandas

BIDS_SCHEMA_DIR = os.path.expanduser("~/git/bids-specification/src/schema/")
TEST_FOLDER = os.path.dirname(__file__)
RESOURCES_FOLDER = TEST_FOLDER + "/data"

DS005_DIR = RESOURCES_FOLDER + "/ds005"
DS005_CONFLICT_DIR = RESOURCES_FOLDER + "/ds005_conflict"


class BasicTestCase(unittest.TestCase):
    def test_ds005_basic_structure(self):
        ds005 = dataset.Dataset(DS005_DIR)
        self.assertEqual("ds005", ds005.name)
        subjects = ds005.get_subjects()
        self.assertEqual(16, len(subjects))

        first_subject = subjects[0]
        self.assertEqual("sub-01", first_subject.name)
        last_subject = subjects[-1]
        self.assertEqual("sub-16", last_subject.name)

        sessions = first_subject.get_sessions()
        self.assertEqual(1, len(sessions))

        first_session = sessions[0]
        self.assertEqual("ses-01", first_session.name)

        datatypes = first_session.get_datatypes()
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
        ds005 = dataset.Dataset(DS005_DIR)
        dataset_description = ds005.folder.load_file("dataset_description.json")
        self.assertTrue(isinstance(dataset_description, dict), "Expected a dictionary")
        self.assertEqual("1.0.0rc2", dataset_description['BIDSVersion'])
        self.assertEqual("Mixed-gambles task", dataset_description['Name'])

    def test_tsv_file_contents(self):
        ds005 = dataset.Dataset(DS005_DIR)
        participants = ds005.folder.load_file("participants.tsv")
        self.assertTrue(isinstance(participants, pandas.DataFrame), "Expected a pandas.DataFrame")
        self.assertListEqual(['participant_id', 'sex', 'age'], list(participants.columns))
        self.assertEqual(16, participants.shape[0])

    def test_validation_top_level_files(self):
        bids_schema = schema.Schema(BIDS_SCHEMA_DIR)
        self.assertEqual("master", bids_schema.get_version())

        ds005_conflict = dataset.Dataset(DS005_CONFLICT_DIR)

        val = validator.Validator()
        report = val.validate(bids_schema, ds005_conflict)
        self.assertTrue(isinstance(report, validator.ValidationReport))

        self.assertEqual(2, len(report.messages))
        self.assertEqual("Missing required top level file 'README'", report.messages[0]['message'])
        self.assertEqual("Missing required top level file 'CHANGES'", report.messages[1]['message'])


if __name__ == '__main__':
    unittest.main()
