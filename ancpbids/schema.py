import logging
import os
import inspect
import sys

import regex

from . import model
from . import files

logger = logging.getLogger(__file__)

SCHEMA_PATH = os.path.dirname(__file__) + '/data/schema-files'
ENTITIES_PATTERN = regex.compile(r'(([^\W_]+)-([^\W_]+)_)+([^\W_]+)(.*)')

NS = 'https://bids.neuroimaging.io/1.6'
NS_PREFIX = 'bids'
NS_MAP = {NS_PREFIX: NS}


class Schema:
    def __init__(self):
        self.modalities = files.load_contents(SCHEMA_PATH + "/modalities.yaml")
        self.entities = files.load_contents(SCHEMA_PATH + "/entities.yaml")
        # convert to dictionary for faster lookup by entity keys
        self.entities = {e['key']: e for e in self.entities}
        self.datatypes = self.merge_to_dict(SCHEMA_PATH + "/datatypes")

    def merge_to_dict(self, dir_path):
        result = {}
        for file in files.get_files(dir_path, include_folders=False, fnmatch_pattern="*.yaml"):
            name_wo_ext = os.path.basename(file)[:-5]
            result[name_wo_ext] = files.load_contents(file)
        return result

    def load_dataset(self, base_dir):
        ds = model.Dataset()
        ds.set_ns_prefix_(NS_PREFIX)
        ds._schema = self
        ds.set_name(os.path.basename(base_dir))
        ds.set_base(base_dir)
        # 1. pass: load file system structure
        _load_folder(ds, base_dir)
        # 3. pass: check if any remaining files can be transformed to artifacts
        self._convert_files_to_artifacts(ds)
        # 2. pass: expand structure based on schema-files
        _expand_members(ds)
        return ds

    def _convert_files_to_artifacts(self, parent: model.Folder):
        for i, file in enumerate(parent.files):
            artifact = self._convert_to_artifact(file)
            if not artifact:
                continue
            artifact.parent_object_ = parent
            parent.replace_files_at(i, artifact)
        for folder in parent.folders:
            self._convert_files_to_artifacts(folder)

    def _convert_to_artifact(self, file: model.File):
        match = ENTITIES_PATTERN.match(file.name)
        if not match:
            return None
        artifact = model.Artifact()
        artifact.name = file.name
        for pair in zip(match.captures(2), match.captures(3)):
            entity = model.EntityRef()
            key = pair[0]
            entity.set_key(key)
            value = self.process_entity_value(key, pair[1])
            entity.set_value(value)
            artifact.add_entities(entity)
        artifact.set_suffix(match[4])
        artifact.set_extension(match[5])
        return artifact

    def process_entity_value(self, key, value):
        sc_entity = self.entities[key]
        # remove paddings/fillers in index values
        if value and sc_entity and 'format' in sc_entity and sc_entity['format'] == 'index':
            if isinstance(value, list):
                return list(map(lambda v: str(int(v)), value))
            else:
                return str(int(value))
        return value


def _to_type(model_type_name: str):
    if model_type_name == 'string':
        return str
    return _MODEL_CLASSES[model_type_name]


def _normalize(member):
    result = {'name': member['name'], 'typ': _to_type(member['type'])}
    if 'use' in member:
        result['lower'] = 1 if member['use'] == 'required' else 0
        result['upper'] = 1
    else:
        result['lower'] = member['minOccurs']
        result['upper'] = member['maxOccurs']
    return result


def _get_members(element_type, include_superclass=True):
    if element_type == model.File or element_type == model.Folder:
        return []
    super_members = []

    if include_superclass:
        try:
            if element_type.superclass:
                super_members = _get_members(element_type.superclass, include_superclass)
        except AttributeError:
            pass

    element_members = []
    try:
        element_members = list(map(lambda member: {'name': member.name, 'type': member.data_type, **member.child_attrs},
                                   element_type.member_data_items_.values()))
        element_members = list(map(_normalize, element_members))
    except AttributeError as ae:
        pass
    return super_members + element_members


