import inspect
import os
import sys

import regex

from ancpbids import model
from ancpbids.schema import Schema, NS_PREFIX
from . import utils

ENTITIES_PATTERN = regex.compile(r'(([^\W_]+)-([^\W_]+)_)+([^\W_]+)(.*)')


class DatasetLoader:
    def __init__(self, schema: Schema):
        self.schema = schema

    def load(self, base_dir):
        ds = model.Dataset()
        ds.set_ns_prefix_(NS_PREFIX)
        ds._schema = self.schema
        ds.set_name(os.path.basename(base_dir))
        ds.set_base(base_dir)
        # 1. pass: load file system structure
        self._load_folder(ds, base_dir)
        # 2. pass: transform files to artifacts, i.e. files containing entities in their name
        self._convert_files_to_artifacts(ds)
        # 3. pass: expand structure based on schema-files
        self._expand_members(ds)
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

    def _trim_int(self, value):
        try:
            # remove paddings/fillers in index values: 001 -> 1, 000230 -> 230
            return str(int(value))
        except ValueError:
            return value

    def process_entity_value(self, key, value):
        if not value or key not in self.schema.entities:
            return value
        sc_entity = self.schema.entities[key]
        if value and sc_entity and 'format' in sc_entity and sc_entity['format'] == 'index':
            if isinstance(value, list):
                return list(map(lambda v: self._trim_int(v), value))
            else:
                return self._trim_int(value)
        return value

    def _get_schema(self, context):
        return self.schema

    def _handle_direct_folders(self, parent, member, pattern, new_type):
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
            self._expand_members(obj)

    def _expand_member(self, parent, member):
        typ = member['typ']
        mapper_name = '_type_handler_' + typ.__name__
        if mapper_name not in _TYPE_MAPPERS:
            mapper_name = '_type_handler_default'
        mapper = _TYPE_MAPPERS[mapper_name]
        mapper(self, parent, member)

    def _expand_members(self, folder: model.Folder):
        members = utils.get_members(type(folder))
        for member in members:
            self._expand_member(folder, member)

    def _load_folder(self, parent: model.Folder, dir_path):
        for root, directories, files in os.walk(dir_path):
            for directory in sorted(directories):
                folder = model.Folder(parent_object_=parent)
                folder.set_name(directory)
                parent.add_folders(folder)
                self._load_folder(folder, root + "/" + directory)
            for file in sorted(files):
                model_file = model.File(parent_object_=parent)
                model_file.set_name(file)
                parent.add_files(model_file)
            break

    def _type_handler_default(self, parent, member):
        typ = member['typ']
        if issubclass(typ, model.File):
            file_name = member['name_raw']
            _, ext = os.path.splitext(file_name)
            if ext and ext in FIELDS_EXTRACTORS:
                FIELDS_EXTRACTORS[ext](parent, member, file_name, typ)

    def _type_handler_File(self, parent, member):
        if not isinstance(parent, model.Folder):
            return
        name = member['name']
        file = parent.get_file(name)
        if file:
            setattr(parent, name, file)
            parent.remove_file(name)

    def _type_handler_Artifact(self, parent, member):
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

    def _type_handler_Folder(self, parent, member):
        if not isinstance(parent, model.Folder):
            return
        name = member['name']
        folder = parent.get_folder(name)
        if folder:
            setattr(parent, name, folder)
            parent.remove_folder(name)

    def _type_handler_Subject(self, parent, member):
        self._handle_direct_folders(parent, member, "sub-", model.Subject)

    def _type_handler_Session(self, parent, member):
        self._handle_direct_folders(parent, member, "ses-", model.Session)

    def _type_handler_DatatypeFolder(self, parent, member):
        pattern = '|'.join(self.schema.datatypes.keys())
        self._handle_direct_folders(parent, member, pattern, model.DatatypeFolder)


def _extract_fields_from_jsonfile(parent, member, file_name, model_type):
    json_object = parent.load_file_contents(file_name)
    if not json_object:
        return
    dsd_file = model_type()
    members = utils.get_members(model_type, False)
    actual_props = json_object.keys()
    direct_props = list(map(lambda m: m['name'], members))
    for prop_name in direct_props:
        if prop_name in actual_props:
            value = json_object[prop_name]
            setattr(dsd_file, prop_name, value)
    setattr(parent, member['name'], dsd_file)
    parent.remove_file(file_name)


FIELDS_EXTRACTORS = {
    '.json': _extract_fields_from_jsonfile
}

_TYPE_MAPPERS = {name: obj for name, obj in inspect.getmembers(DatasetLoader) if
                 inspect.isfunction(obj) and obj.__name__.startswith('_type_handler_')}
