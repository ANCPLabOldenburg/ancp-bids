import os
import ancpbids
from ..base_test_case import RESOURCES_FOLDER

def test_arbitrary_dataset_entities():
    """Test that querying entities in a non-BIDS-compliant dataset returns empty or minimal results."""
    dataset_path = os.path.join(RESOURCES_FOLDER, 'synthetic_arbitrary')
    layout = ancpbids.BIDSLayout(dataset_path)
    entities = layout.get_entities()
    print('Entities:', entities)
    assert isinstance(entities, dict)
    assert len(entities) == 0 or all(isinstance(v, dict) for v in entities.values())

def test_arbitrary_dataset_load_dataset():
    """Test loading a non-BIDS-compliant dataset and basic structure checks."""
    dataset_path = os.path.join(RESOURCES_FOLDER, 'synthetic_arbitrary')
    dataset = ancpbids.load_dataset(dataset_path)
    assert dataset is not None
    assert hasattr(dataset, 'subjects')
    assert isinstance(dataset.subjects, list)
    assert len(dataset.subjects) == 0
    # Check that the expected files and folders are present
    file_names = [f.name for f in dataset.files]
    folder_names = [f.name for f in dataset.folders]
    assert 'random.txt' in file_names
    assert 'subfolder1' in folder_names
    assert 'subfolder2' in folder_names

def test_arbitrary_dataset_query_all_files():
    """Test that all expected files are found using query()."""
    dataset_path = os.path.join(RESOURCES_FOLDER, 'synthetic_arbitrary')
    dataset = ancpbids.load_dataset(dataset_path)
    files = dataset.query(return_type='object')
    file_names = sorted(f.name for f in files)
    expected = sorted(['random.txt', 'notes.md', 'data.csv'])
    assert all(name in file_names for name in expected)

def test_arbitrary_dataset_query_all_folders():
    """Test that all expected folders and their files exist using get_folder()."""
    dataset_path = os.path.join(RESOURCES_FOLDER, 'synthetic_arbitrary')
    dataset = ancpbids.load_dataset(dataset_path)
    folder_names = [f.name for f in dataset.folders]
    assert 'subfolder1' in folder_names
    assert 'subfolder2' in folder_names

    subfolder1 = dataset.get_folder('subfolder1')
    subfolder2 = dataset.get_folder('subfolder2')
    assert subfolder1 is not None
    assert subfolder2 is not None
    subfolder1_files = [f.name for f in subfolder1.files]
    subfolder2_files = [f.name for f in subfolder2.files]
    assert 'notes.md' in subfolder1_files
    assert 'data.csv' in subfolder2_files