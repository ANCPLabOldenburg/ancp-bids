import inspect
import os
import shutil

from ancpbids import model
from ancpbids.schema import Schema


class DatasetSaver:
    def __init__(self, schema: Schema):
        pass

    def save(self, ds: model.Dataset, target_dir: str):
        if os.path.exists(target_dir) and len(os.listdir(target_dir)) > 0:
            raise ValueError("Directory not empty: " + target_dir)
        src_dir = ds.base_dir_
        generator = ds.generateRecursively_()
        for obj, _ in generator:
            typ = type(obj)
            mapper_name = '_type_handler_' + typ.__name__
            if mapper_name not in _TYPE_MAPPERS:
                mapper_name = '_type_handler_default'
            mapper = _TYPE_MAPPERS[mapper_name]
            mapper(self, src_dir, target_dir, obj)
        # copy internal children (files/folders)
        self._type_handler_Folder(src_dir, target_dir, ds, traverse_children=True)
        return target_dir

    def _type_handler_default(self, src_dir, target_dir, obj):
        if isinstance(obj, model.Folder):
            self._type_handler_Folder(src_dir, target_dir, obj)
        elif isinstance(obj, model.File):
            self._type_handler_File(src_dir, target_dir, obj)

    def _type_handler_File(self, src_dir, target_dir, file: model.File, new_file_name=None):
        old_file_name = file.get_relative_path()
        old_file_path = os.path.join(src_dir, old_file_name)
        new_file_path = new_file_name
        if new_file_path:
            new_file_path = os.path.join(target_dir, file.parent_object_.get_relative_path(), new_file_path)
        else:
            new_file_path = os.path.join(target_dir, old_file_name)
        shutil.copy(old_file_path, new_file_path)

    def _type_handler_Folder(self, src_dir, target_dir, folder: model.Folder, traverse_children=False):
        new_dir = os.path.join(target_dir, folder.get_relative_path())
        # the new directory may exist because model Artifacts/Folders are processed first
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)

        if traverse_children:
            for child_folder in folder.folders:
                self._type_handler_Folder(src_dir, target_dir, child_folder)
            for child_file in folder.files:
                self._type_handler_File(src_dir, target_dir, child_file)

    def _type_handler_Artifact(self, src_dir, target_dir, artifact: model.Artifact):
        segments = []
        # TODO sort according order defined in schema
        for e in artifact.get_entities():
            seg = '-'.join([e.get_key(), e.get_value()])
            segments.append(seg)
        segments.append(artifact.get_suffix())
        new_file_name = '_'.join(segments) + artifact.get_extension()
        self._type_handler_File(src_dir, target_dir, artifact, new_file_name)


_TYPE_MAPPERS = {name: obj for name, obj in inspect.getmembers(DatasetSaver) if
                 inspect.isfunction(obj) and obj.__name__.startswith('_type_handler_')}
