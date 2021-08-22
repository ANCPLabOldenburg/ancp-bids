import os

from . import model
from . import files
from .dsloader import DatasetLoader
from .dssaver import DatasetSaver
from .schema import Schema, NS_MAP
from . import utils


def load_dataset(base_dir: str):
    schema = Schema()
    loader = DatasetLoader(schema)
    ds = loader.load(base_dir)
    return ds


def save_dataset(ds: model.Dataset, target_dir: str):
    saver = DatasetSaver(ds._schema)
    return saver.save(ds, target_dir)


def to_etree(ds: model.Dataset):
    return ds.to_etree(nsmap_=NS_MAP)


# start monkey-patching generated code
from .query import XPathQuery


def load_file_contents(folder: model.Folder, file_name):
    file_path = get_absolute_path(folder, file_name)
    contents = files.load_contents(file_path)
    return contents


setattr(model.Folder, 'load_file_contents', load_file_contents)


def load_contents(file: model.File):
    file_path = get_absolute_path(file.parent_object_, file.name)
    contents = files.load_contents(file_path)
    return contents


setattr(model.File, 'load_contents', load_contents)


def get_absolute_path_by_file(file: model.File):
    return get_absolute_path(file.parent_object_, file.name)


setattr(model.File, 'get_absolute_path', get_absolute_path_by_file)


def get_absolute_path(folder: model.Folder, file_name):
    return _get_path(folder, file_name, True)


def _folder_get_relative_path(folder: model.Folder):
    return _get_path(folder, None, False)


setattr(model.Folder, 'get_relative_path', _folder_get_relative_path)


def _file_get_relative_path(file: model.File):
    return _get_path(file.parent_object_, file.name, False)


setattr(model.File, 'get_relative_path', _file_get_relative_path)


def _get_path(folder: model.Folder, file_name, absolute=True):
    segments = []
    if file_name:
        segments.append(file_name)
    current_folder = folder
    while current_folder is not None:
        if isinstance(current_folder, model.Dataset):
            if absolute:
                segments.insert(0, current_folder.base_dir_)
            # assume we reached the highest level, maybe not good for nested datasets
            break
        else:
            segments.insert(0, current_folder.get_name())
        current_folder = current_folder.parent_object_
    _path = os.path.join(*segments) if segments else ''
    return _path


def remove_file(folder: model.Folder, file_name):
    folder.files = list(filter(lambda file: file.name != file_name, folder.files))


setattr(model.Folder, 'remove_file', remove_file)


def get_file(folder: model.Folder, file_name):
    return next(filter(lambda file: file.name == file_name, folder.files), None)


setattr(model.Folder, 'get_file', get_file)


def remove_folder(folder: model.Folder, folder_name):
    folder.folders = list(filter(lambda f: f.name != folder_name, folder.folders))


setattr(model.Folder, 'remove_folder', remove_folder)


def get_folder(folder: model.Folder, folder_name):
    return next(filter(lambda f: f.name == folder_name, folder.folders), None)


setattr(model.Folder, 'get_folder', get_folder)


def get_files_sorted(folder: model.Folder):
    return sorted(folder.get_files(), key=lambda f: f.name)


setattr(model.Folder, 'get_files_sorted', get_files_sorted)


def get_folders_sorted(folder: model.Folder):
    return sorted(folder.get_folders(), key=lambda f: f.name)


setattr(model.Folder, 'get_folders_sorted', get_folders_sorted)

# end monkey-patching


from .pybids_compat import BIDSLayout

from . import _version

__version__ = _version.get_versions()['version']
