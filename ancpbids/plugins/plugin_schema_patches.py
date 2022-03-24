import fnmatch
import inspect
import os
from difflib import SequenceMatcher

from ancpbids.plugin import SchemaPlugin


def has_entity(artifact, entity_):
    for e in artifact.entities:
        if e.key == entity_:
            return True
    return False


def get_entity(artifact, entity_):
    for e in artifact.entities:
        if e.key == entity_:
            return e.value
    return None


def add_entity(artifact, key, value):
    schema = artifact.get_schema()
    if isinstance(key, schema.EntityEnum):
        key = key.entity_
    eref = schema.EntityRef(key, value)
    artifact.entities.append(eref)


def load_file_contents(folder, file_name):
    from ancpbids import utils
    file_path = get_absolute_path(folder, file_name)
    contents = utils.load_contents(file_path)
    return contents


def load_contents(file):
    from ancpbids import utils
    file_path = get_absolute_path(file.parent_object_, file.name)
    contents = utils.load_contents(file_path)
    return contents


def get_absolute_path_by_file(file):
    return get_absolute_path(file.parent_object_, file.name)


def get_absolute_path(folder, file_name=None):
    return _get_path(folder, file_name, True)


def _folder_get_relative_path(folder):
    return _get_path(folder, None, False)


def _file_get_relative_path(file):
    return _get_path(file.parent_object_, file.name, False)


def _get_path(folder, file_name=None, absolute=True):
    schema = folder.get_schema()
    segments = []
    if file_name:
        segments.append(file_name)
    current_folder = folder
    while current_folder is not None:
        if isinstance(current_folder, schema.Dataset):
            if absolute:
                segments.insert(0, current_folder.base_dir_)
            # assume we reached the highest level, maybe not good for nested datasets
            break
        else:
            segments.insert(0, current_folder.name)
        current_folder = current_folder.parent_object_
    _path = os.path.join(*segments) if segments else ''
    return os.path.normpath(_path)


def remove_file(folder, file_name, from_meta=True):
    folder.files = list(filter(lambda file: file.name != file_name, folder.files))
    if from_meta:
        folder.metadatafiles = list(filter(lambda file: file.name != file_name, folder.metadatafiles))


def create_artifact(folder):
    schema = folder.get_schema()
    artifact = schema.Artifact()
    artifact.parent_object_ = folder
    folder.files.append(artifact)
    return artifact


def create_folder(folder, type_=None, **kwargs):
    if not type_:
        type_ = folder.get_schema().Folder
    sub_folder = type_(**kwargs)
    sub_folder.parent_object_ = folder
    folder.folders.append(sub_folder)
    return sub_folder


def create_derivative(ds, **kwargs):
    schema = ds.get_schema()
    derivatives_folder = ds.derivatives
    if not ds.derivatives:
        derivatives_folder = schema.DerivativeFolder()
        derivatives_folder.parent_object_ = ds
        derivatives_folder.name = "derivatives"
        ds.derivatives = derivatives_folder
    derivative = schema.DerivativeFolder(**kwargs)
    derivative.parent_object_ = derivatives_folder
    derivatives_folder.folders.append(derivative)

    derivative.dataset_description = schema.DerivativeDatasetDescriptionFile()
    derivative.dataset_description.parent_object_ = derivative
    derivative.dataset_description.GeneratedBy = schema.GeneratedBy()

    if ds.dataset_description:
        derivative.dataset_description.update(ds.dataset_description)

    return derivative


def get_file(folder, file_name, from_meta=True):
    file = next(filter(lambda file: file.name == file_name, folder.files), None)
    if not file and from_meta:
        # search in metadatafiles
        file = next(filter(lambda file: file.name == file_name, folder.metadatafiles), None)
    return file


def get_files(folder, name_pattern):
    return list(filter(lambda file: fnmatch.fnmatch(file.name, name_pattern), folder.files))


def remove_folder(folder, folder_name):
    folder.folders = list(filter(lambda f: f.name != folder_name, folder.folders))


def get_folder(folder, folder_name):
    return next(filter(lambda f: f.name == folder_name, folder.folders), None)


def get_files_sorted(folder):
    return sorted(folder.files, key=lambda f: f.name)


def get_folders_sorted(folder):
    return sorted(folder.folders, key=lambda f: f.name)


