import ancpbids
from base_test_case import *


class RegressionsTestCase(BaseTestCase):
    def test_get_all_files_from_pipeline(self):
        layout = ancpbids.BIDSLayout(DS005_DIR)
        all_derivative_files = layout.get(scope='derivatives/affine/matrix', return_type='file')
        self.assertEqual(16, len(all_derivative_files))


if __name__ == '__main__':
    unittest.main()
