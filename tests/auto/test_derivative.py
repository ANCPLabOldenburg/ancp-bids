from ancpbids import load_dataset
from ..base_test_case import *


class DerivativesTestCase(BaseTestCase):
    def test_derivative_generated_by(self):
        test_ds = load_dataset(SYNTHETIC_DIR)
        schema = test_ds.get_schema()
        fmriprep_folder = test_ds.derivatives.get_folder('fmriprep')
        self.assertTrue(isinstance(fmriprep_folder, schema.DerivativeFolder))
        self.assertTrue(isinstance(fmriprep_folder.dataset_description, schema.DerivativeDatasetDescriptionFile))
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

    def test_derivative_dataset_description(self):
        test_ds = load_dataset(DS005_SMALL2_DIR)
        schema = test_ds.get_schema()
        dd_files = test_ds.select(schema.DatasetDescriptionFile).objects(as_list=True)
        self.assertEqual(2, len(dd_files))
        names = {'Mixed-gambles task', 'Mixed-gambles task -- dummy derivative'}
        dd_names = [d['Name'] for d in dd_files]
        self.assertTrue(set(dd_names) == names)

        dd = dd_files[1]
        # PipelineDescription is not part of BIDS spec but available in the generic contents object
        self.assertEqual('events', dd.contents['PipelineDescription']['Name'])


if __name__ == '__main__':
    unittest.main()
