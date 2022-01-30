from ..plugin import DatasetPlugin

import inspect
import os

import regex

from ancpbids import model
from ancpbids.schema import Schema
from .. import utils

ENTITIES_PATTERN = regex.compile(r'(([^\W_]+)-([^\W_]+)_)+([^\W_]+)(.*)')


class DatasetPopulationPlugin(DatasetPlugin):
    def execute(self, dataset: model.Dataset):
        self.schema = dataset._schema
        base_dir = dataset.base_dir_
        # 1. pass: load file system structure
        self._load_folder(dataset, base_dir)
        # 2. pass: transform files to artifacts, i.e. files containing entities in their name
        self._convert_files_to_artifacts(dataset)
        # 3. pass: expand structure based on schema-files
        self._expand_members(dataset)

    def _convert_files_to_artifacts(self, parent: model.Folder):
        for i, file in enumerate(parent.files):
            artifact = self._convert_to_artifact(file)
            if not artifact:
                continue
            artifact.parent_object_ = parent
            parent.files[i] = artifact
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
            entity.key = key
            value = self.schema.process_entity_value(key, pair[1])
            entity.value = value
            artifact.entities.append(entity)
        artifact.suffix = match[4]
        artifact.extension = match[5]
        return artifact

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
            if member['max'] > 1:
                getattr(parent, member['name']).append(obj)
            else:
                setattr(parent, member['name'], obj)
            self._expand_members(obj)

    def _expand_member(self, parent, member):
        typ = member['type']
        if not issubclass(typ, model.Model):
            return
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
                folder = model.Folder()
                folder.parent_object_ = parent
                folder.name = directory
                parent.folders.append(folder)
                self._load_folder(folder, root + "/" + directory)
            for file in sorted(files):
                model_file = model.File()
                model_file.parent_object_ = parent
                model_file.name = file
                parent.files.append(model_file)
            break

    def _type_handler_default(self, parent, member):
        typ = member['type']
        if issubclass(typ, model.JsonFile):
            self._type_handler_JsonFile(parent, member, True)
        elif issubclass(typ, model.Folder):
            pattern = '.*'
            meta = member['meta']
            if 'name_pattern' in meta:
                pattern = meta['name_pattern']
            self._handle_direct_folders(parent, member, pattern=pattern, new_type=typ)

    def _type_handler_File(self, parent, member):
        if not isinstance(parent, model.Folder):
            return
        file = parent.get_file(member['name'])
        if file:
            setattr(parent, member['name'], file)
            parent.remove_file(file.name)

    def _type_handler_MetadataFile(self, parent, member):
        if not isinstance(parent, model.Folder):
            return
        if member['max'] > 1:
            files = parent.get_files(member['meta']['name_pattern'])
            files = list(filter(lambda f: isinstance(f, model.Artifact), files))
            for file in files:
                mdfile = model.MetadataFile()
                mdfile.parent_object_ = parent
                mdfile.update(file)
                mdfile.contents = mdfile.load_contents()
                getattr(parent, member['name']).append(mdfile)
                parent.remove_file(file.name, from_meta=False)
        else:
            file = parent.get_file(member['name'])
            if isinstance(file, model.Artifact):
                mdfile = model.MetadataFile()
                mdfile.parent_object_ = parent
                mdfile.update(file)
                mdfile.contents = mdfile.load_contents()
                setattr(parent, member['name'], mdfile)
                parent.remove_file(file.name, from_meta=False)

    def _type_handler_Artifact(self, parent, member):
        if not isinstance(parent, model.Folder):
            return
        attr = getattr(parent, member['name'])
        multi = isinstance(attr, list)
        name = member['name']
        files = parent.files if multi else list(filter(lambda f: f.name == name, parent.files))
        for file in files:
            if not isinstance(file, model.Artifact):
                continue
            file.parent_object_ = parent
            parent.remove_file(file.name)
            if multi:
                attr.append(file)
            else:
                setattr(parent, member['name'], file)

    def _type_handler_Folder(self, parent, member):
        if not isinstance(parent, model.Folder):
            return
        name = member['name']
        folder = parent.get_folder(name)
        if folder:
            setattr(parent, name, folder)
            parent.remove_folder(name)

    def _map_object(self, model_type, json_object):
        target = model_type()
        members = utils.get_members(model_type, False)
        actual_props = json_object.keys()
        direct_props = list(map(lambda m: (m['name'], m), members))
        for prop_name, prop in direct_props:
            if prop_name in actual_props:
                value_type = prop['type']
                value = json_object[prop_name]
                if isinstance(value, list) and len(value) > 0:
                    value = list(map(lambda o: self._map_object(value_type, o) if isinstance(o, dict) else o, value))
                if isinstance(value, dict):
                    value = self._map_object(value_type, value)
                setattr(target, prop_name, value)
        return target

    def _type_handler_JsonFile(self, parent, member, is_subclass=False):
        name = member['name']
        file_name = name + '.json'
        file = parent.get_file(file_name)
        if not file:
            return
        json_object = file.contents if 'contents' in file else file.load_contents()
        if not json_object:
            return
        model_type = member['type']
        json_file = self._map_object(model_type, json_object)
        json_file.name = file_name
        json_file.contents = json_object
        setattr(parent, member['name'], json_file)
        parent.remove_file(file_name)
        json_file.parent_object_ = parent


_TYPE_MAPPERS = {name: obj for name, obj in inspect.getmembers(DatasetPopulationPlugin) if
                 inspect.isfunction(obj) and obj.__name__.startswith('_type_handler_')}
