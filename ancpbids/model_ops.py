"""Graph behavior shared by all BIDS schema versions.

These mixins are bases of the types in model_base. Version-specific logic
(enums, create_dataset, entity value processing) lives on Schema.
"""
import fnmatch
import os
from enum import Enum
from typing import Any, Callable, Dict, Iterator, List, Optional, TYPE_CHECKING, Type, Union

from ancpbids.utils import convert_to_relative, resolve_segments

if TYPE_CHECKING:
    from ancpbids.query import Select
    from ancpbids.schema import Schema
    from .model_base import (
        Artifact,
        DatasetDescriptionFile,
        DerivativeFolder,
        File,
        Folder,
        Model,
    )

FilterFn = Callable[["Model"], bool]
QueryResult = Union[List[str], List[object]]


class LazyContents:
    """Resolve callable contents on first access (lazy file loading)."""

    load_contents: Callable[[], Any]
    _contents: Any
    get: Callable[..., Any]

    @property
    def contents(self) -> Any:
        if hasattr(self, '_contents'):
            value = self._contents
        else:
            value = self.get('contents')
        if callable(value):
            value = value()
            self._contents = value
        return value

    @contents.setter
    def contents(self, value: Any) -> None:
        self._contents = value

    def unload(self) -> None:
        self._contents = self.load_contents


class ModelOps:
    parent_object_: Optional["Model"]

    def __hash__(self) -> int:
        return hash(tuple(self))

    def get_schema(self) -> Optional["Schema"]:
        from .model_base import Dataset
        current = self
        while current is not None:
            if isinstance(current, Dataset):
                return current._versioned_schema
            current = getattr(current, 'parent_object_', None)
        return None

    def get_parent(self) -> Optional["Model"]:
        return getattr(self, 'parent_object_', None)

    def to_dict(self) -> dict:
        return self

    def iterancestors(self) -> Iterator["Model"]:
        context = self
        while context is not None:
            if not hasattr(context, 'parent_object_'):
                break
            context = context.parent_object_
            yield context

    def to_generator(
            self,
            depth_first: bool = False,
            filter_: Optional[FilterFn] = None,
            depth: int = 1000) -> Iterator["Model"]:
        if depth < 0:
            return
        if not depth_first:
            if filter_ and not filter_(self):
                return
            yield self
        for value in self.values():
            yield from _generate_models(value, depth_first, filter_, depth)
        if depth_first:
            if filter_ and not filter_(self):
                return
            yield self


def _generate_models(
        value: Any,
        depth_first: bool,
        filter_: Optional[FilterFn],
        depth: int) -> Iterator["Model"]:
    from .model_base import Model
    if isinstance(value, Model):
        yield from value.to_generator(depth_first, filter_, depth - 1)
        return
    if not isinstance(value, list):
        return
    for item in value:
        if isinstance(item, Model):
            yield from item.to_generator(depth_first, filter_, depth - 1)


def _get_path(
        folder: Optional["Folder"],
        file_name: Optional[str] = None,
        absolute: bool = True) -> str:
    from .model_base import Dataset
    segments = []
    if file_name:
        segments.append(file_name)
    current_folder = folder
    while current_folder is not None:
        if isinstance(current_folder, Dataset):
            if not current_folder.base_dir_.endswith(current_folder.name):
                segments.insert(0, current_folder.name)
            if absolute:
                segments.insert(0, current_folder.base_dir_)
            break
        segments.insert(0, current_folder.name)
        current_folder = current_folder.parent_object_
    path = os.path.join(*segments) if segments else ''
    path = os.path.normpath(path)
    if absolute:
        path = os.path.abspath(path)
    return path


class FileOps:
    name: str
    parent_object_: Optional["Folder"]

    def load_contents(self) -> Any:
        from ancpbids import utils
        file_path = _get_path(self.parent_object_, self.name, True)
        return utils.load_contents(file_path)

    def get_absolute_path(self) -> str:
        return _get_path(self.parent_object_, self.name, True)

    def get_relative_path(self) -> str:
        return _get_path(self.parent_object_, self.name, False)


class ArtifactOps:
    entities: Dict[str, Any]
    suffix: Optional[str]

    def has_entity(self, entity_: str) -> bool:
        return entity_ in self.entities

    def get_entity(self, entity_: str) -> Any:
        return self.entities.get(entity_)

    def get_entities(self) -> Dict[str, Any]:
        return dict(self.entities)

    def add_entity(self, key: Union[str, Enum], value: Any) -> None:
        schema = self.get_schema()
        if schema is not None and isinstance(key, schema.EntityEnum):
            key = key.value['name']
        self.entities[key] = value

    def add_entities(self, **kwargs: Any) -> None:
        for key, value in kwargs.items():
            self.add_entity(key, value)

    def sidecar(self, **entities: Any) -> QueryResult:
        filters = dict(**self.get_entities())
        filters.update(**entities)
        return self.get_parent().query(**filters)

    def get_metadata(self, include_entities: bool = False) -> dict:
        from ancpbids.utils import deepupdate
        schema = self.get_schema()
        parent = self.get_parent()
        artifact_entities = self.entities
        metadata_levels = []
        while parent is not None:
            for parent_mdf in parent.select(schema.MetadataArtifact).objects(depth=1):
                if parent_mdf.suffix != self.suffix:
                    continue
                mdf_entities = parent_mdf.entities
                if mdf_entities.items() <= artifact_entities.items():
                    metadata_levels.append(parent_mdf.contents)
            parent = parent.get_parent()

        metadata = {}
        for mdf in reversed(metadata_levels):
            deepupdate(metadata, mdf)
        if include_entities:
            schema_entities = {e.value['name']: e.name for e in list(schema.EntityEnum)}
            metadata.update({schema_entities[key]: value for key, value in artifact_entities.items()})
        return metadata

    def write(self) -> str:
        from ancpbids.plugins.plugin_dssaver import write_artifact
        return write_artifact(self)


