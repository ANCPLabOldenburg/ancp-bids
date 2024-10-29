import os.path

import ancpbids
from ancpbids import select, re, any_of, all_of, eq, op, entity
from ..base_test_case import *


class QueryTestCase(BaseTestCase):
    def test_entities_formatting(self):
        layout = ancpbids.load_dataset(ENTITIES_DIR)
        files = layout.query(sub='02', run='3', return_type='filename')
        self.assertEqual(1, len(files))
        self.assertTrue(files[0].endswith("sub-02_task-abc_run-00003_events.tsv"))

        files = layout.query(sub='02', run=['000000003'], return_type='filename')
        self.assertEqual(1, len(files))
        self.assertTrue(files[0].endswith("sub-02_task-abc_run-00003_events.tsv"))

        # should also handle invalid formats, i.e. run not as an index but a label
        files = layout.query(sub='02', run='xyz', return_type='filename')
        self.assertEqual(1, len(files))
        self.assertTrue(files[0].endswith("sub-02_task-abc_run-xyz_events.tsv"))

    def test_bidslayout_entities_any(self):
        layout = ancpbids.load_dataset(ENTITIES_DIR)
        files = layout.query(sub='*', suffix='test', task='abc', return_type='filename')
        self.assertEqual(2, len(files))
        self.assertTrue(files[0].endswith("sub-bar_task-abc_test.txt"))
        self.assertTrue(files[1].endswith("sub-foo_task-abc_test.txt"))

    def test_bidslayout_subjects_filtered(self):
        layout = ancpbids.load_dataset(ENTITIES_DIR)
        subjects = layout.query(target="sub", task='abc')
        self.assertEqual(3, len(subjects))
        self.assertListEqual(['02', 'bar', 'foo'], subjects)

    def test_bidslayout(self):
        layout = ancpbids.load_dataset(DS005_DIR)
        ents = layout.query_entities()

        subjects = ents["subject"]
        subjects_expected = {'%02d' % i for i in range(1, 17)}
        self.assertSetEqual(subjects_expected, subjects)

        self.assertNotIn("session", ents)

        tasks = ents["task"]
        self.assertSetEqual({'mixedgamblestask'}, tasks)

    def test_bidslayout_get(self):
        layout = ancpbids.load_dataset(SYNTHETIC_DIR)
        mask_niftis = layout.query(scope='derivatives',
                                   return_type='filename',
                                   suffix='mask',
                                   extension='.nii',
                                   sub='03',
                                   ses='02',
                                   task='nback',
                                   run=["01", "02"])
        self.assertEqual(4, len(mask_niftis))
        expected_paths = [
            'derivatives/fmriprep/sub-03/ses-02/func/sub-03_ses-02_task-nback_run-01_space-MNI152NLin2009cAsym_desc-brain_mask.nii',
            'derivatives/fmriprep/sub-03/ses-02/func/sub-03_ses-02_task-nback_run-01_space-T1w_desc-brain_mask.nii',
            'derivatives/fmriprep/sub-03/ses-02/func/sub-03_ses-02_task-nback_run-02_space-MNI152NLin2009cAsym_desc-brain_mask.nii',
            'derivatives/fmriprep/sub-03/ses-02/func/sub-03_ses-02_task-nback_run-02_space-T1w_desc-brain_mask.nii',
        ]
        expected_paths = list(map(lambda p: os.path.normpath(os.path.join(SYNTHETIC_DIR, p)), expected_paths))
        for file in expected_paths:
            self.assertTrue(list(filter(lambda p: file == p, mask_niftis)))

    def test_bidslayout_get_entities(self):
        layout = ancpbids.load_dataset(DS005_DIR)
        sorted_entities = layout.query_entities(scope='raw', sort=True)
        # note: 'ds' and 'type' entities are contained in folder 'models' at dataset level, so considered raw data
        self.assertListEqual(['ds', 'run', 'subject', 'task', 'type'], list(sorted_entities.keys()))
        self.assertListEqual([1, 2, 3], sorted_entities['run'])
        self.assertEqual(['%02d' % i for i in range(1, 17)], sorted_entities['subject'])
        self.assertListEqual(['mixedgamblestask'], sorted_entities['task'])

    def test_bidslayout_get_suffixes(self):
        layout = ancpbids.load_dataset(DS005_DIR)
        suffixes = layout.query(target="suffixe")
        self.assertListEqual(['T1w', 'bold', 'dwi', 'events', 'model'], suffixes)

    def test_bidslayout_get_extensions(self):
        layout = ancpbids.load_dataset(DS005_DIR)
        extensions = layout.query(target="extension")
        self.assertListEqual(['.json', '.nii.gz', '.tsv'], extensions)

    def test_bidslayout_get_metadata(self):
        layout = ancpbids.load_dataset(DS005_DIR)
        metadata = layout.get_file("sub-01/func/sub-01_task-mixedgamblestask_run-01_bold.nii.gz").get_metadata(
            include_entities=True)
        self.assertTrue(isinstance(metadata, dict))
        self.assertEqual(2.0, metadata['RepetitionTime'])
        self.assertEqual('mixed-gambles task', metadata['TaskName'])
        self.assertListEqual([0.0, 0.0571, 0.1143, 0.1714, 0.2286, 0.2857], metadata['SliceTiming'])
        self.assertEqual('01', metadata['subject'])
        self.assertEqual('mixedgamblestask', metadata['task'])
        self.assertEqual(1, metadata['run'])

    def test_query_language(self):
        ds = ancpbids.load_dataset(DS005_DIR)
        schema = ds.get_schema()
        file_paths = ds.select(schema.Artifact) \
            .where(all_of(eq(schema.Artifact.suffix, 'bold'),
                          entity(schema, schema.EntityEnum.subject, '02'))) \
            .get_file_paths()
        file_paths = list(file_paths)
        self.assertEqual(3, len(file_paths))


if __name__ == '__main__':
    unittest.main()
