import os

from . import model
from . import files


# start monkey-patching generated code
def load_file_contents(folder: model.Folder, file_name):
    file_path = get_absolute_path(folder, file_name)
    contents = files.load_contents(file_path)
    return contents


def load_contents(file: model.File):
    file_path = get_absolute_path(file.parent_object_, file.name)
    contents = files.load_contents(file_path)
    return contents


def get_absolute_path_by_file(file: model.File):
    return get_absolute_path(file.parent_object_, file.name)


def get_absolute_path(folder: model.Folder, file_name):
    segments = [file_name]
    current_folder = folder
    while current_folder is not None:
        if isinstance(current_folder, model.Dataset):
            segments.insert(0, current_folder.get_base())
        else:
            segments.insert(0, current_folder.get_name())
        current_folder = current_folder.parent_object_
    abs_path = os.path.join(*segments)
    return abs_path


def remove_file(folder: model.Folder, file_name):
    folder.files = list(filter(lambda file: file.name != file_name, folder.files))


def get_file(folder: model.Folder, file_name):
    return next(filter(lambda file: file.name == file_name, folder.files), None)


def remove_folder(folder: model.Folder, folder_name):
    folder.folders = list(filter(lambda f: f.name != folder_name, folder.folders))


def get_folder(folder: model.Folder, folder_name):
    return next(filter(lambda f: f.name == folder_name, folder.folders), None)


def get_files_sorted(folder: model.Folder):
    return sorted(folder.get_files(), key=lambda f: f.name)


def get_folders_sorted(folder: model.Folder):
    return sorted(folder.get_folders(), key=lambda f: f.name)


setattr(model.Folder, 'load_file_contents', load_file_contents)
setattr(model.File, 'load_contents', load_contents)
setattr(model.Folder, 'remove_file', remove_file)
setattr(model.Folder, 'get_file', get_file)
setattr(model.Folder, 'remove_folder', remove_folder)
setattr(model.Folder, 'get_folder', get_folder)
setattr(model.Folder, 'get_files_sorted', get_files_sorted)
setattr(model.Folder, 'get_folders_sorted', get_folders_sorted)
setattr(model.File, 'get_absolute_path', get_absolute_path_by_file)

# end monkey-patching

from .pybids_compat import BIDSLayout

from . import _version
__version__ = _version.get_versions()['version']
