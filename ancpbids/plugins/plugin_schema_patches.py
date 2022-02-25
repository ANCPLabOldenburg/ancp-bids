import fnmatch
import os

from ancpbids import model
from ancpbids.model_v1_7_0 import *
from ancpbids.plugin import SchemaPlugin


def has_entity(artifact: Artifact, entity_):
    for e in artifact.entities:
        if e.key == entity_:
            return True
    return False


def get_entity(artifact: Artifact, entity_):
    for e in artifact.entities:
        if e.key == entity_:
            return e.value
    return None


def add_entity(artifact: Artifact, key, value):
    if isinstance(key, EntityEnum):
        key = key.entity_
    eref = EntityRef(key, value)
    artifact.entities.append(eref)


def load_file_contents(folder: Folder, file_name):
    from ancpbids import files
    file_path = get_absolute_path(folder, file_name)
    contents = files.load_contents(file_path)
    return contents


def load_contents(file: File):
    from ancpbids import files
    file_path = get_absolute_path(file.parent_object_, file.name)
    contents = files.load_contents(file_path)
    return contents


def get_absolute_path_by_file(file: File):
    return get_absolute_path(file.parent_object_, file.name)


def get_absolute_path(folder: Folder, file_name=None):
    return _get_path(folder, file_name, True)


def _folder_get_relative_path(folder: Folder):
    return _get_path(folder, None, False)


def _file_get_relative_path(file: File):
    return _get_path(file.parent_object_, file.name, False)


def _get_path(folder: Folder, file_name=None, absolute=True):
    segments = []
    if file_name:
        segments.append(file_name)
    current_folder = folder
    while current_folder is not None:
        if isinstance(current_folder, Dataset):
            if absolute:
                segments.insert(0, current_folder.base_dir_)
            # assume we reached the highest level, maybe not good for nested datasets
            break
        else:
            segments.insert(0, current_folder.name)
        current_folder = current_folder.parent_object_
    _path = os.path.join(*segments) if segments else ''
    return os.path.normpath(_path)


def remove_file(folder: Folder, file_name, from_meta=True):
    folder.files = list(filter(lambda file: file.name != file_name, folder.files))
    if from_meta:
        folder.metadatafiles = list(filter(lambda file: file.name != file_name, folder.metadatafiles))


def create_artifact(folder: Folder):
    artifact = Artifact()
    artifact.parent_object_ = folder
    folder.files.append(artifact)
    return artifact


def create_folder(folder: Folder, type_=Folder, **kwargs):
    sub_folder = type_(**kwargs)
    sub_folder.parent_object_ = folder
    folder.folders.append(sub_folder)
    return sub_folder


def create_derivative(ds: Dataset, **kwargs):
    derivatives_folder = ds.derivatives
    if not ds.derivatives:
        derivatives_folder = DerivativeFolder()
        derivatives_folder.parent_object_ = ds
        derivatives_folder.name = "derivatives"
        ds.derivatives = derivatives_folder
    derivative = DerivativeFolder(**kwargs)
    derivative.parent_object_ = derivatives_folder
    derivatives_folder.folders.append(derivative)

    derivative.dataset_description = DerivativeDatasetDescriptionFile()
    derivative.dataset_description.parent_object_ = derivative
    derivative.dataset_description.GeneratedBy = GeneratedBy()

    if ds.dataset_description:
        derivative.dataset_description.update(ds.dataset_description)

    return derivative


def get_file(folder: Folder, file_name, from_meta=True):
    file = next(filter(lambda file: file.name == file_name, folder.files), None)
    if not file and from_meta:
        # search in metadatafiles
        file = next(filter(lambda file: file.name == file_name, folder.metadatafiles), None)
    return file


def get_files(folder: Folder, name_pattern):
    return list(filter(lambda file: fnmatch.fnmatch(file.name, name_pattern), folder.files))


def remove_folder(folder: Folder, folder_name):
    folder.folders = list(filter(lambda f: f.name != folder_name, folder.folders))


def get_folder(folder: Folder, folder_name):
    return next(filter(lambda f: f.name == folder_name, folder.folders), None)


def get_files_sorted(folder: Folder):
    return sorted(folder.files, key=lambda f: f.name)


def get_folders_sorted(folder: Folder):
    return sorted(folder.folders, key=lambda f: f.name)


def to_generator(source: Model, depth_first=False, filter_=None):
    if not depth_first:
        if filter_ and not filter_(source):
            return
        yield source

    for key, value in source.items():
        if isinstance(value, Model):
            yield from to_generator(value, depth_first, filter_)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, Model):
                    yield from to_generator(item, depth_first, filter_)

    if depth_first:
        if filter_ and not filter_(source):
            return
        yield source


def iterancestors(source: Model):
    context = source
    while context is not None:
        if not hasattr(context, 'parent_object_'):
            break
        context = context.parent_object_
        yield context


def to_dict(source: Model):
    return source


class PatchingSchemaPlugin(SchemaPlugin):
    def execute(self, schema: model):
        schema.Artifact.has_entity = has_entity
        schema.Artifact.get_entity = get_entity
        schema.Artifact.add_entity = add_entity
        schema.Folder.load_file_contents = load_file_contents
        schema.File.load_contents = load_contents
        schema.File.get_absolute_path = get_absolute_path_by_file
        schema.Folder.get_relative_path = _folder_get_relative_path
        schema.Folder.get_absolute_path = get_absolute_path
        schema.File.get_relative_path = _file_get_relative_path
        schema.Folder.remove_file = remove_file
        schema.Folder.create_artifact = create_artifact
        schema.Folder.create_folder = create_folder
        schema.Dataset.create_derivative = create_derivative
        schema.Folder.get_file = get_file
        schema.Folder.get_files = get_files
        schema.Folder.remove_folder = remove_folder
        schema.Folder.get_folder = get_folder
        schema.Folder.get_files_sorted = get_files_sorted
        schema.Folder.get_folders_sorted = get_folders_sorted
        schema.Model.to_generator = to_generator
        schema.Model.to_dict = to_dict
        schema.Model.iterancestors = iterancestors
