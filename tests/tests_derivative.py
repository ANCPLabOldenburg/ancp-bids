from ancpbids import load_dataset
from base_test_case import *


class DerivativesTestCase(BaseTestCase):
    def test_derivative_generated_by(self):
        test_ds = load_dataset(SYNTHETIC_DIR + "/derivatives/fmriprep")
        self.assertEqual(1, len(test_ds.get_dataset_description().get_GeneratedBy()))
        generated_by = test_ds.get_dataset_description().get_GeneratedBy()[0]
        self.assertEqual("fmriprep", generated_by.get_Name())
        self.assertEqual("1.1.0", generated_by.get_Version())
        self.assertTrue(generated_by.get_Container())
        container = generated_by.get_Container()
        self.assertEqual("abc", container.get_Type())
        self.assertEqual("xyz", container.get_Tag())
        self.assertEqual("test:abc/xyz", container.get_URI())



if __name__ == '__main__':
    unittest.main()