class FolderOps:
    files: List["File"]
    folders: List["Folder"]
    name: str

    def select(self, target_type: Type["Model"]) -> "Select":
        from ancpbids.query import Select
        return Select(self, target_type)

    def query(self, return_type: str = 'object', target: Optional[str] = None,
              scope: Optional[str] = None, extension: Union[str, List[str]] = None,
              suffix: Union[str, List[str]] = None, regex_search: bool = False,
              sorter: Optional[Callable] = None, **entities: Any) -> QueryResult:
        from ancpbids.query import query
        return query(self, return_type, target, scope, extension, suffix, regex_search, sorter, **entities)

    def query_entities(self, scope: Optional[str] = None, sort: bool = False,
                       long_form: bool = True) -> dict:
        from ancpbids.query import query_entities
        return query_entities(self, scope, sort, long_form)

    def load_file_contents(self, file_name: str, return_type: Optional[str] = None) -> Any:
        from ancpbids import utils
        return utils.load_contents(_get_path(self, file_name, True), return_type)

    def get_absolute_path(self, file_name: Optional[str] = None) -> str:
        return _get_path(self, file_name, True)

    def get_relative_path(self) -> str:
        return _get_path(self, None, False)

    def remove_file(self, file_name: str) -> None:
        self.files = [file for file in self.files if file.name != file_name]

    def create_artifact(self, raw: Optional["Artifact"] = None) -> "Artifact":
        from .model_base import Artifact
        artifact = Artifact()
        if isinstance(raw, Artifact):
            artifact.entities = dict(raw.entities)
        artifact.parent_object_ = self
        self.files.append(artifact)
        return artifact

    def create_folder(self, type_: Optional[Type["Folder"]] = None, **kwargs: Any) -> "Folder":
        from .model_base import Folder
        if not type_:
            type_ = Folder
        sub_folder = type_(**kwargs)
        sub_folder.parent_object_ = self
        self.folders.append(sub_folder)
        return sub_folder

    def get_file(self, file_name: str) -> Optional["File"]:
        from .model_base import File
        folder, file_name = resolve_segments(self, file_name, True)
        if not folder:
            return None
        for file in folder.files:
            if file.name == file_name:
                return file
        # Schema members may hold promoted File objects (e.g. dataset_description).
        for value in folder.values():
            if isinstance(value, File) and value.name == file_name:
                return value
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, File) and item.name == file_name:
                        return item
        return None

    def get_files(self, name_pattern: str) -> List["File"]:
        from .model_base import File
        matches = [file for file in self.files if fnmatch.fnmatch(file.name, name_pattern)]
        for value in self.values():
            if isinstance(value, File) and fnmatch.fnmatch(value.name, name_pattern):
                if value not in matches:
                    matches.append(value)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, File) and fnmatch.fnmatch(item.name, name_pattern):
                        if item not in matches:
                            matches.append(item)
        return matches

    def remove_folder(self, folder_name: str) -> None:
        self.folders = [folder for folder in self.folders if folder.name != folder_name]

    def get_folder(self, folder_name: str) -> Optional["Folder"]:
        from .model_base import Folder
        for folder in self.folders:
            if folder.name == folder_name:
                return folder
        for value in self.values():
            if isinstance(value, Folder) and value.name == folder_name:
                return value
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, Folder) and item.name == folder_name:
                        return item
        return None

    def get_files_sorted(self) -> List["File"]:
        return sorted(self.files, key=lambda f: f.name)

    def get_folders_sorted(self) -> List["Folder"]:
        return sorted(self.folders, key=lambda f: f.name)


class DatasetOps:
    derivatives: Optional["Folder"]
    dataset_description: Optional["DatasetDescriptionFile"]

    def create_derivative(self, path: Optional[str] = None, **kwargs: Any) -> "DerivativeFolder":
        from .model_base import DerivativeDatasetDescriptionFile, DerivativeFolder, GeneratedBy
        derivatives_folder = self.derivatives
        if not self.derivatives:
            derivatives_folder = DerivativeFolder()
            derivatives_folder.parent_object_ = self
            derivatives_folder.name = "derivatives"
            self.derivatives = derivatives_folder
        path = convert_to_relative(self, path)
        target_folder, _ = resolve_segments(derivatives_folder, path, create_if_missing=True)
        derivative = DerivativeFolder(**kwargs)
        derivative.parent_object_ = target_folder
        target_folder.folders.append(derivative)
        derivative.dataset_description = DerivativeDatasetDescriptionFile()
        derivative.dataset_description.parent_object_ = derivative
        derivative.dataset_description.GeneratedBy = GeneratedBy()
        if self.dataset_description:
            derivative.dataset_description.update(self.dataset_description)
        return derivative

    def pickle(self, custom_dir: Optional[str] = None) -> None:
        from ancpbids.plugins.plugin_pickle import pickle_dataset
        return pickle_dataset(self, custom_dir)
