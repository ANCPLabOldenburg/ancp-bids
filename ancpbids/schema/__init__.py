"""Vendored BIDS schema.json files and runtime Schema objects."""
import inspect
import json
from difflib import SequenceMatcher
from importlib import resources
from enum import Enum
from math import inf
from typing import Any, List, Type, TypeVar, get_args, get_origin

from .. import model_base

_PREFIX = "schema_v"
_SUFFIX = ".json"
_CACHE = {}


def _normalize_version(version: str) -> str:
    return version.lstrip("v")


def _filename(version: str) -> str:
    return f"{_PREFIX}{_normalize_version(version)}{_SUFFIX}"


def _read_text(filename: str) -> str:
    if hasattr(resources, "files"):
        return resources.files(__package__).joinpath(filename).read_text(encoding="utf-8")
    return resources.read_text(__package__, filename, encoding="utf-8")


def _resource_names():
    if hasattr(resources, "files"):
        return [p.name for p in resources.files(__package__).iterdir() if p.is_file()]
    return [
        name
        for name in resources.contents(__package__)
        if resources.is_resource(__package__, name)
    ]


def available_versions() -> List[str]:
    versions = [
        name[len(_PREFIX):-len(_SUFFIX)]
        for name in _resource_names()
        if name.startswith(_PREFIX) and name.endswith(_SUFFIX)
    ]
    return sorted(versions, key=lambda v: tuple(int(part) for part in v.split(".")))


def load_json(version: str) -> dict:
    """Load a vendored official schema.json as a dict."""
    filename = _filename(version)
    try:
        return json.loads(_read_text(filename))
    except (FileNotFoundError, OSError) as exc:
        raise FileNotFoundError(
            f"No vendored schema for version {version!r}. "
            f"Available: {', '.join(available_versions())}"
        ) from exc


_E = TypeVar("_E", bound=Enum)


def _make_enum(base: Type[_E], name: str, members: dict) -> Type[_E]:
    """Build a versioned enum from JSON, equivalent to::

        class DatatypeEnum(DatatypeEnum):
            anat = {'value': 'anat', ...}

    ``base`` is the empty Enum in model_base (no members, so it can be
    subclassed). ``base(name, members)`` is the functional Enum constructor:
    it creates a new subclass with those members. Each schema version gets
    its own class, so 1.8.0 and 1.11.1 do not share DatatypeEnum identity.
    """
    if not members:
        return base
    return base(name, members)


def _ordered_entities(document):
    """Keep entity members in BIDS filename order (rules.entities), not JSON key order."""
    unordered = document["objects"]["entities"]
    return {name: unordered[name] for name in document["rules"]["entities"]}


class Schema:
    """One BIDS schema version: shared graph types plus version-specific enums.

    Replaces the old generated ``model_v1_X_Y`` modules. Callers still use
    ``schema.Dataset``, ``schema.EntityEnum.subject``, ``schema.VERSION``.
    Graph classes (Dataset, Artifact, ...) are the same objects as in
    model_base; only the four enums differ per version.
    """

    VERSION: str
    document: dict
    SCHEMA: "Schema"

    Model = model_base.Model
    MetadataFieldDefinition = model_base.MetadataFieldDefinition
    EntitiyDefinition = model_base.EntitiyDefinition
    SuffixDefinition = model_base.SuffixDefinition
    File = model_base.File
    JsonFile = model_base.JsonFile
    Artifact = model_base.Artifact
    MetadataArtifact = model_base.MetadataArtifact
    MetadataFile = model_base.MetadataFile
    TSVArtifact = model_base.TSVArtifact
    TSVFile = model_base.TSVFile
    Folder = model_base.Folder
    EntityRef = model_base.EntityRef
    DatasetDescriptionFile = model_base.DatasetDescriptionFile
    DerivativeDatasetDescriptionFile = model_base.DerivativeDatasetDescriptionFile
    DerivativeFolder = model_base.DerivativeFolder
    SessionFolder = model_base.SessionFolder
    DatatypeFolder = model_base.DatatypeFolder
    Subject = model_base.Subject
    GeneratedBy = model_base.GeneratedBy
    SourceDatasets = model_base.SourceDatasets
    GeneratedByContainer = model_base.GeneratedByContainer
    Dataset = model_base.Dataset

    DatatypeEnum: Type[model_base.DatatypeEnum]
    ModalityEnum: Type[model_base.ModalityEnum]
    SuffixEnum: Type[model_base.SuffixEnum]
    EntityEnum: Type[model_base.EntityEnum]

    def __init__(self, version: str, document: dict):
        self.VERSION = document.get("bids_version") or version
        self.document = document
        self.SCHEMA = self
        objects = document["objects"]
        self.DatatypeEnum = _make_enum(
            model_base.DatatypeEnum, "DatatypeEnum", objects["datatypes"]
        )
        self.ModalityEnum = _make_enum(
            model_base.ModalityEnum, "ModalityEnum", objects["modalities"]
        )
        self.SuffixEnum = _make_enum(
            model_base.SuffixEnum, "SuffixEnum", objects["suffixes"]
        )
        self.EntityEnum = _make_enum(
            model_base.EntityEnum, "EntityEnum", _ordered_entities(document)
        )

    def __eq__(self, other):
        return isinstance(other, Schema) and self.VERSION == other.VERSION

    def __hash__(self):
        return hash(self.VERSION)

    def __repr__(self):
        return f"Schema({self.VERSION!r})"

    def get_model_classes(self):
        if not hasattr(self, '_CLASSES'):
            self._CLASSES = {
                name: obj for name, obj in inspect.getmembers(self) if inspect.isclass(obj)
            }
        return self._CLASSES

    def get_members(self, element_type, include_superclass=True):
        if element_type == self.Model:
            return []
        cache = self.__dict__.setdefault('_members_cache', {})
        cache_key = (element_type, include_superclass)
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

        super_members = []
        if include_superclass:
            for superclass in inspect.getmro(element_type)[1:]:
                if superclass == self.Model:
                    break
                if not inspect.isclass(superclass) or not issubclass(superclass, self.Model):
                    continue
                super_members.extend(_element_members(self, superclass))
        members = super_members + _element_members(self, element_type)
        cache[cache_key] = members
        return members

    def _entity_formats(self):
        formats = self.__dict__.get('_entity_format_by_name')
        if formats is None:
            formats = {entity.value['name']: entity.value['format'] for entity in self.EntityEnum}
            self._entity_format_by_name = formats
        return formats

    def process_entity_value(self, key, value):
        if not value:
            return value
        if isinstance(key, self.EntityEnum):
            key = key.value['name']
        if self._entity_formats().get(key) != 'index':
            return value
        if isinstance(value, list):
            return [_trim_int(item) if item is not None else item for item in value]
        return _trim_int(value)

    def fuzzy_match_entity(self, user_key):
        ratios = [
            (item, 1.0 if item.name.startswith(user_key) else SequenceMatcher(None, user_key, item.name).quick_ratio())
            for item in self.EntityEnum
        ]
        ratios.sort(key=lambda pair: pair[1])
        return ratios[-1][0]

    def fuzzy_match_entity_key(self, user_key):
        return self.fuzzy_match_entity(user_key).value['name']

    def create_dataset(self, base_dir=None, **kwargs):
        ds = self.Dataset()
        ds._versioned_schema = self
        ds.base_dir_ = base_dir
        ds.update(**kwargs)
        ds.dataset_description = self.DatasetDescriptionFile(name="dataset_description.json")
        ds.dataset_description.BIDSVersion = self.VERSION
        ds.dataset_description.parent_object_ = ds
        return ds


