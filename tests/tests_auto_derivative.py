from ancpbids import load_dataset, model
from base_test_case import *


class DerivativesTestCase(BaseTestCase):
    def test_derivative_generated_by(self):
        test_ds = load_dataset(SYNTHETIC_DIR)
        fmriprep_folder = test_ds.derivatives.get_folder('fmriprep')
        self.assertTrue(isinstance(fmriprep_folder, model.DerivativeFolder))
        self.assertTrue(isinstance(fmriprep_folder.dataset_description, model.DerivativeDatasetDescriptionFile))
        dddf = fmriprep_folder.dataset_description
        self.assertEqual(1, len(dddf.GeneratedBy))
        generated_by = dddf.GeneratedBy[0]
        self.assertEqual("fmriprep", generated_by.Name)
        self.assertEqual("1.1.0", generated_by.Version)
        self.assertTrue(generated_by.Container)
        container = generated_by.Container
        self.assertEqual("abc", container.Type)
        self.assertEqual("xyz", container.Tag)
        self.assertEqual("test:abc/xyz", container.URI)


if __name__ == '__main__':
    unittest.main()
