import inspect
import json
import os

import ancpbids
from ancpbids.plugin import WritingPlugin


class DatasetWritingPlugin(WritingPlugin):
    def execute(self, ds, target_dir: str, context_folder=None, src_dir: str = None):
        if context_folder is None and os.path.exists(target_dir) and len(os.listdir(target_dir)) > 0:
            raise ValueError("Directory not empty: " + target_dir)

        if context_folder is None:
            context_folder = ds
        if src_dir is None:
            src_dir = ds.get_absolute_path()

        self.schema = ds.get_schema()
        generator = context_folder.to_generator()
        for obj in generator:
            typ = type(obj)
            mapper_name = '_type_handler_' + typ.__name__
            if mapper_name not in _TYPE_MAPPERS:
                mapper_name = '_type_handler_default'
            mapper = _TYPE_MAPPERS[mapper_name]
            mapper(self, src_dir, target_dir, obj)
        # copy internal children (files/folders)
        self._type_handler_Folder(src_dir, target_dir, context_folder, traverse_children=True)

    def _type_handler_default(self, src_dir, target_dir, obj):
        if isinstance(obj, self.schema.Folder):
            self._type_handler_Folder(src_dir, target_dir, obj)
        elif isinstance(obj, self.schema.File):
            self._type_handler_File(src_dir, target_dir, obj)

    def _type_handler_File(self, src_dir, target_dir, file, new_file_name=None):
        if hasattr(file, 'content') and callable(file.content):
            file.content(file.get_absolute_path())
        else:
            ancpbids.utils.write_contents(file.get_absolute_path(), file)


    def _type_handler_Folder(self, src_dir, target_dir, folder, traverse_children=False):
        new_dir = os.path.join(target_dir, folder.get_relative_path())
        # the new directory may exist because model Artifacts/Folders are processed first
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)

        if traverse_children:
            for child_folder in folder.folders:
                self._type_handler_Folder(src_dir, target_dir, child_folder)
            for child_file in folder.files:
                self._type_handler_File(src_dir, target_dir, child_file)

    def _get_ordered_entity_keys(self, artifact):
        schema = artifact.get_schema()
        entity_refs = artifact.entities

        schema_entities = list(map(lambda e: e.entity_, list(schema.EntityEnum)))
        expected_key_order = {k: i for i, k in enumerate(schema_entities)}
        expected_order_key = {i: k for i, k in enumerate(schema_entities)}

        artifact_keys = list(map(lambda e: e.key, entity_refs))
        actual_keys_order = list(map(lambda k: expected_key_order[k], artifact_keys))
        expected = tuple(map(lambda k: expected_order_key[k], sorted(actual_keys_order)))
        return expected

    def _type_handler_Artifact(self, src_dir, target_dir, artifact):
        segments = []
        schema = artifact.get_schema()
        # add missing entities
        for ancestor in artifact.iterancestors():
            if isinstance(ancestor, schema.Folder):
                name = ancestor.name
                if name.startswith("ses-"):
                    artifact.add_entity('ses', name[4:])
                if name.startswith("sub-"):
                    artifact.add_entity('sub', name[4:])

        # sort according order defined in schema
        ordered_keys = self._get_ordered_entity_keys(artifact)
        for ok in ordered_keys:
            seg = '-'.join([ok, artifact.get_entity(ok)])
            segments.append(seg)
        segments.append(artifact.suffix)
        new_file_name = '_'.join(segments) + artifact.extension
        artifact.name = new_file_name
        self._type_handler_File(src_dir, target_dir, artifact, new_file_name)


_TYPE_MAPPERS = {name: obj for name, obj in inspect.getmembers(DatasetWritingPlugin) if
                 inspect.isfunction(obj) and obj.__name__.startswith('_type_handler_')}