def _type_handler_DatasetDescriptionFile(parent, member):
    file_name = member['name'] + '.json'
    _extract_fields_from_jsonfile(parent, member, file_name, model.DatasetDescriptionFile)


def _extract_fields_from_jsonfile(parent, member, file_name, model_type):
    json_object = parent.load_file_contents(file_name)
    if not json_object:
        return

    dsd_file = model_type()
    members = _get_members(model_type, False)
    actual_props = json_object.keys()
    direct_props = list(map(lambda m: m['name'], members))
    for prop_name in direct_props:
        if prop_name in actual_props:
            value = json_object[prop_name]
            setattr(dsd_file, prop_name, value)
    setattr(parent, member['name'], dsd_file)
    parent.remove_file(file_name)


def _type_handler_File(parent, member):
    if not isinstance(parent, model.Folder):
        return
    name = member['name']
    file = parent.get_file(name)
    if file:
        setattr(parent, name, file)
        parent.remove_file(name)


def _type_handler_Artifact(parent, member):
    if not isinstance(parent, model.Folder):
        return
    name = member['name']
    attr = getattr(parent, name)
    multi = isinstance(attr, list)
    files = parent.get_files() if multi else list(filter(lambda f: f.name == name, parent.get_files()))
    for file in files:
        if not isinstance(file, model.Artifact):
            continue
        file.parent_object_ = parent
        parent.remove_file(file.name)
        if multi:
            attr.append(file)
        else:
            setattr(parent, name, file)


def _type_handler_Folder(parent, member):
    if not isinstance(parent, model.Folder):
        return
    name = member['name']
    folder = parent.get_folder(name)
    if folder:
        setattr(parent, name, folder)
        parent.remove_folder(name)


def _type_handler_Subject(parent, member):
    _handle_direct_folders(parent, member, "sub-", model.Subject)


def _type_handler_Session(parent, member):
    _handle_direct_folders(parent, member, "ses-", model.Session)


def _type_handler_DatatypeFolder(parent, member):
    bids_schema = _get_schema(parent)
    pattern = '|'.join(bids_schema.datatypes.keys())
    _handle_direct_folders(parent, member, pattern, model.DatatypeFolder)


def _get_schema(context):
    current = context
    while current is not None:
        if isinstance(current, model.Dataset):
            return current._schema
        current = current.parent_object_
    return None


def _handle_direct_folders(parent, member, pattern, new_type):
    if not isinstance(parent, model.Folder):
        return
    folders = list(filter(lambda f: regex.match(pattern, f.name), parent.get_folders_sorted()))
    for folder in folders:
        obj = new_type()
        obj.name = folder.name
        obj.files = folder.files
        obj.folders = folder.folders
        parent.remove_folder(folder.name)
        obj.parent_object_ = parent
        getattr(parent, member['name']).append(obj)
        _expand_members(obj)


def _expand_member(parent, member):
    typ = member['typ']
    mapper_name = '_type_handler_' + typ.__name__
    if mapper_name not in _TYPE_MAPPERS:
        return
    mapper = _TYPE_MAPPERS[mapper_name]
    mapper(parent, member)


def _expand_members(folder: model.Folder):
    members = _get_members(type(folder))
    for member in members:
        _expand_member(folder, member)


def _load_folder(parent: model.Folder, dir_path):
    for root, directories, files in os.walk(dir_path):
        for directory in sorted(directories):
            folder = model.Folder(parent_object_=parent)
            folder.set_name(directory)
            parent.add_folders(folder)
            _load_folder(folder, root + "/" + directory)
        for file in sorted(files):
            model_file = model.File(parent_object_=parent)
            model_file.set_name(file)
            parent.add_files(model_file)
        break


_MODEL_CLASSES = {name: obj for name, obj in inspect.getmembers(model) if inspect.isclass(obj)}
_TYPE_MAPPERS = {name: obj for name, obj in inspect.getmembers(sys.modules[__name__]) if
                 inspect.isfunction(obj) and obj.__name__.startswith('_type_handler_')}
