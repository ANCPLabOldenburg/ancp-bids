import os.path

import ancpbids
from ancpbids import select, re, any_of, all_of, eq, op, entity
from ..base_test_case import *


class QueryTestCase(BaseTestCase):
    def test_bidslayout_entities_formatting(self):
        layout = ancpbids.BIDSLayout(ENTITIES_DIR)
        files = layout.get(sub='02', run='3', return_type='filename')
        self.assertEqual(1, len(files))
        self.assertTrue(files[0].endswith("sub-02_task-abc_run-00003_events.tsv"))

        files = layout.get(sub='02', run=['000000003'], return_type='filename')
        self.assertEqual(1, len(files))
        self.assertTrue(files[0].endswith("sub-02_task-abc_run-00003_events.tsv"))

        # should also handle invalid formats, i.e. run not as an index but a label
        files = layout.get(sub='02', run='xyz', return_type='filename')
        self.assertEqual(1, len(files))
        self.assertTrue(files[0].endswith("sub-02_task-abc_run-xyz_events.tsv"))

    def test_bidslayout_entities_any(self):
        layout = ancpbids.BIDSLayout(ENTITIES_DIR)
        files = layout.get(sub='*', suffix='test', task='abc', return_type='filename')
        self.assertEqual(2, len(files))
        self.assertTrue(files[0].endswith("sub-bar_task-abc_test.txt"))
        self.assertTrue(files[1].endswith("sub-foo_task-abc_test.txt"))

    def test_bidslayout_subjects_filtered(self):
        layout = ancpbids.BIDSLayout(ENTITIES_DIR)
        subjects = layout.get_subjects(task='abc')
        self.assertEqual(3, len(subjects))
        self.assertListEqual(['02', 'bar', 'foo'], subjects)

    def test_bidslayout(self):
        layout = ancpbids.BIDSLayout(DS005_DIR)

        subjects = layout.get_subjects()
        subjects_expected = ['%02d' % i for i in range(1, 17)]
        self.assertListEqual(subjects_expected, subjects)

        sessions = layout.get_sessions()
        self.assertEqual(0, len(sessions))

        tasks = layout.get_tasks()
        self.assertListEqual(['mixedgamblestask'], tasks)

    def test_bidslayout_get(self):
        layout = ancpbids.BIDSLayout(SYNTHETIC_DIR)
        mask_niftis = layout.get(scope='derivatives',
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
        layout = ancpbids.BIDSLayout(DS005_DIR)
        sorted_entities = layout.get_entities(scope='raw', sort=True)
        # note: 'ds' and 'type' entities are contained in folder 'models' at dataset level, so considered raw data
        self.assertListEqual(['ds', 'run', 'sub', 'task', 'type'], list(sorted_entities.keys()))
        self.assertListEqual(['1', '2', '3'], sorted_entities['run'])
        self.assertEqual(['%02d' % i for i in range(1, 17)], sorted_entities['sub'])
        self.assertListEqual(['mixedgamblestask'], sorted_entities['task'])

    def test_bidslayout_get_suffixes(self):
        layout = ancpbids.BIDSLayout(DS005_DIR)
        suffixes = layout.get_suffixes()
        self.assertListEqual(['T1w', 'bold', 'dwi', 'events', 'model'], suffixes)

    def test_bidslayout_get_extensions(self):
        layout = ancpbids.BIDSLayout(DS005_DIR)
        extensions = layout.get_extensions()
        self.assertListEqual(['.json', '.nii.gz', '.tsv'], extensions)

    def test_bidslayout_get_metadata(self):
        layout = ancpbids.BIDSLayout(DS005_DIR)
        metadata = layout.get_metadata(task='mixedgamblestask', suffix='bold')
        self.assertTrue(isinstance(metadata, dict))
        self.assertEqual(2.0, metadata['RepetitionTime'])
        self.assertEqual('mixed-gambles task', metadata['TaskName'])
        self.assertListEqual([0.0, 0.0571, 0.1143, 0.1714, 0.2286, 0.2857], metadata['SliceTiming'])

    def test_bidslayout_get_metadata_inheritance(self):
        layout = ancpbids.BIDSLayout(DS005_DIR + "-small")
        task_bold = layout.dataset.get_file('task-mixedgamblestask_bold.json').load_contents()
        # at the top level, RepetionTime is set to 2.0
        self.assertEqual(2.0, task_bold['RepetitionTime'])

        # now load all metadata matching the filter
        metadata = layout.get_metadata(task='mixedgamblestask', suffix='bold')
        self.assertTrue(isinstance(metadata, dict))

        # now, since at subject/run level the RepetionTime is overridden, it should be 2.5
        self.assertEqual(2.5, metadata['RepetitionTime'])

    def test_query_language(self):
        ds = ancpbids.load_dataset(DS005_DIR)
        schema = ds.get_schema()
        file_paths = ds.select(schema.Artifact) \
            .where(all_of(eq(schema.Artifact.suffix, 'bold'),
                          entity(schema, schema.EntityEnum._subject, '02'))) \
            .get_file_paths()
        file_paths = list(file_paths)
        self.assertEqual(3, len(file_paths))


if __name__ == '__main__':
    unittest.main()
