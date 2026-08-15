"""In-memory BIDS graph types. Hand-maintained; not generated from YAML."""
from enum import Enum, auto
from functools import lru_cache
from typing import Any, Dict, List, Optional, TYPE_CHECKING, Tuple, get_origin

from .model_ops import ArtifactOps, DatasetOps, FileOps, FolderOps, LazyContents, ModelOps

if TYPE_CHECKING:
    from .schema import Schema


def member(pattern):
    """Override the on-disk name used when expanding this property into the graph."""
    def deco(obj):
        target = obj.fget if isinstance(obj, property) else obj
        target._member = {'meta': {'name_pattern': pattern}}
        return obj

    return deco


@lru_cache(maxsize=None)
def _property_fields(cls) -> Tuple[Tuple[str, bool], ...]:
    """Cached (name, is_list) fields for Model subclasses. Fresh list defaults are created per instance."""
    fields = []
    seen_model = False
    for klass in reversed(cls.__mro__):
        if klass is Model:
            seen_model = True
            continue
        if not seen_model:
            continue
        for name, value in klass.__dict__.items():
            if not isinstance(value, property) or not value.fget or name.startswith('_'):
                continue
            annotation = value.fget.__annotations__.get('return')
            fields.append((name, _is_list_type(annotation)))
    return tuple(fields)


def _property_defaults(cls):
    """Compatibility helper: mapping of property name -> default value (new list per call)."""
    return {name: ([] if is_list else None) for name, is_list in _property_fields(cls)}


def _is_list_type(annotation):
    if isinstance(annotation, str):
        return annotation.startswith('List[')
    return get_origin(annotation) in (list, List)


class Model(ModelOps, dict):
    # TODO(v1): switch to dataclasses for typed constructors. Blocked on Model
    # being a dict (update/values/to_dict/hash) and lazy contents as a mixin property.
    parent_object_: Optional['Model']

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        fields = _property_fields(type(self))
        if not args and not kwargs:
            for name, is_list in fields:
                self[name] = [] if is_list else None
            return

        names = [name for name, _ in fields]
        if len(args) > len(names):
            raise TypeError(
                '%s() takes %d positional arguments but %d were given'
                % (type(self).__name__, len(names) + 1, len(args) + 1))
        for name, value in zip(names, args):
            if name in kwargs:
                raise TypeError('%s() got multiple values for argument %r'
                                % (type(self).__name__, name))
            kwargs[name] = value
        field_set = set(names)
        unexpected = [key for key in kwargs if key not in field_set]
        if unexpected:
            raise TypeError('%s() got an unexpected keyword argument %r'
                            % (type(self).__name__, unexpected[0]))
        for name, is_list in fields:
            value = kwargs.get(name)
            self[name] = ([] if is_list else None) if value is None else value

    def __repr__(self) -> str:
        return str({key: (str(value)[:32] + '[...]') if len(str(value)) > 32 else value
                    for key, value in self.items()
                    if value is not None and not isinstance(value, (dict, list))})

class MetadataFieldDefinition(Model):

    @property
    def name(self) -> 'str':
        return self['name']

    @name.setter
    def name(self, name: 'str') -> None:
        self['name'] = name

    @property
    def description(self) -> 'str':
        return self['description']

    @description.setter
    def description(self, description: 'str') -> None:
        self['description'] = description

    @property
    def type(self) -> 'Dict':
        return self['type']

    @type.setter
    def type(self, type: 'Dict') -> None:
        self['type'] = type


class EntitiyDefinition(Model):

    @property
    def key(self) -> 'str':
        return self['key']

    @key.setter
    def key(self, key: 'str') -> None:
        self['key'] = key

    @property
    def name(self) -> 'str':
        return self['name']

    @name.setter
    def name(self, name: 'str') -> None:
        self['name'] = name

    @property
    def entity(self) -> 'str':
        return self['entity']

    @entity.setter
    def entity(self, entity: 'str') -> None:
        self['entity'] = entity

    @property
    def description(self) -> 'str':
        return self['description']

    @description.setter
    def description(self, description: 'str') -> None:
        self['description'] = description

    @property
    def type(self) -> 'Dict':
        return self['type']

    @type.setter
    def type(self, type: 'Dict') -> None:
        self['type'] = type


