import unittest

import ancpbids
from tests.base_test_case import BaseTestCase, DS005_DIR, SYNTHETIC_DIR, ENTITIES_DIR


class QueryTestCase(BaseTestCase):
    def test_bidslayout_entities_formatting(self):
        layout = ancpbids.BIDSLayout(ENTITIES_DIR)
        files = layout.get(sub='02', run='3', return_type='filename')
        self.assertEqual(1, len(files))
        self.assertTrue(files[0].endswith("sub-02_run-00003_task-abc_events.tsv"))

        files = layout.get(sub='02', run=['000000003'], return_type='filename')
        self.assertEqual(1, len(files))
        self.assertTrue(files[0].endswith("sub-02_run-00003_task-abc_events.tsv"))

        # should also handle invalid formats, i.e. run not as an index but a label
        files = layout.get(sub='02', run='xyz', return_type='filename')
        self.assertEqual(1, len(files))
        self.assertTrue(files[0].endswith("sub-02_run-xyz_task-abc_events.tsv"))

    def test_bidslayout(self):
        layout = ancpbids.BIDSLayout(DS005_DIR)

        subjects = layout.get_subjects()
        subjects_expected = ['sub-%02d' % i for i in range(1, 17)]
        self.assertListEqual(subjects_expected, subjects)

        sessions = layout.get_sessions()
        self.assertEqual(0, len(sessions))

        tasks = layout.get_tasks()
        self.assertListEqual(['mixedgamblestask'], tasks)

    def test_bidslayout_get(self):
        layout = ancpbids.BIDSLayout(SYNTHETIC_DIR)
        mask_niftis = layout.get(scope='derivatives',
                                 return_type='filename',
                                 suffix='mask',
                                 extension='.nii',
                                 sub='03',
                                 ses='02',
                                 task='nback',
                                 run=["01", "02"])
        self.assertEqual(4, len(mask_niftis))
        expected_paths = [
            'synthetic/derivatives/fmriprep/sub-03/ses-02/func/sub-03_ses-02_task-nback_run-01_space-MNI152NLin2009cAsym_desc-brain_mask.nii',
            'synthetic/derivatives/fmriprep/sub-03/ses-02/func/sub-03_ses-02_task-nback_run-01_space-T1w_desc-brain_mask.nii',
            'synthetic/derivatives/fmriprep/sub-03/ses-02/func/sub-03_ses-02_task-nback_run-02_space-MNI152NLin2009cAsym_desc-brain_mask.nii',
            'synthetic/derivatives/fmriprep/sub-03/ses-02/func/sub-03_ses-02_task-nback_run-02_space-T1w_desc-brain_mask.nii',
        ]
        for file in expected_paths:
            self.assertTrue(list(filter(lambda f: f.endswith(file), mask_niftis)))


if __name__ == '__main__':
    unittest.main()
