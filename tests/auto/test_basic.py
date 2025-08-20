
import os
import pytest
from ancpbids import load_dataset, DatasetOptions
from ancpbids.utils import parse_bids_name
from ..base_test_case import DS005_DIR

def test_naming_scheme():
    valid_names = ["sub-11_task-mixedgamblestask_run-02_events.tsv", "sub-11_dwi.nii.gz", "x-01_y-02_z-03_xyz.abc",
                   "sub-01_task-mixedgamblestask_run-01_bold.nii.gz"]
    for name in valid_names:
        assert parse_bids_name(name) is not None

    invalid_names = ["sub-04_T1w_bias.nii.gz", "cat.jpg", "readme.txt"]
    for name in invalid_names:
        assert parse_bids_name(name) is None

def test_parse_bids_name():
    bids_obj = parse_bids_name("sub-11_task-mixedgamblestask_run-02_bold.nii.gz")
    assert isinstance(bids_obj, dict)
    assert ['sub', 'task', 'run'] == list(bids_obj['entities'].keys())
    assert ['11', 'mixedgamblestask', '02'] == list(bids_obj['entities'].values())
    assert 'bold' == bids_obj['suffix']
    assert '.nii.gz' == bids_obj['extension']

@pytest.mark.parametrize("lazy_loading", [True, False])
def test_ds005_basic_structure(lazy_loading):
    ds005 = load_dataset(DS005_DIR, DatasetOptions(lazy_loading=lazy_loading))
    assert ds005.name == "ds005"

    ds_descr = ds005.dataset_description
    assert isinstance(ds_descr, ds005.get_schema().DatasetDescriptionFile)
    assert ds_descr.name == 'dataset_description.json'
    assert ds_descr.BIDSVersion == "1.0.0rc2"
    assert ds_descr.Name == "Mixed-gambles task"
    assert ds_descr.License.startswith(
        "This dataset is made available under the Public Domain Dedication and License")
    assert [
        "Tom, S.M., Fox, C.R., Trepel, C., "
        "Poldrack, R.A. (2007). "
        "The neural basis of loss aversion in decision-making under risk. "
        "Science, 315(5811):515-8"] == ds_descr.ReferencesAndLinks

    subjects = ds005.subjects
    assert len(subjects) == 16

    first_subject = subjects[0]
    assert first_subject.name == "sub-01"
    last_subject = subjects[-1]
    assert last_subject.name == "sub-16"

    sessions = first_subject.sessions
    assert len(sessions) == 0

    datatypes = first_subject.datatypes
    assert len(datatypes) == 3

    anat_datatype = datatypes[0]
    assert anat_datatype.name == "anat"
    func_datatype = datatypes[-1]
    assert func_datatype.name == "func"

    artifacts = func_datatype.query(suffix="bold", scope="self")
    assert len(artifacts) == 3
    assert artifacts[0].name == "sub-01_task-mixedgamblestask_run-01_bold.nii.gz"
    assert artifacts[1].name == "sub-01_task-mixedgamblestask_run-02_bold.nii.gz"
    assert artifacts[2].name == "sub-01_task-mixedgamblestask_run-03_bold.nii.gz"

    eventmetafiles = func_datatype.query(suffix="events", extension=".json", scope="self")
    assert len(eventmetafiles) == 1
    assert eventmetafiles[0].name == "sub-01_task-mixedgamblestask_run-01_events.json"

    tsvfiles = func_datatype.query(extension=".tsv", scope="self")
    assert len(tsvfiles) == 3
    assert tsvfiles[0].name == "sub-01_task-mixedgamblestask_run-01_events.tsv"
    assert tsvfiles[1].name == "sub-01_task-mixedgamblestask_run-02_events.tsv"
    assert tsvfiles[2].name == "sub-01_task-mixedgamblestask_run-03_events.tsv"

@pytest.mark.parametrize("lazy_loading", [True, False])
def test_json_file_contents(lazy_loading):
    ds005 = load_dataset(DS005_DIR, DatasetOptions(lazy_loading=lazy_loading))
    dataset_description = ds005.load_file_contents("dataset_description.json")
    assert isinstance(dataset_description, dict)
    assert dataset_description['BIDSVersion'] == "1.0.0rc2"
    assert dataset_description['Name'] == "Mixed-gambles task"