class SuffixDefinition(Model):

    @property
    def name(self) -> 'str':
        return self['name']

    @name.setter
    def name(self, name: 'str') -> None:
        self['name'] = name

    @property
    def description(self) -> 'str':
        return self['description']

    @description.setter
    def description(self, description: 'str') -> None:
        self['description'] = description

    @property
    def type(self) -> 'Dict':
        return self['type']

    @type.setter
    def type(self, type: 'Dict') -> None:
        self['type'] = type


class File(FileOps, Model):

    @property
    def name(self) -> 'str':
        return self['name']

    @name.setter
    def name(self, name: 'str') -> None:
        self['name'] = name

    @property
    def extension(self) -> 'str':
        return self['extension']

    @extension.setter
    def extension(self, extension: 'str') -> None:
        self['extension'] = extension

    @property
    def uri(self) -> 'str':
        return self['uri']

    @uri.setter
    def uri(self, uri: 'str') -> None:
        self['uri'] = uri


class JsonFile(LazyContents, File):
    pass


class Artifact(ArtifactOps, File):
    r"""An artifact is a file whose name conforms to the BIDS file naming convention."""

    @property
    def suffix(self) -> 'str':
        return self['suffix']

    @suffix.setter
    def suffix(self, suffix: 'str') -> None:
        self['suffix'] = suffix

    @property
    def datatype(self) -> 'str':
        return self['datatype']

    @datatype.setter
    def datatype(self, datatype: 'str') -> None:
        self['datatype'] = datatype

    @property
    def entities(self) -> 'List[EntityRef]':
        return self['entities']

    @entities.setter
    def entities(self, entities: 'List[EntityRef]') -> None:
        self['entities'] = entities


class MetadataArtifact(LazyContents, Artifact):
    pass


class MetadataFile(LazyContents, File):
    pass


class TSVArtifact(LazyContents, Artifact):

    @property
    def delimiter(self) -> 'str':
        return self['delimiter']

    @delimiter.setter
    def delimiter(self, delimiter: 'str') -> None:
        self['delimiter'] = delimiter


class TSVFile(LazyContents, File):

    @property
    def delimiter(self) -> 'str':
        return self['delimiter']

    @delimiter.setter
    def delimiter(self, delimiter: 'str') -> None:
        self['delimiter'] = delimiter


class Folder(FolderOps, Model):

    @property
    def name(self) -> 'str':
        return self['name']

    @name.setter
    def name(self, name: 'str') -> None:
        self['name'] = name

    @property
    def files(self) -> 'List[File]':
        return self['files']

    @files.setter
    def files(self, files: 'List[File]') -> None:
        self['files'] = files

    @property
    def folders(self) -> 'List[Folder]':
        return self['folders']

    @folders.setter
    def folders(self, folders: 'List[Folder]') -> None:
        self['folders'] = folders


class EntityRef(Model):

    @property
    def key(self) -> 'str':
        return self['key']

    @key.setter
    def key(self, key: 'str') -> None:
        self['key'] = key

    @property
    def value(self) -> 'str':
        return self['value']

    @value.setter
    def value(self, value: 'str') -> None:
        self['value'] = value


