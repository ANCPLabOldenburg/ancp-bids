import fnmatch
import inspect
import os
import re

from .plugin_files_handlers import read_plain_text
from .. import utils
from ..plugin import DatasetPlugin
from ..model_base import *

class DatasetPopulationPlugin(DatasetPlugin):

    def execute(self, dataset, schema):
        base_dir = str(dataset.base_dir_)
        self.schema = schema
        self.options = dataset.options
        self._load_bidsignore(base_dir)

        # load file system structure
        self._load_folder(dataset, base_dir, base_dir)
        # transform files to artifacts, i.e. files containing entities in their name
        self._convert_files_to_artifacts(dataset)

        # handle special files
        self._handle_metadata_files(dataset)
        self._handle_tsv_files(dataset)

        # expand structure based on schema-files
        self._expand_members(dataset)
        # convert Folders within derivatives to DerivativeFolder
        self._convert_derivatives_folders(dataset.derivatives)

        # do optional stuff
        self._determine_artifact_datatype(dataset)

    def _determine_artifact_datatype(self, dataset):
        if not self.options.infer_artifact_datatype:
            return
        datatype_folders = dataset.select(DatatypeFolder).objects()
        for folder in datatype_folders:
            artifacts = folder.select(Artifact).objects()
            for artifact in artifacts:
                artifact.datatype = folder.name

    def _load_bidsignore(self, base_dir):
        self.bidsignore = lambda relative_path: False
        if self.options.ignore:
            patterns = []
            if isinstance(self.options.ignore, bool):
                bidsignore_file = os.path.join(base_dir, ".bidsignore")
                if os.path.exists(bidsignore_file):
                    patterns = read_plain_text(bidsignore_file)
            elif isinstance(self.options.ignore, list):
                patterns = self.options.ignore

            if patterns:
                patterns = list(map(lambda pattern: pattern.strip(), patterns))
                # TODO cleanup invalid filter such as empty lines or comments
                self.bidsignore = lambda relative_path: next(
                    filter(lambda pattern: fnmatch.fnmatch(relative_path, pattern), patterns), False)

    def _handle_metadata_files(self, folder):
        if not isinstance(folder, Folder):
            return
        for file in filter(lambda f: f.name.endswith(".json"), folder.files):
            if isinstance(file, Artifact):
                mdfile = MetadataArtifact()
            else:
                mdfile = MetadataFile()
            mdfile.parent_object_ = folder
            mdfile.update(file)
            mdfile.contents = mdfile.load_contents()
            folder.files.remove(file)
            folder.files.append(mdfile)

        for child in folder.folders:
            self._handle_metadata_files(child)

    def _handle_tsv_files(self, folder):
        if not isinstance(folder, Folder):
            return
        for file in filter(lambda f: f.name.endswith(".tsv"), folder.files):
            if isinstance(file, Artifact):
                newfile = TSVArtifact()
            else:
                newfile = TSVFile()
            newfile.parent_object_ = folder
            newfile.update(file)
            newfile.contents = newfile.load_contents()
            folder.files.remove(file)
            folder.files.append(newfile)

        for child in folder.folders:
            self._handle_tsv_files(child)

    def _convert_derivatives_folders(self, parent):
        if not parent:
            return
        for i, folder in enumerate(list(parent.folders)):
            dfolder = DerivativeFolder()
            dfolder.parent_object_ = parent
            dfolder.update(folder)
            parent.folders[i] = dfolder
            self._convert_derivatives_folders(dfolder)
            self._expand_members(dfolder)

    def _convert_files_to_artifacts(self, parent):
        for i, file in enumerate(parent.files):
            artifact = self._convert_to_artifact(file)
            if not artifact:
                continue
            artifact.parent_object_ = parent
            parent.files[i] = artifact
        for folder in parent.folders:
            self._convert_files_to_artifacts(folder)

    def _convert_to_artifact(self, file):
        parts = utils.parse_bids_name(file.name)
        if not parts:
            return None
        artifact = Artifact()
        artifact.name = file.name
        for key, value in parts['entities'].items():
            entity = EntityRef()
            entity.key = key
            value = self.schema.process_entity_value(key, value)
            entity.value = value
            artifact.entities.append(entity)
        artifact.suffix = parts['suffix']
        artifact.extension = parts['extension']
        return artifact

    def _handle_direct_folders(self, parent, member, pattern, new_type):
        if not isinstance(parent, Folder):
            return
        parent_folders = parent.get_folders_sorted()
        folders = list(filter(lambda f: re.match(pattern, f.name), parent_folders))
        for folder in folders:
            obj = new_type()
            obj.name = folder.name
            obj.files = folder.files
            for ofile in obj.files:
                ofile.parent_object_ = obj
            obj.folders = folder.folders
            for ofolder in obj.folders:
                ofolder.parent_object_ = obj
            parent.remove_folder(folder.name)
            obj.parent_object_ = parent
            if member['max'] > 1:
                getattr(parent, member['name']).append(obj)
            else:
                setattr(parent, member['name'], obj)
            self._expand_members(obj)

    def _expand_member(self, parent, member):
        typ = member['type']
        if not issubclass(typ, Model):
            return
        mapper_name = '_type_handler_%s' % typ.__name__
        if mapper_name not in _TYPE_MAPPERS:
            mapper_name = '_type_handler_default'
        mapper = _TYPE_MAPPERS[mapper_name]
        mapper(self, parent, member)

    def _expand_members(self, folder):
        members = self.schema.get_members(type(folder))
        for member in members:
            self._expand_member(folder, member)

    def _load_folder(self, parent, dir_path, ds_path):
        for root, directories, files in os.walk(dir_path):
            rel_base = root[len(ds_path):]
            for directory in sorted(directories):
                directory_ds_rel_path = '/'.join([rel_base, directory])[1:]
                if self.bidsignore(directory_ds_rel_path):
                    continue
                folder = Folder()
                folder.parent_object_ = parent
                folder.name = directory
                parent.folders.append(folder)
                self._load_folder(folder, '/'.join([root, directory]), ds_path)
            for file in sorted(files):
                file_ds_rel_path = '/'.join([rel_base, file])[1:]
                if self.bidsignore(file_ds_rel_path):
                    continue
                model_file = File()
                model_file.parent_object_ = parent
                model_file.name = file
                parent.files.append(model_file)
            # do not traverse into sub-dirs as they have been already processed recursively
            break

    def _type_handler_default(self, parent, member):
        typ = member['type']
        if issubclass(typ, JsonFile):
            self._type_handler_JsonFile(parent, member, True)
        elif issubclass(typ, Folder):
            pattern = '.*'
            meta = member['meta']
            if 'name_pattern' in meta:
                pattern = meta['name_pattern']
            self._handle_direct_folders(parent, member, pattern=pattern, new_type=typ)

    def _type_handler_File(self, parent, member):
        if not isinstance(parent, Folder):
            return
        file_name = member['name']
        meta = member['meta']
        if 'name_pattern' in meta:
            file_name = meta['name_pattern']
        file = parent.get_file(file_name)
        if file:
            setattr(parent, member['name'], file)
            parent.remove_file(file.name)

    def _type_handler_Artifact(self, parent, member):
        if not isinstance(parent, Folder):
            return
        attr = getattr(parent, member['name'])
        multi = isinstance(attr, list)
        name = member['name']
        files = parent.files if multi else list(filter(lambda f: f.name == name, parent.files))
        for file in files:
            if not isinstance(file, Artifact):
                continue
            file.parent_object_ = parent
            parent.remove_file(file.name)
            if multi:
                attr.append(file)
            else:
                setattr(parent, member['name'], file)

    def _type_handler_Folder(self, parent, member):
        if not isinstance(parent, Folder):
            return
        name = member['name']
        folder = parent.get_folder(name)
        if folder:
            setattr(parent, name, folder)
            parent.remove_folder(name)

    def _map_object(self, model_type, json_object):
        target = model_type()
        members = self.schema.get_members(model_type, True)
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
