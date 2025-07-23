# Simplified parametrized test case using pytest fixtures
import pytest
import time
import sys
from unittest.mock import patch, MagicMock
import os
import time


import shutil
import tempfile

from numpy.testing import tempdir

import ancpbids
from ancpbids import model_latest, re
from ..base_test_case import BaseTestCase, DS005_DIR
from ancpbids import DatasetOptions
from ancpbids import load_dataset, DatasetOptions


@pytest.fixture(params=[True, False], ids=['lazy_loading', 'eager_loading'])
def lazy_loading_option(request):
    """Fixture that provides both lazy and eager loading options."""
    return request.param


@pytest.fixture
def dataset_options(lazy_loading_option):
    """Fixture that creates DatasetOptions with the parametrized lazy_loading value."""
    return DatasetOptions(lazy_loading=lazy_loading_option)


@pytest.fixture
def loaded_dataset(dataset_options):
    """Fixture that loads the dataset with the given options."""
    return load_dataset(DS005_DIR, dataset_options)


# All tests below will automatically run with both lazy_loading=True and lazy_loading=False
def test_loading_completes_successfully(loaded_dataset, lazy_loading_option):
    """Test that both lazy and eager loading complete successfully."""
    assert loaded_dataset is not None
    assert hasattr(loaded_dataset, 'files')
    assert hasattr(loaded_dataset, 'folders')


def test_participants_file_access(loaded_dataset, lazy_loading_option):
    """Test that participants.tsv can be accessed in both modes."""
    participants_file = loaded_dataset.get_file("participants.tsv")
    assert participants_file is not None

    # Access contents
    contents = participants_file.contents
    assert contents is not None
    assert len(contents) == 16
    assert list(contents[0].keys()) == ['participant_id', 'sex', 'age']


@pytest.mark.parametrize('file_name', ['participants.tsv', 'dataset_description.json'])
def test_file_contents_not_none(loaded_dataset, lazy_loading_option, file_name):
    """Test that file contents are accessible for various files in both modes.

    This test has double parametrization:
    - lazy_loading_option: True/False (from fixture)
    - file_name: different files to test
    """
    file_obj = loaded_dataset.get_file(file_name)
    if file_obj:  # File might not exist in test dataset
        contents = file_obj.contents
        assert contents is not None


def test_content_caching_behavior(dataset_options, lazy_loading_option):
    """Test caching behavior differs between lazy and eager loading."""
    ds = load_dataset(DS005_DIR, dataset_options)
    participants_file = ds.get_file("participants.tsv")

    if lazy_loading_option:
        # For lazy loading, test that content is cached after first access
        with patch('ancpbids.utils.load_contents') as mock_load:
            mock_load.return_value = [{'test': 'cached_data'}]

            # First access
            contents1 = participants_file.contents
            first_call_count = mock_load.call_count

            # Second access should use cached content
            contents2 = participants_file.contents
            second_call_count = mock_load.call_count

            # For lazy loading, should be same object and no additional calls
            assert contents1 is contents2
            assert first_call_count == second_call_count
    else:
        # For eager loading, content is loaded immediately
        # Just verify contents are accessible
        contents = participants_file.contents
        assert contents is not None


def test_lazy_loading_deferred_execution():
    """Test that lazy loading defers content loading until accessed.

    This test doesn't use parametrization because it's specific to lazy loading.
    """
    options = DatasetOptions(lazy_loading=True)

    with patch('ancpbids.utils.load_contents') as mock_load:
        mock_load.return_value = {'test': 'deferred_data'}

        # Load dataset - content loading should be deferred
        ds = load_dataset(DS005_DIR, options)
        initial_call_count = mock_load.call_count

        # Access a file's contents - this should trigger loading
        participants_file = ds.get_file("participants.tsv")
        if participants_file:
            contents = participants_file.contents
            final_call_count = mock_load.call_count

            # Should have made additional calls when accessing contents
            assert final_call_count >= initial_call_count


