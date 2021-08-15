import logging
import os
import inspect
import sys
from collections import OrderedDict

import regex

import bids.files as files
import bids.model as model

logger = logging.getLogger(__file__)

SCHEMA_PATH = os.path.dirname(__file__) + '/../schema'
ENTITIES_PATTERN = regex.compile(r'(([^\W_]+)-([^\W_]+)_)+([^\W_]+)(.*)')

NS = 'https://bids.neuroimaging.io/1.7.0'
NS_PREFIX = 'bids'
NS_MAP = {NS_PREFIX: NS}


class Schema:
    def __init__(self):
        self.modalities = files.load_contents(SCHEMA_PATH + "/modalities.yaml")
        self.entities = files.load_contents(SCHEMA_PATH + "/entities.yaml")
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
        _load_folder(ds, base_dir)
        _expand_members(ds)
        return ds


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


def _dict_to_JsonObject(data: dict):
    if not data:
        return None
    result = model.JsonObject()
    for k, v in data.items():
        prop = model.Property()
        prop.set_key(k)
        if isinstance(v, dict):
            obj = _dict_to_JsonObject(v)
            prop.set_value_obj(obj)
        elif isinstance(v, list):
            prop.set_value_multi(v)
        else:
            prop.set_value_single(v)
        result.add_properties(prop)
    return result


def _to_JsonObject(parent: model.Folder, file: str):
    if not isinstance(parent, model.Folder):
        return None
    json_contents = parent.load_file_contents(file)
    json_object = _dict_to_JsonObject(json_contents)
    if json_object:
        json_object.set_name(file)
    return json_object


def _type_handler_DatasetDescriptionFile(parent, member):
    name = member['name']
    json_object = _to_JsonObject(parent, name + '.json')
    if json_object:
        dsd_file = model.DatasetDescriptionFile()
        members = _get_members(model.DatasetDescriptionFile, False)
        direct_props = list(map(lambda m: m['name'], members))
        for prop in json_object.get_properties():
            if prop.get_key() in direct_props:
                if prop.get_value_single():
                    setattr(dsd_file, prop.get_key(), prop.get_value_single())
                elif prop.get_value_multi():
                    setattr(dsd_file, prop.get_key(), prop.get_value_multi())
                else:
                    setattr(dsd_file, prop.get_key(), prop.get_value_obj())
            else:
                dsd_file.add_properties(prop)
        setattr(parent, name, dsd_file)
        parent.remove_file(json_object.name)


def _type_handler_JsonObject(parent, member):
    name = member['name']
    json_object = _to_JsonObject(parent, name + '.json')
    if json_object:
        setattr(parent, name, json_object)
        parent.remove_file(json_object.name)


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
    for file in parent.get_files_sorted():
        match = regex.match(ENTITIES_PATTERN, file.name)
        if not match:
            continue
        artifact = model.Artifact()
        artifact.name = file.name
        parent.remove_file(file.name)
        artifact.parent_object_ = parent
        getattr(parent, name).append(artifact)
        for pair in zip(match.captures(2), match.captures(3)):
            entity = model.EntityRef()
            entity.set_key(pair[0])
            entity.set_value(pair[1])
            artifact.add_entities(entity)
        artifact.set_suffix(match[4])
        artifact.set_extension(match[5])


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
        for directory in directories:
            folder = model.Folder()
            folder.set_name(directory)
            parent.add_folders(folder)
            _load_folder(folder, root + "/" + directory)
        for file in files:
            model_file = model.File()
            model_file.set_name(file)
            parent.add_files(model_file)
        break


_MODEL_CLASSES = {name: obj for name, obj in inspect.getmembers(model) if inspect.isclass(obj)}
_TYPE_MAPPERS = {name: obj for name, obj in inspect.getmembers(sys.modules[__name__]) if
                 inspect.isfunction(obj) and obj.__name__.startswith('_type_handler_')}