@pytest.mark.parametrize("lazy_loading", [True, False])
def test_tsv_file_contents(lazy_loading):
    ds005 = load_dataset(DS005_DIR, DatasetOptions(lazy_loading=lazy_loading))
    participants = ds005.load_file_contents("participants.tsv")
    assert ['participant_id', 'sex', 'age'] == list(participants[0].keys())
    assert len(participants) == 16
    participants = ds005.load_file_contents("participants.tsv", return_type="ndarray")
    assert ['participant_id', 'sex', 'age'] == list(participants.dtype.names)
    assert len(participants) == 16
    participants = ds005.load_file_contents("participants.tsv", return_type="dataframe")
    assert ['participant_id', 'sex', 'age'] == list(participants.columns)
    assert len(participants) == 16

@pytest.mark.parametrize("lazy_loading", [True, False])
def test_parse_entities_in_filenames(lazy_loading):
    ds005 = load_dataset(DS005_DIR, DatasetOptions(lazy_loading=lazy_loading))
    artifact = ds005.subjects[0].datatypes[-1].query(scope="self")[0]
    assert isinstance(artifact, ds005.get_schema().Artifact)
    assert artifact.suffix == "bold"
    assert artifact.extension == ".nii.gz"
    entities = artifact.entities
    assert isinstance(entities, list)
    assert len(entities) == 3
    entity = entities[0]
    assert entity.key == "sub"
    assert entity.value == "01"
    entity = entities[1]
    assert entity.key == "task"
    assert entity.value == "mixedgamblestask"
    entity = entities[2]
    assert entity.key == "run"
    assert entity.value == 1

@pytest.mark.parametrize("lazy_loading", [True, False])
def test_to_generator(lazy_loading):
    ds005 = load_dataset(DS005_DIR, DatasetOptions(lazy_loading=lazy_loading))
    schema = ds005.get_schema()
    all_direct_files = list(ds005.to_generator(depth_first=True, depth=1, filter_=lambda n: isinstance(n, schema.File)))
    assert len(all_direct_files) == 8

@pytest.mark.parametrize("lazy_loading", [True, False])
def test_get_files_and_folders(lazy_loading):
    ds005 = load_dataset(DS005_DIR, DatasetOptions(lazy_loading=lazy_loading))
    file = ds005.get_file("dataset_description.json")
    assert file is not None
    assert file.name == "dataset_description.json"
    file = ds005.get_file("sub-01/func/sub-01_task-mixedgamblestask_run-01_bold.nii.gz")
    assert file is not None
    assert file.name == "sub-01_task-mixedgamblestask_run-01_bold.nii.gz"

@pytest.mark.parametrize("lazy_loading", [True, False])
def test_repr(lazy_loading):
    ds005 = load_dataset(DS005_DIR, DatasetOptions(lazy_loading=lazy_loading))
    assert str(ds005) == "{'name': 'ds005'}"
    assert str(ds005.derivatives) == "{'name': 'derivatives'}"
    assert str(ds005.README) == "{'name': 'README'}"
    expected = "{'name': 'dataset_description.json', 'Name': 'Mixed-gambles task', 'BIDSVersion': '1.0.0rc2', 'License': 'This dataset is made available u[...]'}"
    assert str(ds005.dataset_description) == expected

@pytest.mark.parametrize("lazy_loading", [True, False])
def test_participants_tsv(lazy_loading):
    ds005 = load_dataset(DS005_DIR, DatasetOptions(lazy_loading=lazy_loading))
    schema = ds005.get_schema()
    assert isinstance(ds005.participants_tsv, schema.TSVFile)
    contents = ds005.participants_tsv.contents
    assert contents is not None
    assert len(contents) == 16
    assert ['participant_id', 'sex', 'age'] == list(contents[0].keys())
    assert ['sub-01', '0', '28'] == list(contents[0].values())
    assert contents[0] == {'participant_id': 'sub-01', 'sex': '0', 'age': '28'}

@pytest.mark.parametrize("lazy_loading", [True, False])
def test_absolute_path(lazy_loading):
    ds_path_norm = os.path.normpath(DS005_DIR)
    ds005 = load_dataset(ds_path_norm, DatasetOptions(lazy_loading=lazy_loading))
    ds_path = ds005.get_absolute_path()
    assert ds_path == ds_path_norm

@pytest.mark.parametrize("lazy_loading", [True, False])
def test_datatype_of_artifact(lazy_loading):
    ds005 = load_dataset(DS005_DIR, DatasetOptions(lazy_loading=lazy_loading))
    anat_files = ds005.query(scope="raw", sub="01", suffix="T1w")
    assert len(anat_files) == 1
    assert anat_files[0].datatype is None
    ds005 = load_dataset(DS005_DIR, DatasetOptions(infer_artifact_datatype=True, lazy_loading=lazy_loading))
    anat_files = ds005.query(scope="raw", sub="01", suffix="T1w")
    assert len(anat_files) == 1
    assert anat_files[0].datatype == "anat"


