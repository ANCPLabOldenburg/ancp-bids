import ancpbids
from ..base_test_case import *


class RegressionsTestCase(BaseTestCase):
    def test_get_all_files_from_pipeline(self):
        dataset = ancpbids.load_dataset(DS005_DIR)
        all_derivative_files = dataset.query(scope='derivatives/affine/matrix', return_type='file')
        # that derivatives folder has no valid BIDS files (of type model.Artifact)
        # but ordinary files (if type model.File)
        self.assertEqual(16, len(all_derivative_files))

    def test_report_errors(self):
        dataset = ancpbids.load_dataset(DS005_DIR)
        report = ancpbids.validate_dataset(dataset)
        self.assertTrue(report.has_errors())

    def test_get_entitites_no_scope(self):
        dataset = ancpbids.load_dataset(DS005_DIR)
        entities = dataset.query_entities(scope=None)
        self.assertEqual(['ds', 'type', 'subject', 'task', 'run', 'description'], list(entities.keys()))


if __name__ == '__main__':
    unittest.main()
