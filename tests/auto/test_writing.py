import time
import unittest

import numpy as np
import pandas as pd
import shutil
import tempfile

import ancpbids
from ancpbids import model, re
from ..base_test_case import BaseTestCase, DS005_DIR


class WritingTestCase(BaseTestCase):

    def write_test_derivative(self):
        layout = ancpbids.BIDSLayout(DS005_DIR)
        dataset = layout.get_dataset()
        pipeline_name = "mypipeline-%d" % time.time()
        derivative = dataset.create_derivative(name=pipeline_name)
        derivative.dataset_description.GeneratedBy.Name = "My Test Pipeline"
        task_label = layout.get_tasks()[0]

        for sub_label in layout.get_subjects():
            subject = derivative.create_folder(name='sub-' + sub_label)

            # do some complex task
            # ... doing complex task ...
            # ... done
            txt_artifact = subject.create_artifact()
            txt_artifact.add_entity("desc", "mypipeline")
            txt_artifact.suffix = 'textual'
            txt_artifact.extension = ".txt"
            txt_artifact.content = "Subject %s participated in task %s" % (sub_label, task_label)

            # create some random data
            df = pd.DataFrame(np.random.randint(0, 100, size=(100, 4)), columns=list('ABCD'))
            ev_artifact = subject.create_artifact()
            ev_artifact.add_entity("desc", "mypipeline")
            ev_artifact.suffix = 'events'
            ev_artifact.extension = ".tsv"
            # at this point, the file path is not known and will be provided
            # to lambda when the derivative is written to disk
            ev_artifact.content = lambda file_path: df.to_csv(file_path, index=None)

        layout.write_derivative(derivative)
        return DS005_DIR, pipeline_name

    def test_write_derivative(self):
        # create a temporary dataset with a test derivative and return its root path and the created derivative
        ds_path, pipeline_name = self.write_test_derivative()
        # pretend loading a new dataset
        layout = ancpbids.BIDSLayout(ds_path)
        # get the underlying graph/dataset for further inspection
        dataset = layout.get_dataset()
        derivative_folder = filter(lambda f: f.name == pipeline_name, dataset.derivatives.folders)
        self.assertIsNotNone(derivative_folder)
        derivative_folder = next(derivative_folder)
        schema = dataset.get_schema()
        subjects = derivative_folder.select(schema.Folder) \
            .where(re(schema.Folder.name, r"sub-[\d]+")) \
            .objects(True)
        self.assertEqual(16, len(subjects))

        for i, subject in enumerate(subjects):
            exptected_sub_name = "sub-%02d" % (i + 1)
            self.assertEqual(exptected_sub_name, subject.name)
            for artifact in subject.files:
                # check if 'sub' entity has been automatically added as it is inferrable from its parent directory
                self.assertEqual(exptected_sub_name, "sub-%s" % artifact.get_entity('sub'))

        self.assertTrue(isinstance(derivative_folder.dataset_description, schema.DerivativeDatasetDescriptionFile))
        self.assertEqual(derivative_folder.dataset_description.GeneratedBy.Name, "My Test Pipeline")


if __name__ == '__main__':
    unittest.main()
