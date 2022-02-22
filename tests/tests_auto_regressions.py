import ancpbids
from base_test_case import *


class RegressionsTestCase(BaseTestCase):
    def test_get_all_files_from_pipeline(self):
        layout = ancpbids.BIDSLayout(DS005_DIR)
        all_derivative_files = layout.get(scope='derivatives/affine/matrix', return_type='file')
        # that derivatives folder has no valid BIDS files
        self.assertEqual(0, len(all_derivative_files))


if __name__ == '__main__':
    unittest.main()
