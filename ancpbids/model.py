import fnmatch
import os
from xml import etree

from .model_v1_7_0 import *


# start monkey-patching generated code

def has_entity(artifact: Artifact, entity_):
    for e in artifact.entities:
        if e.key == entity_:
            return True
    return False


Artifact.has_entity = has_entity


def get_entity(artifact: Artifact, entity_):
    for e in artifact.entities:
        if e.key == entity_:
            return e.value
    return None


Artifact.get_entity = get_entity


def add_entity(artifact: Artifact, key, value):
    if isinstance(key, EntityEnum):
        key = key.entity_
    eref = EntityRef(key, value)
    artifact.entities.append(eref)


Artifact.add_entity = add_entity


def load_file_contents(folder: Folder, file_name):
    from ancpbids import files
    file_path = get_absolute_path(folder, file_name)
    contents = files.load_contents(file_path)
    return contents


Folder.load_file_contents = load_file_contents


def load_contents(file: File):
    from ancpbids import files
    file_path = get_absolute_path(file.parent_object_, file.name)
    contents = files.load_contents(file_path)
    return contents


File.load_contents = load_contents


def get_absolute_path_by_file(file: File):
    return get_absolute_path(file.parent_object_, file.name)


File.get_absolute_path = get_absolute_path_by_file


def get_absolute_path(folder: Folder, file_name=None):
    return _get_path(folder, file_name, True)


def _folder_get_relative_path(folder: Folder):
    return _get_path(folder, None, False)


Folder.get_relative_path = _folder_get_relative_path
Folder.get_absolute_path = get_absolute_path


def _file_get_relative_path(file: File):
    return _get_path(file.parent_object_, file.name, False)


File.get_relative_path = _file_get_relative_path


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
    return _path


def remove_file(folder: Folder, file_name, from_meta=True):
    folder.files = list(filter(lambda file: file.name != file_name, folder.files))
    if from_meta:
        folder.metadatafiles = list(filter(lambda file: file.name != file_name, folder.metadatafiles))


Folder.remove_file = remove_file


def create_artifact(folder: Folder):
    artifact = Artifact()
    artifact.parent_object_ = folder
    folder.files.append(artifact)
    return artifact


Folder.create_artifact = create_artifact


def create_folder(folder: Folder, type_=Folder, **kwargs):
    sub_folder = type_(**kwargs)
    sub_folder.parent_object_ = folder
    folder.folders.append(sub_folder)
    return sub_folder


Folder.create_folder = create_folder


def create_derivative(ds: Dataset, **kwargs):
    derivatives_folder = ds.derivatives
    if not ds.derivatives:
        derivatives_folder = DerivativeFolder()
        derivatives_folder.parent_object_ = ds
        derivatives_folder.name = "derivatives"
        ds.derivatives = derivatives_folder
    derivative = DerivativeFolder(**kwargs)
    derivative.parent_object_ = derivatives_folder
    derivatives_folder.derivatives.append(derivative)

    derivative.dataset_description = DerivativeDatasetDescriptionFile()
    derivative.dataset_description.parent_object_ = derivative
    derivative.dataset_description.GeneratedBy = GeneratedBy()

    if ds.dataset_description:
        derivative.dataset_description.update(ds.dataset_description)

    return derivative


Dataset.create_derivative = create_derivative


def get_file(folder: Folder, file_name, from_meta=True):
    file = next(filter(lambda file: file.name == file_name, folder.files), None)
    if not file and from_meta:
        # search in metadatafiles
        file = next(filter(lambda file: file.name == file_name, folder.metadatafiles), None)
    return file


Folder.get_file = get_file


def get_files(folder: Folder, name_pattern):
    return list(filter(lambda file: fnmatch.fnmatch(file.name, name_pattern), folder.files))


Folder.get_files = get_files


def remove_folder(folder: Folder, folder_name):
    folder.folders = list(filter(lambda f: f.name != folder_name, folder.folders))


Folder.remove_folder = remove_folder


def get_folder(folder: Folder, folder_name):
    return next(filter(lambda f: f.name == folder_name, folder.folders), None)


Folder.get_folder = get_folder


def get_files_sorted(folder: Folder):
    return sorted(folder.files, key=lambda f: f.name)


Folder.get_files_sorted = get_files_sorted


def get_folders_sorted(folder: Folder):
    return sorted(folder.folders, key=lambda f: f.name)


Folder.get_folders_sorted = get_folders_sorted


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


to_generator = to_generator


def to_etree(source: dict, parent=None, name=None, id2x=None, x2id=None, nsmap_=None):
    if not name:
        name = type(source).__name__
    if parent is None:
        parent = etree.Element(name, nsmap=nsmap_)

    if isinstance(source, Model):
        if id2x is not None:
            id2x[id(source)] = parent
        if x2id is not None:
            x2id[parent] = source

    if isinstance(source, dict):
        for key, value in source.items():
            if value is None:
                continue
            context = parent
            if isinstance(value, dict):
                context = etree.SubElement(context, key)
            to_etree(value, parent=context, name=key, id2x=id2x, x2id=x2id, nsmap_=nsmap_)
    elif isinstance(source, list):
        for item in source:
            sub = etree.SubElement(parent, name)
            to_etree(item, parent=sub, name=name, id2x=id2x, x2id=x2id, nsmap_=nsmap_)
    else:
        sub = etree.SubElement(parent, name)
        sub.text = str(source)

    return parent


to_etree = to_etree


def to_dict(source: Model):
    return source


to_dict = to_dict


def query(ds: Dataset, expr: str):
    from ancpbids.query import XPathQuery
    query = XPathQuery(ds, ds._schema)
    return query.execute(expr), query


Dataset.query = query


def select(context: Model, target_type):
    from ancpbids.query import Select
    return Select(context, target_type)


Dataset.select = select

# end monkey-patching