class DatasetDescriptionFile(JsonFile):
    class DatasetTypeEnum(Enum):
        raw = auto()
        derivative = auto()


    @property
    def Name(self) -> 'str':
        return self['Name']

    @Name.setter
    def Name(self, Name: 'str') -> None:
        self['Name'] = Name

    @property
    def BIDSVersion(self) -> 'str':
        return self['BIDSVersion']

    @BIDSVersion.setter
    def BIDSVersion(self, BIDSVersion: 'str') -> None:
        self['BIDSVersion'] = BIDSVersion

    @property
    def HEDVersion(self) -> 'str':
        return self['HEDVersion']

    @HEDVersion.setter
    def HEDVersion(self, HEDVersion: 'str') -> None:
        self['HEDVersion'] = HEDVersion

    @property
    def DatasetType(self) -> 'DatasetDescriptionFile.DatasetTypeEnum':
        r"""The interpretation of the dataset. MUST be one of "raw" or "derivative". For backwards compatibility, the default value is "raw"."""
        return self['DatasetType']

    @DatasetType.setter
    def DatasetType(self, DatasetType: 'DatasetDescriptionFile.DatasetTypeEnum') -> None:
        self['DatasetType'] = DatasetType

    @property
    def License(self) -> 'str':
        return self['License']

    @License.setter
    def License(self, License: 'str') -> None:
        self['License'] = License

    @property
    def Acknowledgements(self) -> 'str':
        return self['Acknowledgements']

    @Acknowledgements.setter
    def Acknowledgements(self, Acknowledgements: 'str') -> None:
        self['Acknowledgements'] = Acknowledgements

    @property
    def HowToAcknowledge(self) -> 'str':
        return self['HowToAcknowledge']

    @HowToAcknowledge.setter
    def HowToAcknowledge(self, HowToAcknowledge: 'str') -> None:
        self['HowToAcknowledge'] = HowToAcknowledge

    @property
    def DatasetDOI(self) -> 'str':
        return self['DatasetDOI']

    @DatasetDOI.setter
    def DatasetDOI(self, DatasetDOI: 'str') -> None:
        self['DatasetDOI'] = DatasetDOI

    @property
    def Authors(self) -> 'List[str]':
        return self['Authors']

    @Authors.setter
    def Authors(self, Authors: 'List[str]') -> None:
        self['Authors'] = Authors

    @property
    def Funding(self) -> 'List[str]':
        return self['Funding']

    @Funding.setter
    def Funding(self, Funding: 'List[str]') -> None:
        self['Funding'] = Funding

    @property
    def EthicsApprovals(self) -> 'List[str]':
        return self['EthicsApprovals']

    @EthicsApprovals.setter
    def EthicsApprovals(self, EthicsApprovals: 'List[str]') -> None:
        self['EthicsApprovals'] = EthicsApprovals

    @property
    def ReferencesAndLinks(self) -> 'List[str]':
        return self['ReferencesAndLinks']

    @ReferencesAndLinks.setter
    def ReferencesAndLinks(self, ReferencesAndLinks: 'List[str]') -> None:
        self['ReferencesAndLinks'] = ReferencesAndLinks


class DerivativeDatasetDescriptionFile(DatasetDescriptionFile):

    @property
    def GeneratedBy(self) -> 'List[GeneratedBy]':
        return self['GeneratedBy']

    @GeneratedBy.setter
    def GeneratedBy(self, GeneratedBy: 'List[GeneratedBy]') -> None:
        self['GeneratedBy'] = GeneratedBy

    @property
    def SourceDatasets(self) -> 'List[SourceDatasets]':
        return self['SourceDatasets']

    @SourceDatasets.setter
    def SourceDatasets(self, SourceDatasets: 'List[SourceDatasets]') -> None:
        self['SourceDatasets'] = SourceDatasets


class DerivativeFolder(Folder):

    @property
    def dataset_description(self) -> 'DerivativeDatasetDescriptionFile':
        return self['dataset_description']

    @dataset_description.setter
    def dataset_description(self, dataset_description: 'DerivativeDatasetDescriptionFile') -> None:
        self['dataset_description'] = dataset_description


class SessionFolder(Folder):

    @property
    def datatypes(self) -> 'List[DatatypeFolder]':
        return self['datatypes']

    @datatypes.setter
    def datatypes(self, datatypes: 'List[DatatypeFolder]') -> None:
        self['datatypes'] = datatypes


class DatatypeFolder(Folder):
    pass


class Subject(Folder):

    @member('ses-.*')
    @property
    def sessions(self) -> 'List[SessionFolder]':
        return self['sessions']

    @sessions.setter
    def sessions(self, sessions: 'List[SessionFolder]') -> None:
        self['sessions'] = sessions

    @member('.*')
    @property
    def datatypes(self) -> 'List[DatatypeFolder]':
        return self['datatypes']

    @datatypes.setter
    def datatypes(self, datatypes: 'List[DatatypeFolder]') -> None:
        self['datatypes'] = datatypes


class GeneratedBy(Model):

    @property
    def Name(self) -> 'str':
        return self['Name']

    @Name.setter
    def Name(self, Name: 'str') -> None:
        self['Name'] = Name

    @property
    def Version(self) -> 'str':
        return self['Version']

    @Version.setter
    def Version(self, Version: 'str') -> None:
        self['Version'] = Version

    @property
    def Description(self) -> 'str':
        return self['Description']

    @Description.setter
    def Description(self, Description: 'str') -> None:
        self['Description'] = Description

    @property
    def CodeURL(self) -> 'str':
        return self['CodeURL']

    @CodeURL.setter
    def CodeURL(self, CodeURL: 'str') -> None:
        self['CodeURL'] = CodeURL

    @property
    def Container(self) -> 'List[GeneratedByContainer]':
        return self['Container']

    @Container.setter
    def Container(self, Container: 'List[GeneratedByContainer]') -> None:
        self['Container'] = Container


