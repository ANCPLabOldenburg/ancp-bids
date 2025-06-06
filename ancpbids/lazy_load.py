from enum import Enum, auto
from typing import List, Union, Dict, Any
from math import inf
import sys
import os

class LazyLoadingMixin:
    """Mixin to provide lazy loading capabilities for file objects."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._contents = None
        self._is_lazy = False
        self._is_loaded = False

    def _load_contents_impl(self):
        """Override this method in subclasses to define how to load contents."""
        raise NotImplementedError("Subclasses must implement _load_contents_impl")

    def set_lazy_loading(self, enabled=True):
        """Enable or disable lazy loading for this file."""
        self._is_lazy = enabled
        if not enabled and not self._is_loaded:
            # If disabling lazy loading and not loaded yet, load now
            self._contents = self._load_contents_impl()
            self._is_loaded = True

    @property
    def contents(self):
        """Get file contents, loading them if necessary."""
        if self._is_lazy and not self._is_loaded:
            self._contents = self._load_contents_impl()
            self._is_loaded = True
        return self._contents

    @contents.setter
    def contents(self, value):
        """Set file contents directly."""
        self._contents = value
        self._is_loaded = True

    def is_loaded(self):
        """Check if contents have been loaded."""
        return self._is_loaded

    def unload_contents(self):
        """Unload contents to free memory (only works with lazy loading)."""
        if self._is_lazy:
            self._contents = None
            self._is_loaded = False

    def get_absolute_path(self):
        """Get the absolute path to this file for loading."""
        if hasattr(self, 'parent_object_') and self.parent_object_:
            parent_path = self.parent_object_.get_absolute_path()
            return os.path.join(parent_path, self.name)
        return self.name


# Enhanced file classes with lazy loading
class LazyTSVFile(LazyLoadingMixin, TSVFile):
    """TSV file with lazy loading capabilities."""

    def _load_contents_impl(self):
        """Load TSV contents from file."""
        file_path = self.get_absolute_path()
        if os.path.exists(file_path):
            return utils.load_contents(file_path)  # Assuming utils.load_contents handles TSV
        return None


class LazyTSVArtifact(LazyLoadingMixin, TSVArtifact):
    """TSV artifact with lazy loading capabilities."""

    def _load_contents_impl(self):
        """Load TSV contents from file."""
        file_path = self.get_absolute_path()
        if os.path.exists(file_path):
            return utils.load_contents(file_path)
        return None


class LazyMetadataFile(LazyLoadingMixin, MetadataFile):
    """Metadata file with lazy loading capabilities."""

    def _load_contents_impl(self):
        """Load JSON contents from file."""
        file_path = self.get_absolute_path()
        if os.path.exists(file_path):
            return utils.load_contents(file_pa
        return None


class LazyMetadataArtifact(LazyLoadingMixin, MetadataArtifact):
    """Metadata artifact with lazy loading capabilities."""

    def _load_contents_impl(self):
        """Load JSON contents from file."""
        file_path = self.get_absolute_path()
        if os.path.exists(file_path):
            return utils.load_contents(file_path)
        return None