def _element_members(schema, element_type):
    return [
        _member_spec(schema, name, prop)
        for name, prop in _own_properties(element_type).items()
    ]


def _own_properties(element_type):
    props = {}
    for cls in _member_sources(element_type):
        for name, value in cls.__dict__.items():
            if isinstance(value, property) and value.fget and not name.startswith('_'):
                props[name] = value
    return props


def _member_sources(element_type):
    sources = []
    for base in element_type.__bases__:
        if _is_ops_mixin(base):
            sources.append(base)
    sources.append(element_type)
    return sources


def _is_ops_mixin(cls):
    if not inspect.isclass(cls) or cls is object:
        return False
    if issubclass(cls, dict) or issubclass(cls, model_base.Model):
        return False
    return True


def _member_spec(schema, name, prop):
    extra = getattr(prop.fget, '_member', None) or {}
    type_name, max_count = _annotation_cardinality(prop)
    return {
        'name': name,
        'type': _to_type(schema, type_name),
        'min': extra.get('min', 0),
        'max': max_count,
        'use': extra.get('use', 'optional'),
        'meta': extra.get('meta', {}),
    }


def _annotation_cardinality(prop):
    annotation = prop.fget.__annotations__.get('return') if prop.fget else None
    inner, is_list = _unwrap_list(annotation)
    return _type_name(inner), inf if is_list else 1


def _unwrap_list(annotation):
    if isinstance(annotation, str):
        if annotation.startswith('List[') and annotation.endswith(']'):
            return annotation[5:-1], True
        return annotation, False
    origin = get_origin(annotation)
    if origin in (list, List):
        args = get_args(annotation)
        return (args[0] if args else Any), True
    return annotation, False


def _type_name(annotation):
    if annotation is None or annotation is Any:
        return 'dict'
    if isinstance(annotation, str):
        return annotation
    return getattr(annotation, '__name__', annotation)


def _to_type(schema, model_type_name):
    if not isinstance(model_type_name, str):
        return model_type_name
    classes = schema.get_model_classes()
    if model_type_name in classes:
        return classes[model_type_name]
    resolved = _resolve_nested(classes, model_type_name)
    if resolved is not None:
        return resolved
    aliases = {'Dict': dict, 'List': list, 'Any': dict}
    if model_type_name in aliases:
        return aliases[model_type_name]
    if model_type_name in __builtins__:
        return __builtins__[model_type_name]
    return object


def _resolve_nested(classes, model_type_name):
    if '.' not in model_type_name:
        return None
    root, rest = model_type_name.split('.', 1)
    obj = classes.get(root)
    if obj is None:
        return None
    for part in rest.split('.'):
        obj = getattr(obj, part, None)
        if obj is None:
            return None
    return obj


def _trim_int(value):
    try:
        return int(value)
    except ValueError:
        return value


def load(version: str) -> Schema:
    """Load a runtime Schema for a vendored BIDS schema version."""
    version = _normalize_version(version)
    cached = _CACHE.get(version)
    if cached is not None:
        return cached
    if version not in available_versions():
        raise FileNotFoundError(
            f"No vendored schema for version {version!r}. "
            f"Available: {', '.join(available_versions())}"
        )
    schema = Schema(version, load_json(version))
    _CACHE[version] = schema
    return schema
