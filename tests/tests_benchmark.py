from ancpbids import BIDSLayout
from tests.base_test_case import BaseTestCase


class BenchmarkTestCase(BaseTestCase):
    def test_measure_scan_ds001734(self):
        layout = BIDSLayout('/media/erdal/work/datasets/ds001734')
        subjects = layout.get_subjects()
        self.assertEqual(108, len(subjects))

