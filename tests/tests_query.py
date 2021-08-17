import bids
from tests.base_test_case import BaseTestCase, DS005_DIR, SYNTHETIC_DIR


class QueryTestCase(BaseTestCase):
    def test_bidslayout(self):
        layout = bids.BIDSLayout(DS005_DIR)

        subjects = layout.get_subjects()
        subjects_expected = ['sub-%02d' % i for i in range(1, 17)]
        self.assertListEqual(subjects_expected, subjects)

        sessions = layout.get_sessions()
        self.assertEqual(0, len(sessions))

        tasks = layout.get_tasks()
        self.assertListEqual(['mixedgamblestask'], tasks)

    def test_bidslayout_get(self):
        layout = bids.BIDSLayout(SYNTHETIC_DIR)
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