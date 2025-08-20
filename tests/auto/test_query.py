

import os
import ancpbids
from ancpbids import select, re, any_of, all_of, eq, op, entity
from ..base_test_case import ENTITIES_DIR, DS005_DIR, SYNTHETIC_DIR

def test_entities_formatting():
    layout = ancpbids.load_dataset(ENTITIES_DIR)
    files = layout.query(sub='02', run='3', return_type='filename')
    assert len(files) == 1
    assert files[0].endswith("sub-02_task-abc_run-00003_events.tsv")

    files = layout.query(sub='02', run=['000000003'], return_type='filename')
    assert len(files) == 1
    assert files[0].endswith("sub-02_task-abc_run-00003_events.tsv")

    # should also handle invalid formats, i.e. run not as an index but a label
    files = layout.query(sub='02', run='xyz', return_type='filename')
    assert len(files) == 1
    assert files[0].endswith("sub-02_task-abc_run-xyz_events.tsv")

def test_bidslayout_entities_any():
    layout = ancpbids.load_dataset(ENTITIES_DIR)
    files = layout.query(sub='*', suffix='test', task='abc', return_type='filename')
    assert len(files) == 2
    assert files[0].endswith("sub-bar_task-abc_test.txt")
    assert files[1].endswith("sub-foo_task-abc_test.txt")

def test_bidslayout_subjects_filtered():
    layout = ancpbids.load_dataset(ENTITIES_DIR)
    subjects = layout.query(target="sub", task='abc')
    assert len(subjects) == 3
    assert ['02', 'bar', 'foo'] == subjects

def test_bidslayout():
    layout = ancpbids.load_dataset(DS005_DIR)
    ents = layout.query_entities()
    subjects = ents["subject"]
    subjects_expected = {'%02d' % i for i in range(1, 17)}
    assert subjects_expected == subjects
    assert "session" not in ents
    tasks = ents["task"]
    assert {'mixedgamblestask'} == tasks

def test_bidslayout_get():
    layout = ancpbids.load_dataset(SYNTHETIC_DIR)
    mask_niftis = layout.query(scope='derivatives',
                               return_type='filename',
                               suffix='mask',
                               extension='.nii',
                               sub='03',
                               ses='02',
                               task='nback',
                               run=["01", "02"])
    assert len(mask_niftis) == 4
    # If you want to check the actual file paths, add the expected_paths check here
    expected_paths = [
        'derivatives/fmriprep/sub-03/ses-02/func/sub-03_ses-02_task-nback_run-01_space-MNI152NLin2009cAsym_desc-brain_mask.nii',
        'derivatives/fmriprep/sub-03/ses-02/func/sub-03_ses-02_task-nback_run-01_space-T1w_desc-brain_mask.nii',
        'derivatives/fmriprep/sub-03/ses-02/func/sub-03_ses-02_task-nback_run-02_space-MNI152NLin2009cAsym_desc-brain_mask.nii',
        'derivatives/fmriprep/sub-03/ses-02/func/sub-03_ses-02_task-nback_run-02_space-T1w_desc-brain_mask.nii',
    ]
    expected_paths = list(map(lambda p: os.path.normpath(os.path.join(SYNTHETIC_DIR, p)), expected_paths))
    for file in expected_paths:
        assert any(file == p for p in mask_niftis)

def test_bidslayout_get_entities():
    layout = ancpbids.load_dataset(DS005_DIR)
    sorted_entities = layout.query_entities(scope='raw', sort=True)
    assert ['ds', 'run', 'subject', 'task', 'type'] == list(sorted_entities.keys())
    assert [1, 2, 3] == sorted_entities['run']
    assert ['%02d' % i for i in range(1, 17)] == sorted_entities['subject']
    assert ['mixedgamblestask'] == sorted_entities['task']

def test_bidslayout_get_suffixes():
    layout = ancpbids.load_dataset(DS005_DIR)
    suffixes = layout.query(target="suffixe")
    assert ['T1w', 'bold', 'dwi', 'events', 'model'] == suffixes

def test_bidslayout_get_extensions():
    layout = ancpbids.load_dataset(DS005_DIR)
    extensions = layout.query(target="extension")
    assert ['.json', '.nii.gz', '.tsv'] == extensions

def test_bidslayout_get_metadata():
    layout = ancpbids.load_dataset(DS005_DIR)
    metadata = layout.get_file("sub-01/func/sub-01_task-mixedgamblestask_run-01_bold.nii.gz").get_metadata(
        include_entities=True)
    assert isinstance(metadata, dict)
    assert metadata['RepetitionTime'] == 2.0
    assert metadata['TaskName'] == 'mixed-gambles task'
    assert metadata['SliceTiming'] == [0.0, 0.0571, 0.1143, 0.1714, 0.2286, 0.2857]
    assert metadata['subject'] == '01'
    assert metadata['task'] == 'mixedgamblestask'
    assert metadata['run'] == 1

def test_query_language():
    ds = ancpbids.load_dataset(DS005_DIR)
    schema = ds.get_schema()
    file_paths = ds.select(schema.Artifact) \
        .where(all_of(eq(schema.Artifact.suffix, 'bold'),
                      entity(schema, schema.EntityEnum.subject, '02'))) \
        .get_file_paths()
    file_paths = list(file_paths)
    assert len(file_paths) == 3


