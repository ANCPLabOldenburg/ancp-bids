import ancpbids
from ..base_test_case import *


class RegressionsTestCase(BaseTestCase):
    def test_get_all_files_from_pipeline(self):
        layout = ancpbids.BIDSLayout(DS005_DIR)
        all_derivative_files = layout.get(scope='derivatives/affine/matrix', return_type='file')
        # that derivatives folder has no valid BIDS files (of type model.Artifact)
        # but ordinary files (if type model.File)
        self.assertEqual(16, len(all_derivative_files))

    def test_get_metadata_no_params(self):
        layout = ancpbids.BIDSLayout(DS005_DIR)
        md = layout.get_metadata()
        expected_md = {'RepetitionTime': 2.0, 'TaskName': 'mixed-gambles task',
                       'SliceTiming': [0.0, 0.0571, 0.1143, 0.1714, 0.2286, 0.2857], 'run': 1}
        self.assertEqual(md, expected_md)

    def test_report_errors(self):
        layout = ancpbids.BIDSLayout(DS005_DIR)
        report = layout.validate()
        self.assertTrue(report.has_errors())

    def test_get_entitites_no_scope(self):
        layout = ancpbids.BIDSLayout(DS005_DIR)
        entities = layout.get_entities(scope=None)
        self.assertEqual(['ds', 'type', 'task', 'sub', 'run', 'desc'], list(entities.keys()))


if __name__ == '__main__':
    unittest.main()
