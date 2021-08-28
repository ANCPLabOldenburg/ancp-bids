from unittest import skip

import ancpbids
import bids
from base_test_case import *

OPENNEURO_DS001734 = '/media/erdal/work/datasets/ds001734'


@skip('please checkout openneuro dataset ds001734, and adapt path to it above')
class BenchmarkTestCase(BaseTestCase):
    def test_ancpbids_openneuro_ds001734(self):
        layout = ancpbids.BIDSLayout(OPENNEURO_DS001734)
        subjects = layout.get_subjects()
        self.assertEqual(108, len(subjects))

    def test_pybids_measure_scan_ds001734(self):
        layout = bids.BIDSLayout(OPENNEURO_DS001734)
        subjects = layout.get_subjects()
        self.assertEqual(108, len(subjects))
