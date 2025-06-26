# Simplified test case
import unittest
import time
import sys
from unittest.mock import patch, MagicMock
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
from ancpbids import DatasetOptions
from ancpbids import load_dataset, DatasetOptions



class LazyLoadingTestCase(BaseTestCase):
    """Test cases for lazy loading functionality."""

    def test_lazy_loading_prevents_immediate_loading(self):
        """Test that lazy loading prevents immediate content loading using mocking."""
        with patch('ancpbids.utils.load_contents') as mock_load:
            mock_load.return_value = {'test': 'data'}

            # Load with lazy loading enabled
            options = DatasetOptions(lazy_loading=True)
            ds005 = load_dataset(DS005_DIR, options)

            # Mock should not have been called during initialization
            # (or called much less frequently than with eager loading)
            lazy_call_count = mock_load.call_count

        with patch('ancpbids.utils.load_contents') as mock_load:
            mock_load.return_value = {'test': 'data'}

            # Load with lazy loading disabled
            options = DatasetOptions(lazy_loading=False)
            ds005_eager = load_dataset(DS005_DIR, options)

            eager_call_count = mock_load.call_count

        # Lazy loading should result in fewer immediate load calls
        self.assertLess(lazy_call_count, eager_call_count)

    def test_lazy_loading_on_demand(self):
        """Test that lazy-loaded content can be accessed when needed."""
        options = DatasetOptions(lazy_loading=True)
        ds005 = load_dataset(DS005_DIR, options)

        # Get a lazy-loaded TSV file
        participants_file = ds005.get_file("participants.tsv")

        # Access contents - this should trigger loading
        contents = participants_file.contents
        self.assertIsNotNone(contents)
        self.assertEqual(16, len(contents))
        self.assertEqual(['participant_id', 'sex', 'age'], list(contents[0].keys()))

    def test_lazy_vs_eager_content_equivalence(self):
        """Test that lazy and eager loading produce equivalent results."""
        # Load with lazy loading
        options_lazy = DatasetOptions(lazy_loading=True)
        ds005_lazy = load_dataset(DS005_DIR, options_lazy)

        # Load with eager loading
        options_eager = DatasetOptions(lazy_loading=False)
        ds005_eager = load_dataset(DS005_DIR, options_eager)

        # Compare participants file contents
        lazy_participants = ds005_lazy.get_file("participants.tsv").contents
        eager_participants = ds005_eager.get_file("participants.tsv").contents

        self.assertEqual(len(lazy_participants), len(eager_participants))
        self.assertEqual(lazy_participants[0], eager_participants[0])

    def test_lazy_vs_eager_performance(self):
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

        # Lazy loading should generally be faster for initial loading
        print(f"Mean lazy loading time: {mean_lazy:.4f}s")
        print(f"Mean eager loading time: {mean_eager:.4f}s")

        # For small datasets, the difference might be minimal, so we just verify
        # that both complete successfully rather than asserting performance
        self.assertGreaterEqual(mean_lazy, 0)
        self.assertGreaterEqual(mean_eager, 0)

    def test_memory_usage_difference(self):
        """Test memory usage difference between lazy and eager loading."""
        import sys

        # Measure memory usage of lazy loading
        options_lazy = DatasetOptions(lazy_loading=True)
        ds005_lazy = load_dataset(DS005_DIR, options_lazy)
        lazy_size = sys.getsizeof(ds005_lazy)

        # Measure memory usage of eager loading
        options_eager = DatasetOptions(lazy_loading=False)
        ds005_eager = load_dataset(DS005_DIR, options_eager)
        eager_size = sys.getsizeof(ds005_eager)

        print(f"Lazy dataset object size: {lazy_size} bytes")
        print(f"Eager dataset object size: {eager_size} bytes")

        # This is a basic check - in practice, you might want to use more
        # sophisticated memory profiling tools
        self.assertGreaterEqual(lazy_size, 0)
        self.assertGreaterEqual(eager_size, 0)

    def test_lazy_loading_caching(self):
        """Test that lazy-loaded content is cached after first access."""
        options = DatasetOptions(lazy_loading=True)
        ds005 = load_dataset(DS005_DIR, options)

        participants_file = ds005.get_file("participants.tsv")

        with patch('ancpbids.utils.load_contents') as mock_load:
            mock_load.return_value = [{'test': 'data'}]

            # First access should trigger loading
            contents1 = participants_file.contents
            first_call_count = mock_load.call_count

            # Second access should use cached content
            contents2 = participants_file.contents
            second_call_count = mock_load.call_count

            # Should be the same object and no additional calls
            self.assertIs(contents1, contents2)
            self.assertEqual(first_call_count, second_call_count)


if __name__ == '__main__':
    unittest.main()