class SourceDatasets(Model):

    @property
    def DOI(self) -> 'str':
        return self['DOI']

    @DOI.setter
    def DOI(self, DOI: 'str') -> None:
        self['DOI'] = DOI

    @property
    def URL(self) -> 'str':
        return self['URL']

    @URL.setter
    def URL(self, URL: 'str') -> None:
        self['URL'] = URL

    @property
    def Version(self) -> 'str':
        return self['Version']

    @Version.setter
    def Version(self, Version: 'str') -> None:
        self['Version'] = Version


class GeneratedByContainer(Model):

    @property
    def Type(self) -> 'str':
        return self['Type']

    @Type.setter
    def Type(self, Type: 'str') -> None:
        self['Type'] = Type

    @property
    def Tag(self) -> 'str':
        return self['Tag']

    @Tag.setter
    def Tag(self, Tag: 'str') -> None:
        self['Tag'] = Tag

    @property
    def URI(self) -> 'str':
        return self['URI']

    @URI.setter
    def URI(self, URI: 'str') -> None:
        self['URI'] = URI


class Dataset(DatasetOps, Folder):
    r"""The entry point of an in-memory graph representation of a BIDS dataset."""
    base_dir_: Optional[str]
    _versioned_schema: Optional['Schema']


    @member('sub-.*')
    @property
    def subjects(self) -> 'List[Subject]':
        return self['subjects']

    @subjects.setter
    def subjects(self, subjects: 'List[Subject]') -> None:
        self['subjects'] = subjects

    @property
    def dataset_description(self) -> 'DatasetDescriptionFile':
        return self['dataset_description']

    @dataset_description.setter
    def dataset_description(self, dataset_description: 'DatasetDescriptionFile') -> None:
        self['dataset_description'] = dataset_description

    @property
    def README(self) -> 'File':
        return self['README']

    @README.setter
    def README(self, README: 'File') -> None:
        self['README'] = README

    @property
    def CHANGES(self) -> 'File':
        return self['CHANGES']

    @CHANGES.setter
    def CHANGES(self, CHANGES: 'File') -> None:
        self['CHANGES'] = CHANGES

    @property
    def LICENSE(self) -> 'File':
        return self['LICENSE']

    @LICENSE.setter
    def LICENSE(self, LICENSE: 'File') -> None:
        self['LICENSE'] = LICENSE

    @property
    def genetic_info(self) -> 'JsonFile':
        return self['genetic_info']

    @genetic_info.setter
    def genetic_info(self, genetic_info: 'JsonFile') -> None:
        self['genetic_info'] = genetic_info

    @property
    def samples(self) -> 'JsonFile':
        return self['samples']

    @samples.setter
    def samples(self, samples: 'JsonFile') -> None:
        self['samples'] = samples

    @member('participants.tsv')
    @property
    def participants_tsv(self) -> 'File':
        return self['participants_tsv']

    @participants_tsv.setter
    def participants_tsv(self, participants_tsv: 'File') -> None:
        self['participants_tsv'] = participants_tsv

    @member('participants.json')
    @property
    def participants_json(self) -> 'JsonFile':
        return self['participants_json']

    @participants_json.setter
    def participants_json(self, participants_json: 'JsonFile') -> None:
        self['participants_json'] = participants_json

    @property
    def code(self) -> 'Folder':
        return self['code']

    @code.setter
    def code(self, code: 'Folder') -> None:
        self['code'] = code

    @property
    def derivatives(self) -> 'Folder':
        return self['derivatives']

    @derivatives.setter
    def derivatives(self, derivatives: 'Folder') -> None:
        self['derivatives'] = derivatives

    @property
    def sourcedata(self) -> 'Folder':
        return self['sourcedata']

    @sourcedata.setter
    def sourcedata(self, sourcedata: 'Folder') -> None:
        self['sourcedata'] = sourcedata

    @property
    def stimuli(self) -> 'Folder':
        return self['stimuli']

    @stimuli.setter
    def stimuli(self, stimuli: 'Folder') -> None:
        self['stimuli'] = stimuli


class DatatypeEnum(Enum):
 pass
class ModalityEnum(Enum):
 pass
class SuffixEnum(Enum):
 pass
class EntityEnum(Enum):
 pass
