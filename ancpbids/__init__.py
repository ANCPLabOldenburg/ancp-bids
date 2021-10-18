import fnmatch
import os
from lxml import etree

from . import files
from . import model
from . import utils
from .dsloader import DatasetLoader
from .dssaver import DatasetSaver
from .schema import Schema
from .query import XPathQuery, BoolExpr, Select, EqExpr, AnyExpr, AllExpr, ReExpr, CustomOpExpr, EntityExpr
from .validator import ValidationReport

SCHEMA_LATEST = Schema(model)


def load_dataset(base_dir: str, bids_schema=SCHEMA_LATEST):
    loader = DatasetLoader(bids_schema)
    ds = loader.load(base_dir)
    return ds


def save_dataset(ds: model.Dataset, target_dir: str):
    saver = DatasetSaver(ds._schema)
    return saver.save(ds, target_dir)


# start monkey-patching generated code
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
            segments.insert(0, current_folder.name)
        current_folder = current_folder.parent_object_
    _path = os.path.join(*segments) if segments else ''
    return _path


def remove_file(folder: model.Folder, file_name, from_meta=True):
    folder.files = list(filter(lambda file: file.name != file_name, folder.files))
    if from_meta:
        folder.metadatafiles = list(filter(lambda file: file.name != file_name, folder.metadatafiles))


setattr(model.Folder, 'remove_file', remove_file)


def get_file(folder: model.Folder, file_name, from_meta=True):
    file = next(filter(lambda file: file.name == file_name, folder.files), None)
    if not file and from_meta:
        # search in metadatafiles
        file = next(filter(lambda file: file.name == file_name, folder.metadatafiles), None)
    return file


setattr(model.Folder, 'get_file', get_file)


def get_files(folder: model.Folder, name_pattern):
    return list(filter(lambda file: fnmatch.fnmatch(file.name, name_pattern), folder.files))


setattr(model.Folder, 'get_files', get_files)


def remove_folder(folder: model.Folder, folder_name):
    folder.folders = list(filter(lambda f: f.name != folder_name, folder.folders))


setattr(model.Folder, 'remove_folder', remove_folder)


def get_folder(folder: model.Folder, folder_name):
    return next(filter(lambda f: f.name == folder_name, folder.folders), None)


setattr(model.Folder, 'get_folder', get_folder)


def get_files_sorted(folder: model.Folder):
    return sorted(folder.files, key=lambda f: f.name)


setattr(model.Folder, 'get_files_sorted', get_files_sorted)


def get_folders_sorted(folder: model.Folder):
    return sorted(folder.folders, key=lambda f: f.name)


setattr(model.Folder, 'get_folders_sorted', get_folders_sorted)


def to_generator(source: model.Model, depth_first=False, filter_=None):
    if not depth_first:
        if filter_ and not filter_(source):
            return
        yield source

    for key, value in source.items():
        if isinstance(value, model.Model):
            yield from to_generator(value, depth_first, filter_)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, model.Model):
                    yield from to_generator(item, depth_first, filter_)

    if depth_first:
        if filter_ and not filter_(source):
            return
        yield source


setattr(model.Model, 'to_generator', to_generator)


def to_etree(source: dict, parent=None, name=None, id2x=None, x2id=None, nsmap_=None):
    if not name:
        name = type(source).__name__
    if parent is None:
        parent = etree.Element(name, nsmap=nsmap_)

    if isinstance(source, model.Model):
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


setattr(model.Model, 'to_etree', to_etree)


def to_dict(source: model.Model):
    return source


setattr(model.Model, 'to_dict', to_dict)


def query(ds: model.Dataset, expr: str):
    query = XPathQuery(ds, ds._schema)
    return query.execute(expr), query


setattr(model.Dataset, 'query', query)


def select(context: model.Model, target_type):
    return Select(context, target_type)


setattr(model.Dataset, 'select', select)


def validate(target: model.Model, report: ValidationReport):
    gen = to_generator(target)
    for obj in gen:
        members = utils.get_members(type(obj))
        for member in members:
            typ = member['type']
            name = member['name']
            lb = member['min']
            ub = member['max']
            val = getattr(obj, name)
            use = member['use']
            if (lb > 0 or use == 'required') and not val:
                report.error(f"Missing required field {name}.")
            if use == 'recommended' and not val:
                report.warn(f"Missing recommended field {name}.")


setattr(model.Model, 'validate', validate)

# end monkey-patching


from .pybids_compat import BIDSLayout

select = Select
any_of = AnyExpr
all_of = AllExpr
eq = EqExpr
re = ReExpr
op = CustomOpExpr
entity = EntityExpr

from . import _version

__version__ = _version.get_versions()['version']