def to_generator(source, depth_first=False, filter_=None):
    schema = source.get_schema()
    if not depth_first:
        if filter_ and not filter_(source):
            return
        yield source

    for key, value in source.items():
        if isinstance(value, schema.Model):
            yield from to_generator(value, depth_first, filter_)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, schema.Model):
                    yield from to_generator(item, depth_first, filter_)

    if depth_first:
        if filter_ and not filter_(source):
            return
        yield source


def iterancestors(source):
    context = source
    while context is not None:
        if not hasattr(context, 'parent_object_'):
            break
        context = context.parent_object_
        yield context


def to_dict(source):
    return source


def get_model_classes(schema):
    if not hasattr(schema, '_CLASSES'):
        schema._CLASSES = {name: obj for name, obj in inspect.getmembers(schema) if inspect.isclass(obj)}
    return schema._CLASSES


def _get_element_members(schema, element_type):
    element_members = []
    try:
        members = element_type.MEMBERS
        element_members = list(
            map(lambda item: {'name': item[0], **item[1], 'type': _to_type(schema, item[1]['type'])},
                members.items()))
    except AttributeError as ae:
        pass
    return element_members


def get_members(schema, element_type, include_superclass=True):
    if element_type == schema.Model:
        return []
    super_members = []

    if include_superclass:
        superclass = element_type
        while True:
            try:
                superclass = inspect.getmro(superclass)[1]
                if not superclass or superclass == schema.Model:
                    break
                super_members = super_members + _get_element_members(schema, superclass)
            except AttributeError:
                pass

    element_members = _get_element_members(schema, element_type)
    return super_members + element_members


def _to_type(schema, model_type_name: str):
    classes = schema.get_model_classes()
    if model_type_name in classes:
        return classes[model_type_name]
    if model_type_name in __builtins__:
        return __builtins__[model_type_name]
    return model_type_name


def _trim_int(value):
    try:
        # remove paddings/fillers in index values: 001 -> 1, 000230 -> 230
        return str(int(value))
    except ValueError:
        return value


def process_entity_value(schema, key, value):
    if not value:
        return value
    for sc_entity in filter(lambda e: e.literal_ == key, schema.EntityEnum.__members__.values()):
        if sc_entity.format_ == 'index':
            if isinstance(value, list):
                return list(map(lambda v: _trim_int(v), value))
            else:
                return _trim_int(value)
    return value


def fuzzy_match_entity_key(schema, user_key):
    return fuzzy_match_entity(schema, user_key).entity_


def fuzzy_match_entity(schema, user_key):
    ratios = list(
        map(lambda item: (
            item,
            1.0 if item.literal_.startswith(user_key) else SequenceMatcher(None, user_key,
                                                                           item.literal_).quick_ratio()),
            list(schema.EntityEnum)))
    ratios = sorted(ratios, key=lambda t: t[1])
    return ratios[-1][0]


class PatchingSchemaPlugin(SchemaPlugin):
    def execute(self, schema):
        schema.Artifact.has_entity = has_entity
        schema.Artifact.get_entity = get_entity
        schema.Artifact.add_entity = add_entity
        schema.Folder.load_file_contents = load_file_contents
        schema.File.load_contents = load_contents
        schema.File.get_absolute_path = get_absolute_path_by_file
        schema.Folder.get_relative_path = _folder_get_relative_path
        schema.Folder.get_absolute_path = get_absolute_path
        schema.File.get_relative_path = _file_get_relative_path
        schema.Folder.remove_file = remove_file
        schema.Folder.create_artifact = create_artifact
        schema.Folder.create_folder = create_folder
        schema.Dataset.create_derivative = create_derivative
        schema.Folder.get_file = get_file
        schema.Folder.get_files = get_files
        schema.Folder.remove_folder = remove_folder
        schema.Folder.get_folder = get_folder
        schema.Folder.get_files_sorted = get_files_sorted
        schema.Folder.get_folders_sorted = get_folders_sorted
        schema.Model.to_generator = to_generator
        schema.Model.to_dict = to_dict
        schema.Model.iterancestors = iterancestors

        schema.get_model_classes = lambda: get_model_classes(schema)
        schema.get_members = lambda element_type, include_superclass=True: get_members(schema, element_type,
                                                                                       include_superclass)
        schema.process_entity_value = lambda key, value: process_entity_value(schema, key, value)
        schema.fuzzy_match_entity_key = lambda user_key: fuzzy_match_entity_key(schema, user_key)
        schema.fuzzy_match_entity = lambda user_key: fuzzy_match_entity(schema, user_key)
