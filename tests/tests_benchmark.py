import ancpbids
from base_test_case import *

import bids


class BenchmarkTestCase(BaseTestCase):
    def test_ancpbids_openneuro_ds001734(self):
        layout = ancpbids.BIDSLayout('/media/erdal/work/datasets/ds001734')
        subjects = layout.get_subjects()
        self.assertEqual(108, len(subjects))

    def test_pybids_measure_scan_ds001734(self):
        layout = bids.BIDSLayout('/media/erdal/work/datasets/ds001734')
        subjects = layout.get_subjects()
        self.assertEqual(108, len(subjects))
