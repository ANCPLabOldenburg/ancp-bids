import os
import time
import unittest

import numpy as np
import pandas as pd
import shutil
import tempfile

from numpy.testing import tempdir

import ancpbids
from ancpbids import model_latest, re
from ..base_test_case import BaseTestCase, DS005_DIR


class WritingTestCase(BaseTestCase):

    def write_test_derivative(self):
        dataset = ancpbids.load_dataset(DS005_DIR)
        pipeline_name = "mypipeline-%d" % time.time()
        derivative = dataset.create_derivative(name=pipeline_name)
        derivative.dataset_description.GeneratedBy.Name = "My Test Pipeline"
        ents = dataset.query_entities()
        task_label = list(ents['task'])[0]

        for sub_label in ents["subject"]:
            subject = derivative.create_folder(name='sub-' + sub_label)
            # create an additional folder level to increase complexity of generation
            session = subject.create_folder(name='ses-01')

            # do some complex task
            # ... doing complex task ...
            # ... done
            txt_artifact = session.create_artifact()
            txt_artifact.add_entities(desc="mypipeline", run=1, sub=sub_label)
            txt_artifact.suffix = 'textual'
            txt_artifact.extension = ".txt"
            txt_artifact.content = "Subject %s participated in task %s" % (sub_label, task_label)

            # create some random data
            df = pd.DataFrame(np.random.randint(0, 100, size=(100, 4)), columns=list('ABCD'))
            ev_artifact = session.create_artifact()
            ev_artifact.add_entities(desc="mypipeline", run=1, sub=sub_label)
            ev_artifact.suffix = 'events'
            ev_artifact.extension = ".tsv"
            # at this point, the file path is not known and will be provided
            # to lambda when the derivative is written to disk
            ev_artifact.content = lambda file_path, df=df: df.to_csv(file_path, index=None)

        ancpbids.write_derivative(dataset, derivative)
        return DS005_DIR, pipeline_name

    def test_write_derivative(self):
        # create a temporary dataset with a test derivative and return its root path and the created derivative
        ds_path, pipeline_name = self.write_test_derivative()
        # pretend loading a new dataset
        dataset = ancpbids.load_dataset(ds_path)
        # get the underlying graph/dataset for further inspection
        derivative_folder = filter(lambda f: f.name == pipeline_name, dataset.derivatives.folders)
        self.assertIsNotNone(derivative_folder)
        derivative_folder = next(derivative_folder)
        schema = dataset.get_schema()
        subjects = derivative_folder.select(schema.Folder) \
            .where(re(schema.Folder.name, r"sub-[\d]+")) \
            .objects(True)
        self.assertEqual(16, len(subjects))

        for i, subject in enumerate(subjects):
            sub_label = "%02d" % (i + 1)
            expected_sub_name = "sub-%s" % sub_label
            self.assertEqual(expected_sub_name, subject.name)

            expected_ses_name = "ses-01"
            self.assertEqual(expected_ses_name, subject.folders[0].name)

            ses_folder = subject.folders[0]
            for artifact in ses_folder.files:
                ents = artifact.get_entities()
                self.assertEqual(
                    "{'sub': '%s', 'ses': '01', 'run': 1, 'desc': 'mypipeline'}" % (sub_label),
                    str(ents))
                self.assertTrue(artifact.name.startswith('sub-%s_ses-01_run-1_desc-mypipeline_' % sub_label))

        self.assertTrue(isinstance(derivative_folder.dataset_description, schema.DerivativeDatasetDescriptionFile))
        self.assertEqual(derivative_folder.dataset_description.GeneratedBy.Name, "My Test Pipeline")
        shutil.rmtree(derivative_folder.get_absolute_path())

    def test_create_new_dataset(self):
        from ancpbids import model_latest as schema
        dataset = schema.create_dataset(name='my-test-ds')
        dataset.dataset_description.Name = 'a programmatically created dataset'
        dataset.dataset_description.BIDSVersion = schema.VERSION

        for i in range(1, 10):
            subject = dataset.create_folder(name=f"sub-{i}", type_=schema.Subject)
            func_folder = subject.create_folder(name='func', type_=schema.DatatypeFolder)
            img_file = func_folder.create_artifact()
            img_file.suffix = 'bold'
            img_file.extension = '.nii.gz'
            img_file.add_entity('task', 'programming')
            # just create an empty file
            img_file.content = lambda file_name: open(file_name, 'w').close()

        output_dir = tempfile.mkdtemp()
        ancpbids.save_dataset(dataset, output_dir)

        # TODO reload dataset and add assertions


if __name__ == '__main__':
    unittest.main()
