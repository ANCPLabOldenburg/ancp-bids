import inspect
import os

from ancpbids import model
from ancpbids.plugin import WritingPlugin


class DatasetWritingPlugin(WritingPlugin):
    def execute(self, ds: model.Dataset, target_dir: str, context_folder: model.Folder = None, src_dir: str = None):
        if context_folder is None and os.path.exists(target_dir) and len(os.listdir(target_dir)) > 0:
            raise ValueError("Directory not empty: " + target_dir)

        if context_folder is None:
            context_folder = ds
        if src_dir is None:
            src_dir = ds.get_absolute_path()

        self.schema = ds._schema
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

        if hasattr(file, 'content') and callable(file.content):
            file.content(file.get_absolute_path())
        else:
            # TODO process fields
            pass

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
        for e in artifact.entities:
            seg = '-'.join([e.key, e.value])
            segments.append(seg)
        segments.append(artifact.suffix)
        new_file_name = '_'.join(segments) + artifact.extension
        artifact.name = new_file_name
        self._type_handler_File(src_dir, target_dir, artifact, new_file_name)


_TYPE_MAPPERS = {name: obj for name, obj in inspect.getmembers(DatasetWritingPlugin) if
                 inspect.isfunction(obj) and obj.__name__.startswith('_type_handler_')}