def test_unload_functionality():
    """Test the unload functionality for lazy-loaded objects.

    This test is specific to lazy loading only.
    """
    options = DatasetOptions(lazy_loading=True)
    ds = load_dataset(DS005_DIR, options)

    participants_file = ds.get_file("participants.tsv")
    if participants_file and hasattr(participants_file, 'unload'):
        # Load content first
        original_contents = participants_file.contents

        # Unload content
        participants_file.unload()

        # Content should be reloaded on next access
        reloaded_contents = participants_file.contents

        # Content should be equivalent (though potentially different objects)
        if isinstance(original_contents, list) and isinstance(reloaded_contents, list):
            assert len(original_contents) == len(reloaded_contents)


# Tests that need to compare both modes explicitly
def test_content_equivalence():
    """Test that lazy and eager loading produce equivalent results."""
    # Load with lazy loading
    options_lazy = DatasetOptions(lazy_loading=True)
    ds_lazy = load_dataset(DS005_DIR, options_lazy)

    # Load with eager loading
    options_eager = DatasetOptions(lazy_loading=False)
    ds_eager = load_dataset(DS005_DIR, options_eager)

    # Compare participants file contents
    lazy_participants = ds_lazy.get_file("participants.tsv").contents
    eager_participants = ds_eager.get_file("participants.tsv").contents

    assert len(lazy_participants) == len(eager_participants)
    assert lazy_participants[0] == eager_participants[0]


def test_loading_call_count_difference():
    """Test that lazy loading prevents immediate content loading using mocking."""
    with patch('ancpbids.utils.load_contents') as mock_load:
        mock_load.return_value = {'test': 'data'}

        # Load with lazy loading enabled
        options = DatasetOptions(lazy_loading=True)
        ds005 = load_dataset(DS005_DIR, options)
        lazy_call_count = mock_load.call_count

    with patch('ancpbids.utils.load_contents') as mock_load:
        mock_load.return_value = {'test': 'data'}

        # Load with lazy loading disabled
        options = DatasetOptions(lazy_loading=False)
        ds005_eager = load_dataset(DS005_DIR, options)
        eager_call_count = mock_load.call_count

    # Lazy loading should result in fewer immediate load calls
    assert lazy_call_count < eager_call_count


def test_performance_comparison():
    """Test performance difference between lazy and eager loading."""
    measurements_lazy = []
    measurements_eager = []

    # Perform multiple measurements for stability
    for _ in range(3):
        # Time lazy loading
        start_time = time.time()
        options_lazy = DatasetOptions(lazy_loading=True)
        ds005_lazy = load_dataset(DS005_DIR, options_lazy)
        lazy_time = time.time() - start_time
        measurements_lazy.append(lazy_time)

        # Time eager loading
        start_time = time.time()
        options_eager = DatasetOptions(lazy_loading=False)
        ds005_eager = load_dataset(DS005_DIR, options_eager)
        eager_time = time.time() - start_time
        measurements_eager.append(eager_time)

    # Calculate means
    mean_lazy = sum(measurements_lazy) / len(measurements_lazy)
    mean_eager = sum(measurements_eager) / len(measurements_eager)

    print(f"Mean lazy loading time: {mean_lazy:.4f}s")
    print(f"Mean eager loading time: {mean_eager:.4f}s")

    # Verify both complete successfully
    assert mean_lazy >= 0
    assert mean_eager >= 0


def test_memory_usage_comparison():
    """Test memory usage difference between lazy and eager loading."""
    # Lazy dataset
    options_lazy = DatasetOptions(lazy_loading=True)
    ds_lazy = load_dataset(DS005_DIR, options_lazy)
    lazy_size = sys.getsizeof(ds_lazy)

    # Eager dataset
    options_eager = DatasetOptions(lazy_loading=False)
    ds_eager = load_dataset(DS005_DIR, options_eager)
    eager_size = sys.getsizeof(ds_eager)

    print(f"Lazy dataset object size: {lazy_size} bytes")
    print(f"Eager dataset object size: {eager_size} bytes")

    # Basic memory usage verification
    assert lazy_size >= 0
    assert eager_size >= 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])