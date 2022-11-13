from enum import Enum, auto
from typing import List, Union, Dict, Any
from math import inf
import sys

VERSION = 'v1.8.0'
SCHEMA = sys.modules[__name__]

class Model(dict):
    def __init__(self, *args, **kwargs):
        self._schema = SCHEMA

    def get_schema(self):
        return self._schema
        
    def __repr__(self):
        return str({key: (str(value)[:32] + '[...]') if len(str(value)) > 32 else value
                    for key, value in self.items()
                    if value is not None and not isinstance(value, (dict, list))})
        
class MetadataFieldDefinition(Model):
    def __init__(self, name: 'str' = None, description: 'str' = None, type: 'Dict' = None):
        super(MetadataFieldDefinition, self).__init__()
        self['name'] = name or None
        self['description'] = description or None
        self['type'] = type or None

    @property
    def name(self) -> 'str':
        return self['name']

    @name.setter
    def name(self, name: 'str'):
        self['name'] = name
            
    @property
    def description(self) -> 'str':
        return self['description']

    @description.setter
    def description(self, description: 'str'):
        self['description'] = description
            
    @property
    def type(self) -> 'Dict':
        return self['type']

    @type.setter
    def type(self, type: 'Dict'):
        self['type'] = type
            
    MEMBERS = {
        'name': {'type': 'str', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'description': {'type': 'str', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'type': {'type': 'dict', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
    }


class EntitiyDefinition(Model):
    def __init__(self, key: 'str' = None, name: 'str' = None, entity: 'str' = None, description: 'str' = None, type: 'Dict' = None):
        super(EntitiyDefinition, self).__init__()
        self['key'] = key or None
        self['name'] = name or None
        self['entity'] = entity or None
        self['description'] = description or None
        self['type'] = type or None

    @property
    def key(self) -> 'str':
        return self['key']

    @key.setter
    def key(self, key: 'str'):
        self['key'] = key
            
    @property
    def name(self) -> 'str':
        return self['name']

    @name.setter
    def name(self, name: 'str'):
        self['name'] = name
            
    @property
    def entity(self) -> 'str':
        return self['entity']

    @entity.setter
    def entity(self, entity: 'str'):
        self['entity'] = entity
            
    @property
    def description(self) -> 'str':
        return self['description']

    @description.setter
    def description(self, description: 'str'):
        self['description'] = description
            
    @property
    def type(self) -> 'Dict':
        return self['type']

    @type.setter
    def type(self, type: 'Dict'):
        self['type'] = type
            
    MEMBERS = {
        'key': {'type': 'str', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'name': {'type': 'str', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'entity': {'type': 'str', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'description': {'type': 'str', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'type': {'type': 'dict', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
    }


class SuffixDefinition(Model):
    def __init__(self, name: 'str' = None, description: 'str' = None, type: 'Dict' = None):
        super(SuffixDefinition, self).__init__()
        self['name'] = name or None
        self['description'] = description or None
        self['type'] = type or None

    @property
    def name(self) -> 'str':
        return self['name']

    @name.setter
    def name(self, name: 'str'):
        self['name'] = name
            
    @property
    def description(self) -> 'str':
        return self['description']

    @description.setter
    def description(self, description: 'str'):
        self['description'] = description
            
    @property
    def type(self) -> 'Dict':
        return self['type']

    @type.setter
    def type(self, type: 'Dict'):
        self['type'] = type
            
    MEMBERS = {
        'name': {'type': 'str', 'min': 0, 'max': 1, 'use': 'required', 'meta': {}},
        'description': {'type': 'str', 'min': 0, 'max': 1, 'use': 'required', 'meta': {}},
        'type': {'type': 'dict', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
    }


class File(Model):
    def __init__(self, name: 'str' = None, extension: 'str' = None, uri: 'str' = None):
        super(File, self).__init__()
        self['name'] = name or None
        self['extension'] = extension or None
        self['uri'] = uri or None

    @property
    def name(self) -> 'str':
        return self['name']

    @name.setter
    def name(self, name: 'str'):
        self['name'] = name
            
    @property
    def extension(self) -> 'str':
        return self['extension']

    @extension.setter
    def extension(self, extension: 'str'):
        self['extension'] = extension
            
    @property
    def uri(self) -> 'str':
        return self['uri']

    @uri.setter
    def uri(self, uri: 'str'):
        self['uri'] = uri
            
    MEMBERS = {
        'name': {'type': 'str', 'min': 0, 'max': 1, 'use': 'required', 'meta': {}},
        'extension': {'type': 'str', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'uri': {'type': 'str', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
    }


class JsonFile(File):
    def __init__(self, contents: 'Dict' = None, name: 'str' = None, extension: 'str' = None, uri: 'str' = None):
        super(JsonFile, self).__init__(name or None, extension or None, uri or None)
        self['contents'] = contents or None

    @property
    def contents(self) -> 'Dict':
        return self['contents']

    @contents.setter
    def contents(self, contents: 'Dict'):
        self['contents'] = contents
            
    MEMBERS = {
        'contents': {'type': 'dict', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
    }


class Artifact(File):
    r"""An artifact is a file whose name conforms to the BIDS file naming convention."""
    def __init__(self, suffix: 'str' = None, entities: 'List[EntityRef]' = None, name: 'str' = None, extension: 'str' = None, uri: 'str' = None):
        super(Artifact, self).__init__(name or None, extension or None, uri or None)
        self['suffix'] = suffix or None
        self['entities'] = entities or []

    @property
    def suffix(self) -> 'str':
        return self['suffix']

    @suffix.setter
    def suffix(self, suffix: 'str'):
        self['suffix'] = suffix
            
    @property
    def entities(self) -> 'List[EntityRef]':
        return self['entities']

    @entities.setter
    def entities(self, entities: 'List[EntityRef]'):
        self['entities'] = entities
            
    MEMBERS = {
        'suffix': {'type': 'str', 'min': 0, 'max': 1, 'use': 'required', 'meta': {}},
        'entities': {'type': 'EntityRef', 'min': 1, 'max': inf, 'use': 'optional', 'meta': {}},
    }


class MetadataFile(Artifact):
    def __init__(self, contents: 'Dict' = None, suffix: 'str' = None, entities: 'List[EntityRef]' = None, name: 'str' = None, extension: 'str' = None, uri: 'str' = None):
        super(MetadataFile, self).__init__(suffix or None, entities or [], name or None, extension or None, uri or None)
        self['contents'] = contents or None

    @property
    def contents(self) -> 'Dict':
        return self['contents']

    @contents.setter
    def contents(self, contents: 'Dict'):
        self['contents'] = contents
            
    MEMBERS = {
        'contents': {'type': 'dict', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
    }


class Folder(Model):
    def __init__(self, name: 'str' = None, files: 'List[File]' = None, folders: 'List[Folder]' = None, metadatafiles: 'List[MetadataFile]' = None):
        super(Folder, self).__init__()
        self['name'] = name or None
        self['files'] = files or []
        self['folders'] = folders or []
        self['metadatafiles'] = metadatafiles or []

    @property
    def name(self) -> 'str':
        return self['name']

    @name.setter
    def name(self, name: 'str'):
        self['name'] = name
            
    @property
    def files(self) -> 'List[File]':
        return self['files']

    @files.setter
    def files(self, files: 'List[File]'):
        self['files'] = files
            
    @property
    def folders(self) -> 'List[Folder]':
        return self['folders']

    @folders.setter
    def folders(self, folders: 'List[Folder]'):
        self['folders'] = folders
            
    @property
    def metadatafiles(self) -> 'List[MetadataFile]':
        return self['metadatafiles']

    @metadatafiles.setter
    def metadatafiles(self, metadatafiles: 'List[MetadataFile]'):
        self['metadatafiles'] = metadatafiles
            
    MEMBERS = {
        'name': {'type': 'str', 'min': 0, 'max': 1, 'use': 'required', 'meta': {}},
        'files': {'type': 'File', 'min': 0, 'max': inf, 'use': 'optional', 'meta': {}},
        'folders': {'type': 'Folder', 'min': 0, 'max': inf, 'use': 'optional', 'meta': {}},
        'metadatafiles': {'type': 'MetadataFile', 'min': 0, 'max': inf, 'use': 'optional', 'meta': {'name_pattern': '*.json'}},
    }


class EntityRef(Model):
    def __init__(self, key: 'str' = None, value: 'str' = None):
        super(EntityRef, self).__init__()
        self['key'] = key or None
        self['value'] = value or None

    @property
    def key(self) -> 'str':
        return self['key']

    @key.setter
    def key(self, key: 'str'):
        self['key'] = key
            
    @property
    def value(self) -> 'str':
        return self['value']

    @value.setter
    def value(self, value: 'str'):
        self['value'] = value
            
    MEMBERS = {
        'key': {'type': 'str', 'min': 0, 'max': 1, 'use': 'required', 'meta': {}},
        'value': {'type': 'str', 'min': 0, 'max': 1, 'use': 'required', 'meta': {}},
    }


class DatasetDescriptionFile(JsonFile):
    class DatasetTypeEnum(Enum):
        raw = auto()
        derivative = auto()

    def __init__(self, Name: 'str' = None, BIDSVersion: 'str' = None, HEDVersion: 'str' = None, DatasetType: 'DatasetDescriptionFile.DatasetTypeEnum' = None, License: 'str' = None, Acknowledgements: 'str' = None, HowToAcknowledge: 'str' = None, DatasetDOI: 'str' = None, Authors: 'List[str]' = None, Funding: 'List[str]' = None, EthicsApprovals: 'List[str]' = None, ReferencesAndLinks: 'List[str]' = None, contents: 'Dict' = None, name: 'str' = None, extension: 'str' = None, uri: 'str' = None):
        super(DatasetDescriptionFile, self).__init__(contents or None, name or None, extension or None, uri or None)
        self['Name'] = Name or None
        self['BIDSVersion'] = BIDSVersion or None
        self['HEDVersion'] = HEDVersion or None
        self['DatasetType'] = DatasetType or None
        self['License'] = License or None
        self['Acknowledgements'] = Acknowledgements or None
        self['HowToAcknowledge'] = HowToAcknowledge or None
        self['DatasetDOI'] = DatasetDOI or None
        self['Authors'] = Authors or []
        self['Funding'] = Funding or []
        self['EthicsApprovals'] = EthicsApprovals or []
        self['ReferencesAndLinks'] = ReferencesAndLinks or []

    @property
    def Name(self) -> 'str':
        return self['Name']

    @Name.setter
    def Name(self, Name: 'str'):
        self['Name'] = Name
            
    @property
    def BIDSVersion(self) -> 'str':
        return self['BIDSVersion']

    @BIDSVersion.setter
    def BIDSVersion(self, BIDSVersion: 'str'):
        self['BIDSVersion'] = BIDSVersion
            
    @property
    def HEDVersion(self) -> 'str':
        return self['HEDVersion']

    @HEDVersion.setter
    def HEDVersion(self, HEDVersion: 'str'):
        self['HEDVersion'] = HEDVersion
            
    @property
    def DatasetType(self) -> 'DatasetDescriptionFile.DatasetTypeEnum':
        r"""The interpretation of the dataset. MUST be one of "raw" or "derivative". For backwards compatibility, the default value is "raw"."""
        return self['DatasetType']

    @DatasetType.setter
    def DatasetType(self, DatasetType: 'DatasetDescriptionFile.DatasetTypeEnum'):
        self['DatasetType'] = DatasetType
            
    @property
    def License(self) -> 'str':
        return self['License']

    @License.setter
    def License(self, License: 'str'):
        self['License'] = License
            
    @property
    def Acknowledgements(self) -> 'str':
        return self['Acknowledgements']

    @Acknowledgements.setter
    def Acknowledgements(self, Acknowledgements: 'str'):
        self['Acknowledgements'] = Acknowledgements
            
    @property
    def HowToAcknowledge(self) -> 'str':
        return self['HowToAcknowledge']

    @HowToAcknowledge.setter
    def HowToAcknowledge(self, HowToAcknowledge: 'str'):
        self['HowToAcknowledge'] = HowToAcknowledge
            
    @property
    def DatasetDOI(self) -> 'str':
        return self['DatasetDOI']

    @DatasetDOI.setter
    def DatasetDOI(self, DatasetDOI: 'str'):
        self['DatasetDOI'] = DatasetDOI
            
    @property
    def Authors(self) -> 'List[str]':
        return self['Authors']

    @Authors.setter
    def Authors(self, Authors: 'List[str]'):
        self['Authors'] = Authors
            
    @property
    def Funding(self) -> 'List[str]':
        return self['Funding']

    @Funding.setter
    def Funding(self, Funding: 'List[str]'):
        self['Funding'] = Funding
            
    @property
    def EthicsApprovals(self) -> 'List[str]':
        return self['EthicsApprovals']

    @EthicsApprovals.setter
    def EthicsApprovals(self, EthicsApprovals: 'List[str]'):
        self['EthicsApprovals'] = EthicsApprovals
            
    @property
    def ReferencesAndLinks(self) -> 'List[str]':
        return self['ReferencesAndLinks']

    @ReferencesAndLinks.setter
    def ReferencesAndLinks(self, ReferencesAndLinks: 'List[str]'):
        self['ReferencesAndLinks'] = ReferencesAndLinks
            
    MEMBERS = {
        'Name': {'type': 'str', 'min': 0, 'max': 1, 'use': 'required', 'meta': {}},
        'BIDSVersion': {'type': 'str', 'min': 0, 'max': 1, 'use': 'required', 'meta': {}},
        'HEDVersion': {'type': 'str', 'min': 0, 'max': 1, 'use': 'recommended', 'meta': {}},
        'DatasetType': {'type': 'DatasetTypeEnum', 'min': 0, 'max': 1, 'use': 'recommended', 'meta': {}},
        'License': {'type': 'str', 'min': 0, 'max': 1, 'use': 'recommended', 'meta': {}},
        'Acknowledgements': {'type': 'str', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'HowToAcknowledge': {'type': 'str', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'DatasetDOI': {'type': 'str', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'Authors': {'type': 'str', 'min': 0, 'max': inf, 'use': 'optional', 'meta': {}},
        'Funding': {'type': 'str', 'min': 0, 'max': inf, 'use': 'optional', 'meta': {}},
        'EthicsApprovals': {'type': 'str', 'min': 0, 'max': inf, 'use': 'optional', 'meta': {}},
        'ReferencesAndLinks': {'type': 'str', 'min': 0, 'max': inf, 'use': 'optional', 'meta': {}},
    }


class DerivativeDatasetDescriptionFile(DatasetDescriptionFile):
    def __init__(self, GeneratedBy: 'List[GeneratedBy]' = None, SourceDatasets: 'List[SourceDatasets]' = None, Name: 'str' = None, BIDSVersion: 'str' = None, HEDVersion: 'str' = None, DatasetType: 'DatasetDescriptionFile.DatasetTypeEnum' = None, License: 'str' = None, Acknowledgements: 'str' = None, HowToAcknowledge: 'str' = None, DatasetDOI: 'str' = None, Authors: 'List[str]' = None, Funding: 'List[str]' = None, EthicsApprovals: 'List[str]' = None, ReferencesAndLinks: 'List[str]' = None, contents: 'Dict' = None, name: 'str' = None, extension: 'str' = None, uri: 'str' = None):
        super(DerivativeDatasetDescriptionFile, self).__init__(Name or None, BIDSVersion or None, HEDVersion or None, DatasetType or None, License or None, Acknowledgements or None, HowToAcknowledge or None, DatasetDOI or None, Authors or [], Funding or [], EthicsApprovals or [], ReferencesAndLinks or [], contents or None, name or None, extension or None, uri or None)
        self['GeneratedBy'] = GeneratedBy or []
        self['SourceDatasets'] = SourceDatasets or []

    @property
    def GeneratedBy(self) -> 'List[GeneratedBy]':
        return self['GeneratedBy']

    @GeneratedBy.setter
    def GeneratedBy(self, GeneratedBy: 'List[GeneratedBy]'):
        self['GeneratedBy'] = GeneratedBy
            
    @property
    def SourceDatasets(self) -> 'List[SourceDatasets]':
        return self['SourceDatasets']

    @SourceDatasets.setter
    def SourceDatasets(self, SourceDatasets: 'List[SourceDatasets]'):
        self['SourceDatasets'] = SourceDatasets
            
    MEMBERS = {
        'GeneratedBy': {'type': 'GeneratedBy', 'min': 0, 'max': inf, 'use': 'optional', 'meta': {}},
        'SourceDatasets': {'type': 'SourceDatasets', 'min': 0, 'max': inf, 'use': 'recommended', 'meta': {}},
    }


class DerivativeFolder(Folder):
    def __init__(self, dataset_description: 'DerivativeDatasetDescriptionFile' = None, name: 'str' = None, files: 'List[File]' = None, folders: 'List[Folder]' = None, metadatafiles: 'List[MetadataFile]' = None):
        super(DerivativeFolder, self).__init__(name or None, files or [], folders or [], metadatafiles or [])
        self['dataset_description'] = dataset_description or None

    @property
    def dataset_description(self) -> 'DerivativeDatasetDescriptionFile':
        return self['dataset_description']

    @dataset_description.setter
    def dataset_description(self, dataset_description: 'DerivativeDatasetDescriptionFile'):
        self['dataset_description'] = dataset_description
            
    MEMBERS = {
        'dataset_description': {'type': 'DerivativeDatasetDescriptionFile', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
    }


class Session(Folder):
    def __init__(self, datatypes: 'List[DatatypeFolder]' = None, name: 'str' = None, files: 'List[File]' = None, folders: 'List[Folder]' = None, metadatafiles: 'List[MetadataFile]' = None):
        super(Session, self).__init__(name or None, files or [], folders or [], metadatafiles or [])
        self['datatypes'] = datatypes or []

    @property
    def datatypes(self) -> 'List[DatatypeFolder]':
        return self['datatypes']

    @datatypes.setter
    def datatypes(self, datatypes: 'List[DatatypeFolder]'):
        self['datatypes'] = datatypes
            
    MEMBERS = {
        'datatypes': {'type': 'DatatypeFolder', 'min': 0, 'max': inf, 'use': 'optional', 'meta': {}},
    }


class DatatypeFolder(Folder):
    def __init__(self, artifacts: 'List[Artifact]' = None, name: 'str' = None, files: 'List[File]' = None, folders: 'List[Folder]' = None, metadatafiles: 'List[MetadataFile]' = None):
        super(DatatypeFolder, self).__init__(name or None, files or [], folders or [], metadatafiles or [])
        self['artifacts'] = artifacts or []

    @property
    def artifacts(self) -> 'List[Artifact]':
        return self['artifacts']

    @artifacts.setter
    def artifacts(self, artifacts: 'List[Artifact]'):
        self['artifacts'] = artifacts
            
    MEMBERS = {
        'artifacts': {'type': 'Artifact', 'min': 0, 'max': inf, 'use': 'optional', 'meta': {}},
    }


class Subject(Folder):
    def __init__(self, sessions: 'List[Session]' = None, datatypes: 'List[DatatypeFolder]' = None, name: 'str' = None, files: 'List[File]' = None, folders: 'List[Folder]' = None, metadatafiles: 'List[MetadataFile]' = None):
        super(Subject, self).__init__(name or None, files or [], folders or [], metadatafiles or [])
        self['sessions'] = sessions or []
        self['datatypes'] = datatypes or []

    @property
    def sessions(self) -> 'List[Session]':
        return self['sessions']

    @sessions.setter
    def sessions(self, sessions: 'List[Session]'):
        self['sessions'] = sessions
            
    @property
    def datatypes(self) -> 'List[DatatypeFolder]':
        return self['datatypes']

    @datatypes.setter
    def datatypes(self, datatypes: 'List[DatatypeFolder]'):
        self['datatypes'] = datatypes
            
    MEMBERS = {
        'sessions': {'type': 'Session', 'min': 0, 'max': inf, 'use': 'optional', 'meta': {'name_pattern': 'ses-.*'}},
        'datatypes': {'type': 'DatatypeFolder', 'min': 0, 'max': inf, 'use': 'optional', 'meta': {}},
    }


class GeneratedBy(Model):
    def __init__(self, Name: 'str' = None, Version: 'str' = None, Description: 'str' = None, CodeURL: 'str' = None, Container: 'List[GeneratedByContainer]' = None):
        super(GeneratedBy, self).__init__()
        self['Name'] = Name or None
        self['Version'] = Version or None
        self['Description'] = Description or None
        self['CodeURL'] = CodeURL or None
        self['Container'] = Container or []

    @property
    def Name(self) -> 'str':
        return self['Name']

    @Name.setter
    def Name(self, Name: 'str'):
        self['Name'] = Name
            
    @property
    def Version(self) -> 'str':
        return self['Version']

    @Version.setter
    def Version(self, Version: 'str'):
        self['Version'] = Version
            
    @property
    def Description(self) -> 'str':
        return self['Description']

    @Description.setter
    def Description(self, Description: 'str'):
        self['Description'] = Description
            
    @property
    def CodeURL(self) -> 'str':
        return self['CodeURL']

    @CodeURL.setter
    def CodeURL(self, CodeURL: 'str'):
        self['CodeURL'] = CodeURL
            
    @property
    def Container(self) -> 'List[GeneratedByContainer]':
        return self['Container']

    @Container.setter
    def Container(self, Container: 'List[GeneratedByContainer]'):
        self['Container'] = Container
            
    MEMBERS = {
        'Name': {'type': 'str', 'min': 0, 'max': 1, 'use': 'required', 'meta': {}},
        'Version': {'type': 'str', 'min': 0, 'max': 1, 'use': 'recommended', 'meta': {}},
        'Description': {'type': 'str', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'CodeURL': {'type': 'str', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'Container': {'type': 'GeneratedByContainer', 'min': 0, 'max': inf, 'use': 'optional', 'meta': {}},
    }


class SourceDatasets(Model):
    def __init__(self, DOI: 'str' = None, URL: 'str' = None, Version: 'str' = None):
        super(SourceDatasets, self).__init__()
        self['DOI'] = DOI or None
        self['URL'] = URL or None
        self['Version'] = Version or None

    @property
    def DOI(self) -> 'str':
        return self['DOI']

    @DOI.setter
    def DOI(self, DOI: 'str'):
        self['DOI'] = DOI
            
    @property
    def URL(self) -> 'str':
        return self['URL']

    @URL.setter
    def URL(self, URL: 'str'):
        self['URL'] = URL
            
    @property
    def Version(self) -> 'str':
        return self['Version']

    @Version.setter
    def Version(self, Version: 'str'):
        self['Version'] = Version
            
    MEMBERS = {
        'DOI': {'type': 'str', 'min': 0, 'max': 1, 'use': 'required', 'meta': {}},
        'URL': {'type': 'str', 'min': 0, 'max': 1, 'use': 'required', 'meta': {}},
        'Version': {'type': 'str', 'min': 0, 'max': 1, 'use': 'required', 'meta': {}},
    }


class GeneratedByContainer(Model):
    def __init__(self, Type: 'str' = None, Tag: 'str' = None, URI: 'str' = None):
        super(GeneratedByContainer, self).__init__()
        self['Type'] = Type or None
        self['Tag'] = Tag or None
        self['URI'] = URI or None

    @property
    def Type(self) -> 'str':
        return self['Type']

    @Type.setter
    def Type(self, Type: 'str'):
        self['Type'] = Type
            
    @property
    def Tag(self) -> 'str':
        return self['Tag']

    @Tag.setter
    def Tag(self, Tag: 'str'):
        self['Tag'] = Tag
            
    @property
    def URI(self) -> 'str':
        return self['URI']

    @URI.setter
    def URI(self, URI: 'str'):
        self['URI'] = URI
            
    MEMBERS = {
        'Type': {'type': 'str', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'Tag': {'type': 'str', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'URI': {'type': 'str', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
    }


class Dataset(Folder):
    r"""The entry point of an in-memory graph representation of a BIDS dataset."""
    def __init__(self, subjects: 'List[Subject]' = None, dataset_description: 'DatasetDescriptionFile' = None, README: 'File' = None, CHANGES: 'File' = None, LICENSE: 'File' = None, genetic_info: 'JsonFile' = None, samples: 'JsonFile' = None, participants_tsv: 'File' = None, participants_json: 'JsonFile' = None, code: 'Folder' = None, derivatives: 'Folder' = None, sourcedata: 'Folder' = None, stimuli: 'Folder' = None, name: 'str' = None, files: 'List[File]' = None, folders: 'List[Folder]' = None, metadatafiles: 'List[MetadataFile]' = None):
        super(Dataset, self).__init__(name or None, files or [], folders or [], metadatafiles or [])
        self['subjects'] = subjects or []
        self['dataset_description'] = dataset_description or None
        self['README'] = README or None
        self['CHANGES'] = CHANGES or None
        self['LICENSE'] = LICENSE or None
        self['genetic_info'] = genetic_info or None
        self['samples'] = samples or None
        self['participants_tsv'] = participants_tsv or None
        self['participants_json'] = participants_json or None
        self['code'] = code or None
        self['derivatives'] = derivatives or None
        self['sourcedata'] = sourcedata or None
        self['stimuli'] = stimuli or None

    @property
    def subjects(self) -> 'List[Subject]':
        return self['subjects']

    @subjects.setter
    def subjects(self, subjects: 'List[Subject]'):
        self['subjects'] = subjects
            
    @property
    def dataset_description(self) -> 'DatasetDescriptionFile':
        return self['dataset_description']

    @dataset_description.setter
    def dataset_description(self, dataset_description: 'DatasetDescriptionFile'):
        self['dataset_description'] = dataset_description
            
    @property
    def README(self) -> 'File':
        return self['README']

    @README.setter
    def README(self, README: 'File'):
        self['README'] = README
            
    @property
    def CHANGES(self) -> 'File':
        return self['CHANGES']

    @CHANGES.setter
    def CHANGES(self, CHANGES: 'File'):
        self['CHANGES'] = CHANGES
            
    @property
    def LICENSE(self) -> 'File':
        return self['LICENSE']

    @LICENSE.setter
    def LICENSE(self, LICENSE: 'File'):
        self['LICENSE'] = LICENSE
            
    @property
    def genetic_info(self) -> 'JsonFile':
        return self['genetic_info']

    @genetic_info.setter
    def genetic_info(self, genetic_info: 'JsonFile'):
        self['genetic_info'] = genetic_info
            
    @property
    def samples(self) -> 'JsonFile':
        return self['samples']

    @samples.setter
    def samples(self, samples: 'JsonFile'):
        self['samples'] = samples
            
    @property
    def participants_tsv(self) -> 'File':
        return self['participants_tsv']

    @participants_tsv.setter
    def participants_tsv(self, participants_tsv: 'File'):
        self['participants_tsv'] = participants_tsv
            
    @property
    def participants_json(self) -> 'JsonFile':
        return self['participants_json']

    @participants_json.setter
    def participants_json(self, participants_json: 'JsonFile'):
        self['participants_json'] = participants_json
            
    @property
    def code(self) -> 'Folder':
        return self['code']

    @code.setter
    def code(self, code: 'Folder'):
        self['code'] = code
            
    @property
    def derivatives(self) -> 'Folder':
        return self['derivatives']

    @derivatives.setter
    def derivatives(self, derivatives: 'Folder'):
        self['derivatives'] = derivatives
            
    @property
    def sourcedata(self) -> 'Folder':
        return self['sourcedata']

    @sourcedata.setter
    def sourcedata(self, sourcedata: 'Folder'):
        self['sourcedata'] = sourcedata
            
    @property
    def stimuli(self) -> 'Folder':
        return self['stimuli']

    @stimuli.setter
    def stimuli(self, stimuli: 'Folder'):
        self['stimuli'] = stimuli
            
    MEMBERS = {
        'subjects': {'type': 'Subject', 'min': 0, 'max': inf, 'use': 'optional', 'meta': {'name_pattern': 'sub-.*'}},
        'dataset_description': {'type': 'DatasetDescriptionFile', 'min': 0, 'max': 1, 'use': 'required', 'meta': {}},
        'README': {'type': 'File', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'CHANGES': {'type': 'File', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'LICENSE': {'type': 'File', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'genetic_info': {'type': 'JsonFile', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'samples': {'type': 'JsonFile', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'participants_tsv': {'type': 'File', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'participants_json': {'type': 'JsonFile', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'code': {'type': 'Folder', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'derivatives': {'type': 'Folder', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'sourcedata': {'type': 'Folder', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'stimuli': {'type': 'Folder', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
    }


class DatatypeEnum(Enum):
    anat = r"anat", r"Anatomical Magnetic Resonance Imaging"
    r"""Magnetic resonance imaging sequences designed to characterize static, anatomical features."""
    beh = r"beh", r"Behavioral Data"
    r"""Behavioral data."""
    dwi = r"dwi", r"Diffusion-Weighted Imaging"
    r"""Diffusion-weighted imaging (DWI)."""
    eeg = r"eeg", r"Electroencephalography"
    r"""Electroencephalography"""
    fmap = r"fmap", r"Field maps"
    r"""MRI scans for estimating B0 inhomogeneity-induced distortions."""
    func = r"func", r"Task-Based Magnetic Resonance Imaging"
    r"""Task (including resting state) imaging data"""
    ieeg = r"ieeg", r"Intracranial electroencephalography"
    r"""Intracranial electroencephalography (iEEG) or electrocorticography (ECoG) data"""
    meg = r"meg", r"Magnetoencephalography"
    r"""Magnetoencephalography"""
    micr = r"micr", r"Microscopy"
    r"""Microscopy"""
    perf = r"perf", r"Perfusion imaging"
    r"""Blood perfusion imaging data, including arterial spin labeling (ASL)"""
    pet = r"pet", r"Positron Emission Tomography"
    r"""Positron emission tomography data"""
    nirs = r"nirs", r"Near-Infrared Spectroscopy"
    r"""Near-Infrared Spectroscopy data organized around the SNIRF format"""

    def __init__(self, literal, display_name_):
        self.literal_ = literal
        self.display_name_ = display_name_

class ModalityEnum(Enum):
    mri = r"mri", r"Magnetic Resonance Imaging"
    r"""Data acquired with an MRI scanner."""
    eeg = r"eeg", r"Electroencephalography"
    r"""Data acquired with EEG."""
    ieeg = r"ieeg", r"Intracranial Electroencephalography"
    r"""Data acquired with iEEG."""
    meg = r"meg", r"Magnetoencephalography"
    r"""Data acquired with an MEG scanner."""
    beh = r"beh", r"Behavioral experiments"
    r"""Behavioral data acquired without accompanying neuroimaging data."""
    pet = r"pet", r"Positron Emission Tomography"
    r"""Data acquired with PET."""
    micr = r"micr", r"Microscopy"
    r"""Data acquired with a microscope."""
    nirs = r"nirs", r"Near-Infrared Spectroscopy"
    r"""Data acquired with NIRS."""

    def __init__(self, literal, display_name_):
        self.literal_ = literal
        self.display_name_ = display_name_

class SuffixEnum(Enum):
    TwoPE = r"2PE", r"2-photon excitation microscopy", r""
    r"""2-photon excitation microscopy imaging data"""
    BF = r"BF", r"Bright-field microscopy", r""
    r"""Bright-field microscopy imaging data"""
    Chimap = r"Chimap", r"Quantitative susceptibility map (QSM)", r"ppm"
    r"""In parts per million (ppm).
QSM allows for determining the underlying magnetic susceptibility of tissue
(Chi)
([Wang & Liu, 2014](https://doi.org/10.1002/mrm.25358)).
Chi maps are REQUIRED to use this suffix regardless of the method used to
generate them."""
    CARS = r"CARS", r"Coherent anti-Stokes Raman spectroscopy", r""
    r"""Coherent anti-Stokes Raman spectroscopy imaging data"""
    CONF = r"CONF", r"Confocal microscopy", r""
    r"""Confocal microscopy imaging data"""
    DIC = r"DIC", r"Differential interference contrast microscopy", r""
    r"""Differential interference contrast microscopy imaging data"""
    DF = r"DF", r"Dark-field microscopy", r""
    r"""Dark-field microscopy imaging data"""
    FLAIR = r"FLAIR", r"Fluid attenuated inversion recovery image", r"arbitrary"
    r"""In arbitrary units (arbitrary).
Structural images with predominant T2 contribution (also known as T2-FLAIR),
in which signal from fluids (for example, CSF) is nulled out by adjusting
inversion time, coupled with notably long repetition and echo times."""
    FLASH = r"FLASH", r"Fast-Low-Angle-Shot image", r""
    r"""FLASH (Fast-Low-Angle-Shot) is a vendor-specific implementation for spoiled
gradient echo acquisition.
It is commonly used for rapid anatomical imaging and also for many different
qMRI applications.
When used for a single file, it does not convey any information about the
image contrast.
When used in a file collection, it may result in conflicts across filenames of
different applications.
**Change:** Removed from suffixes."""
    FLUO = r"FLUO", r"Fluorescence microscopy", r""
    r"""Fluorescence microscopy imaging data"""
    IRT1 = r"IRT1", r"Inversion recovery T1 mapping", r""
    r"""The IRT1 method involves multiple inversion recovery spin-echo images
acquired at different inversion times
([Barral et al. 2010](https://doi.org/10.1002/mrm.22497))."""
    M0map = r"M0map", r"Equilibrium magnetization (M0) map", r"arbitrary"
    r"""In arbitrary units (arbitrary).
A common quantitative MRI (qMRI) fitting variable that represents the amount
of magnetization at thermal equilibrium.
M0 maps are RECOMMENDED to use this suffix if generated by qMRI applications
(for example, variable flip angle T1 mapping)."""
    MEGRE = r"MEGRE", r"Multi-echo Gradient Recalled Echo", r""
    r"""Anatomical gradient echo images acquired at different echo times.
Please note that this suffix is not intended for the logical grouping of
images acquired using an Echo Planar Imaging (EPI) readout."""
    MESE = r"MESE", r"Multi-echo Spin Echo", r""
    r"""The MESE method involves multiple spin echo images acquired at different echo
times and is primarily used for T2 mapping.
Please note that this suffix is not intended for the logical grouping of
images acquired using an Echo Planar Imaging (EPI) readout."""
    MP2RAGE = r"MP2RAGE", r"Magnetization Prepared Two Gradient Echoes", r""
    r"""The MP2RAGE method is a special protocol that collects several images at
different flip angles and inversion times to create a parametric T1map by
combining the magnitude and phase images
([Marques et al. 2010](https://doi.org/10.1016/j.neuroimage.2009.10.002))."""
    MPE = r"MPE", r"Multi-photon excitation microscopy", r""
    r"""Multi-photon excitation microscopy imaging data"""
    MPM = r"MPM", r"Multi-parametric Mapping", r""
    r"""The MPM approaches (a.k.a hMRI) involves the acquisition of highly-similar
anatomical images that differ in terms of application of a magnetization
transfer RF pulse (MTon or MToff), flip angle and (optionally) echo time and
magnitue/phase parts
([Weiskopf et al. 2013](https://doi.org/10.3389/fnins.2013.00095)).
See [here](https://owncloud.gwdg.de/index.php/s/iv2TOQwGy4FGDDZ) for
suggested MPM acquisition protocols."""
    MTR = r"MTR", r"Magnetization Transfer Ratio", r""
    r"""This method is to calculate a semi-quantitative magnetization transfer ratio
map."""
    MTRmap = r"MTRmap", r"Magnetization transfer ratio image", r"arbitrary"
    r"""In arbitrary units (arbitrary).
MTR maps are REQUIRED to use this suffix regardless of the method used to
generate them.
MTRmap intensity values are RECOMMENDED to be represented in percentage in
the range of 0-100%."""
    MTS = r"MTS", r"Magnetization transfer saturation", r""
    r"""This method is to calculate a semi-quantitative magnetization transfer
saturation index map.
The MTS method involves three sets of anatomical images that differ in terms
of application of a magnetization transfer RF pulse (MTon or MToff) and flip
angle ([Helms et al. 2008](https://doi.org/10.1002/mrm.21732))."""
    MTVmap = r"MTVmap", r"Macromolecular tissue volume (MTV) image", r"arbitrary"
    r"""In arbitrary units (arbitrary).
MTV maps are REQUIRED to use this suffix regardless of the method used to
generate them."""
    MTsat = r"MTsat", r"Magnetization transfer saturation image", r"arbitrary"
    r"""In arbitrary units (arbitrary).
MTsat maps are REQUIRED to use this suffix regardless of the method used to
generate them."""
    MWFmap = r"MWFmap", r"Myelin water fraction image", r"arbitrary"
    r"""In arbitrary units (arbitrary).
MWF maps are REQUIRED to use this suffix regardless of the method used to
generate them.
MWF intensity values are RECOMMENDED to be represented in percentage in the
range of 0-100%."""
    NLO = r"NLO", r"Nonlinear optical microscopy", r""
    r"""Nonlinear optical microscopy imaging data"""
    OCT = r"OCT", r"Optical coherence tomography", r""
    r"""Optical coherence tomography imaging data"""
    PC = r"PC", r"Phase-contrast microscopy", r""
    r"""Phase-contrast microscopy imaging data"""
    PD = r"PD", r"Proton density image", r"arbitrary"
    r"""Ambiguous, may refer to a parametric image or to a conventional image.
**Change:** Replaced by `PDw` or `PDmap`."""
    PDT2 = r"PDT2", r"PD and T2 weighted image", r"arbitrary"
    r"""In arbitrary units (arbitrary).
PDw and T2w images acquired using a dual echo FSE sequence through view
sharing process
([Johnson et al. 1994](https://pubmed.ncbi.nlm.nih.gov/8010268/))."""
    PDT2map = r"PDT2map", r"Combined PD/T2 image", r"arbitrary"
    r"""In arbitrary units (arbitrary).
Combined PD/T2 maps are REQUIRED to use this suffix regardless of the method
used to generate them."""
    PDmap = r"PDmap", r"Proton density image", r"arbitrary"
    r"""In arbitrary units (arbitrary).
PD maps are REQUIRED to use this suffix regardless of the method used to
generate them."""
    PDw = r"PDw", r"Proton density (PD) weighted image", r"arbitrary"
    r"""In arbitrary units (arbitrary).
The contrast of these images is mainly determined by spatial variations in
the spin density (1H) of the imaged specimen.
In spin-echo sequences this contrast is achieved at short repetition and long
echo times.
In a gradient-echo acquisition, PD weighting dominates the contrast at long
repetition and short echo times, and at small flip angles."""
    PLI = r"PLI", r"Polarized-light microscopy", r""
    r"""Polarized-light microscopy imaging data"""
    R1map = r"R1map", r"Longitudinal relaxation rate image", r"1/s"
    r"""In seconds<sup>-1</sup> (1/s).
R1 maps (R1 = 1/T1) are REQUIRED to use this suffix regardless of the method
used to generate them."""
    R2map = r"R2map", r"True transverse relaxation rate image", r"1/s"
    r"""In seconds<sup>-1</sup> (1/s).
R2 maps (R2 = 1/T2) are REQUIRED to use this suffix regardless of the method
used to generate them."""
    R2starmap = r"R2starmap", r"Observed transverse relaxation rate image", r"1/s"
    r"""In seconds<sup>-1</sup> (1/s).
R2-star maps (R2star = 1/T2star) are REQUIRED to use this suffix regardless
of the method used to generate them."""
    RB1COR = r"RB1COR", r"RB1COR", r""
    r"""Low resolution images acquired by the body coil
(in the gantry of the scanner) and the head coil using identical acquisition
parameters to generate a combined sensitivity map as described in
[Papp et al. (2016)](https://doi.org/10.1002/mrm.26058)."""
    RB1map = r"RB1map", r"RF receive sensitivity map", r"arbitrary"
    r"""In arbitrary units (arbitrary).
Radio frequency (RF) receive (B1-) sensitivity maps are REQUIRED to use this
suffix regardless of the method used to generate them.
RB1map intensity values are RECOMMENDED to be represented as percent
multiplicative factors such that Amplitude<sub>effective</sub> =
B1-<sub>intensity</sub>\*Amplitude<sub>ideal</sub>."""
    S0map = r"S0map", r"Observed signal amplitude (S0) image", r""
    r"""In arbitrary units (arbitrary).
For a multi-echo (typically fMRI) sequence, S0 maps index the baseline signal
before exponential (T2-star) signal decay.
In other words: the exponential of the intercept for a linear decay model
across log-transformed echos. For more information, please see, for example,
[the tedana documentation](https://tedana.readthedocs.io/en/latest/\
approach.html#monoexponential-decay-model-fit).
S0 maps are RECOMMENDED to use this suffix if derived from an ME-FMRI dataset."""
    SEM = r"SEM", r"Scanning electron microscopy", r""
    r"""Scanning electron microscopy imaging data"""
    SPIM = r"SPIM", r"Selective plane illumination microscopy", r""
    r"""Selective plane illumination microscopy imaging data"""
    SR = r"SR", r"Super-resolution microscopy", r""
    r"""Super-resolution microscopy imaging data"""
    T1map = r"T1map", r"Longitudinal relaxation time image", r"s"
    r"""In seconds (s).
T1 maps are REQUIRED to use this suffix regardless of the method used to
generate them.
See [this interactive book on T1 mapping](https://qmrlab.org/t1_book/intro)
for further reading on T1-mapping."""
    T1rho = r"T1rho", r"T1 in rotating frame (T1 rho) image", r"s"
    r"""In seconds (s).
T1-rho maps are REQUIRED to use this suffix regardless of the method used to
generate them."""
    T1w = r"T1w", r"T1-weighted image", r"arbitrary"
    r"""In arbitrary units (arbitrary).
The contrast of these images is mainly determined by spatial variations in
the longitudinal relaxation time of the imaged specimen.
In spin-echo sequences this contrast is achieved at relatively short
repetition and echo times.
To achieve this weighting in gradient-echo images, again, short repetition
and echo times are selected; however, at relatively large flip angles.
Another common approach to increase T1 weighting in gradient-echo images is
to add an inversion preparation block to the beginning of the imaging
sequence (for example, `TurboFLASH` or `MP-RAGE`)."""
    T2map = r"T2map", r"True transverse relaxation time image", r"s"
    r"""In seconds (s).
T2 maps are REQUIRED to use this suffix regardless of the method used to
generate them."""
    T2star = r"T2star", r"T2\* image", r""
    r"""Ambiguous, may refer to a parametric image or to a conventional image.
**Change:** Replaced by `T2starw` or `T2starmap`."""
    T2starmap = r"T2starmap", r"Observed transverse relaxation time image", r"s"
    r"""In seconds (s).
T2-star maps are REQUIRED to use this suffix regardless of the method used to
generate them."""
    T2starw = r"T2starw", r"T2star weighted image", r"arbitrary"
    r"""In arbitrary units (arbitrary).
The contrast of these images is mainly determined by spatial variations in
the (observed) transverse relaxation time of the imaged specimen.
In spin-echo sequences, this effect is negated as the excitation is followed
by an inversion pulse.
The contrast of gradient-echo images natively depends on T2-star effects.
However, for T2-star variation to dominate the image contrast,
gradient-echo acquisitions are carried out at long repetition and echo times,
and at small flip angles."""
    T2w = r"T2w", r"T2-weighted image", r"arbitrary"
    r"""In arbitrary units (arbitrary).
The contrast of these images is mainly determined by spatial variations in
the (true) transverse relaxation time of the imaged specimen.
In spin-echo sequences this contrast is achieved at relatively long
repetition and echo times.
Generally, gradient echo sequences are not the most suitable option for
achieving T2 weighting, as their contrast natively depends on T2-star rather
than on T2."""
    TB1AFI = r"TB1AFI", r"TB1AFI", r""
    r"""This method ([Yarnykh 2007](https://doi.org/10.1002/mrm.21120))
calculates a B1<sup>+</sup> map from two images acquired at interleaved (two)
TRs with identical RF pulses using a steady-state sequence."""
    TB1DAM = r"TB1DAM", r"TB1DAM", r""
    r"""The double-angle B1<sup>+</sup> method
([Insko and Bolinger 1993](https://doi.org/10.1006/jmra.1993.1133)) is based
on the calculation of the actual angles from signal ratios,
collected by two acquisitions at different nominal excitation flip angles.
Common sequence types for this application include spin echo and echo planar
imaging."""
    TB1EPI = r"TB1EPI", r"TB1EPI", r""
    r"""This B1<sup>+</sup> mapping method
([Jiru and Klose 2006](https://doi.org/10.1002/mrm.21083)) is based on two
EPI readouts to acquire spin echo (SE) and stimulated echo (STE) images at
multiple flip angles in one sequence, used in the calculation of deviations
from the nominal flip angle."""
    TB1RFM = r"TB1RFM", r"TB1RFM", r""
    r"""The result of a Siemens `rf_map` product sequence.
This sequence produces two images.
The first image appears like an anatomical image and the second output is a
scaled flip angle map."""
    TB1SRGE = r"TB1SRGE", r"TB1SRGE", r""
    r"""Saturation-prepared with 2 rapid gradient echoes (SA2RAGE) uses a ratio of
two saturation recovery images with different time delays,
and a simulated look-up table to estimate B1+
([Eggenschwiler et al. 2011](https://doi.org/10.1002/mrm.23145)).
This sequence can also be used in conjunction with MP2RAGE T1 mapping to
iteratively improve B1+ and T1 map estimation
([Marques & Gruetter 2013](https://doi.org/10.1371/journal.pone.0069294))."""
    TB1TFL = r"TB1TFL", r"TB1TFL", r""
    r"""The result of a Siemens `tfl_b1_map` product sequence.
This sequence produces two images.
The first image appears like an anatomical image and the second output is a
scaled flip angle map."""
    TB1map = r"TB1map", r"RF transmit field image", r"arbitrary"
    r"""In arbitrary units (arbitrary).
Radio frequency (RF) transmit (B1+) field maps are REQUIRED to use this
suffix regardless of the method used to generate them.
TB1map intensity values are RECOMMENDED to be represented as percent
multiplicative factors such that FlipAngle<sub>effective</sub> =
B1+<sub>intensity</sub>\*FlipAngle<sub>nominal</sub> ."""
    TEM = r"TEM", r"Transmission electron microscopy", r""
    r"""Transmission electron microscopy imaging data"""
    UNIT1 = r"UNIT1", r"Homogeneous (flat) T1-weighted MP2RAGE image", r""
    r"""In arbitrary units (arbitrary).
UNIT1 images are REQUIRED to use this suffix regardless of the method used to
generate them.
Note that although this image is T1-weighted, regions without MR signal will
contain white salt-and-pepper noise that most segmentation algorithms will
fail on.
Therefore, it is important to dissociate it from `T1w`.
Please see [`MP2RAGE` specific notes](SPEC_ROOT/appendices/qmri.md#unit1-images)
in the qMRI appendix for further information."""
    VFA = r"VFA", r"Variable flip angle", r""
    r"""The VFA method involves at least two spoiled gradient echo (SPGR) of
steady-state free precession (SSFP) images acquired at different flip angles.
Depending on the provided metadata fields and the sequence type,
data may be eligible for DESPOT1, DESPOT2 and their variants
([Deoni et al. 2005](https://doi.org/10.1002/mrm.20314))."""
    angio = r"angio", r"Angiogram", r""
    r"""Magnetic resonance angiography sequences focus on enhancing the contrast of
blood vessels (generally arteries, but sometimes veins) against other tissue
types."""
    asl = r"asl", r"Arterial Spin Labeling", r""
    r"""The complete ASL time series stored as a 4D NIfTI file in the original
acquisition order, with possible volume types including: control, label,
m0scan, deltam, cbf."""
    aslcontext = r"aslcontext", r"Arterial Spin Labeling Context", r""
    r"""A TSV file defining the image types for volumes in an associated ASL file."""
    asllabeling = r"asllabeling", r"ASL Labeling Screenshot", r""
    r"""An anonymized screenshot of the planning of the labeling slab/plane with
respect to the imaging slab or slices `*_asllabeling.jpg`.
Based on DICOM macro C.8.13.5.14."""
    beh = r"beh", r"Behavioral recording", r""
    r"""Behavioral recordings from tasks.
These files are similar to events files, but do not include the `"onset"` and
`"duration"` columns that are mandatory for events files."""
    blood = r"blood", r"Blood recording data", r""
    r"""Blood measurements of radioactivity stored in
[tabular files](SPEC_ROOT/common-principles.md#tabular-files)
and located in the `pet/` directory along with the corresponding PET data."""
    bold = r"bold", r"Blood-Oxygen-Level Dependent image", r""
    r"""Blood-Oxygen-Level Dependent contrast (specialized T2\* weighting)"""
    cbv = r"cbv", r"Cerebral blood volume image", r""
    r"""Cerebral Blood Volume contrast (specialized T2\* weighting or difference between T1 weighted images)"""
    channels = r"channels", r"Channels File", r""
    r"""Channel information."""
    coordsystem = r"coordsystem", r"Coordinate System File", r""
    r"""A JSON document specifying the coordinate system(s) used for the MEG, EEG,
head localization coils, and anatomical landmarks."""
    defacemask = r"defacemask", r"Defacing Mask", r""
    r"""A binary mask that was used to remove facial features from an anatomical MRI
image."""
    dseg = r"dseg", r"Discrete Segmentation", r""
    r"""A discrete segmentation.

This suffix may only be used in derivative datasets."""
    dwi = r"dwi", r"Diffusion-weighted image", r""
    r"""Diffusion-weighted imaging contrast (specialized T2 weighting)."""
    eeg = r"eeg", r"Electroencephalography", r""
    r"""Electroencephalography recording data."""
    electrodes = r"electrodes", r"Electrodes", r""
    r"""File that gives the location of (i)EEG electrodes."""
    epi = r"epi", r"EPI", r""
    r"""The phase-encoding polarity (PEpolar) technique combines two or more Spin Echo
EPI scans with different phase encoding directions to estimate the underlying
inhomogeneity/deformation map."""
    events = r"events", r"Events", r""
    r"""Event timing information from a behavioral task."""
    fieldmap = r"fieldmap", r"Fieldmap", r""
    r"""Some MR schemes such as spiral-echo imaging (SEI) sequences are able to
directly provide maps of the *B<sub>0</sub>* field inhomogeneity."""
    headshape = r"headshape", r"Headshape File", r""
    r"""The 3-D locations of points that describe the head shape and/or electrode
locations can be digitized and stored in separate files."""
    ieeg = r"ieeg", r"Intracranial Electroencephalography", r""
    r"""Intracranial electroencephalography recording data."""
    inplaneT1 = r"inplaneT1", r"Inplane T1", r"arbitrary"
    r"""In arbitrary units (arbitrary).
T1 weighted structural image matched to a functional (task) image."""
    inplaneT2 = r"inplaneT2", r"Inplane T2", r"arbitrary"
    r"""In arbitrary units (arbitrary).
T2 weighted structural image matched to a functional (task) image."""
    m0scan = r"m0scan", r"M0 image", r""
    r"""The M0 image is a calibration image, used to estimate the equilibrium
magnetization of blood."""
    magnitude = r"magnitude", r"Magnitude", r""
    r"""Field-mapping MR schemes such as gradient-recalled echo (GRE) generate a
Magnitude image to be used for anatomical reference.
Requires the existence of Phase, Phase-difference or Fieldmap maps."""
    magnitude1 = r"magnitude1", r"Magnitude", r""
    r"""Magnitude map generated by GRE or similar schemes, associated with the first
echo in the sequence."""
    magnitude2 = r"magnitude2", r"Magnitude", r""
    r"""Magnitude map generated by GRE or similar schemes, associated with the second
echo in the sequence."""
    markers = r"markers", r"MEG Sensor Coil Positions", r""
    r"""Another manufacturer-specific detail pertains to the KIT/Yokogawa/Ricoh
system, which saves the MEG sensor coil positions in a separate file with two
possible filename extensions  (`.sqd`, `.mrk`).
For these files, the `markers` suffix MUST be used.
For example: `sub-01_task-nback_markers.sqd`"""
    mask = r"mask", r"Binary Mask", r""
    r"""A binary mask that functions as a discrete "label" for a single structure.

This suffix may only be used in derivative datasets."""
    meg = r"meg", r"Magnetoencephalography", r""
    r"""Unprocessed MEG data stored in the native file format of the MEG instrument
with which the data was collected."""
    nirs = r"nirs", r"Near Infrared Spectroscopy", r""
    r"""Data associated with a Shared Near Infrared Spectroscopy Format file."""
    optodes = r"optodes", r"Optodes", r""
    r"""Either a light emitting device, sometimes called a transmitter, or a photoelectric transducer, sometimes called a
receiver."""
    pet = r"pet", r"Positron Emission Tomography", r""
    r"""PET imaging data SHOULD be stored in 4D
(or 3D, if only one volume was acquired) NIfTI files with the `_pet` suffix.
Volumes MUST be stored in chronological order
(the order they were acquired in)."""
    phase = r"phase", r"Phase image", r""
    r"""[DEPRECATED](SPEC_ROOT/common-principles.md#definitions).
Phase information associated with magnitude information stored in BOLD
contrast.
This suffix should be replaced by the
[`part-phase`](SPEC_ROOT/appendices/entities.md#part)
in conjunction with the `bold` suffix."""
    phase1 = r"phase1", r"Phase", r""
    r"""Phase map generated by GRE or similar schemes, associated with the first
echo in the sequence."""
    phase2 = r"phase2", r"Phase", r""
    r"""Phase map generated by GRE or similar schemes, associated with the second
echo in the sequence."""
    phasediff = r"phasediff", r"Phase-difference", r""
    r"""Some scanners subtract the `phase1` from the `phase2` map and generate a
unique `phasediff` file.
For instance, this is a common output for the built-in fieldmap sequence of
Siemens scanners."""
    photo = r"photo", r"Photo File", r""
    r"""Photos of the anatomical landmarks, head localization coils or tissue sample."""
    physio = r"physio", r"Physiological recording", r""
    r"""Physiological recordings such as cardiac and respiratory signals."""
    probseg = r"probseg", r"Probabilistic Segmentation", r""
    r"""A probabilistic segmentation.

This suffix may only be used in derivative datasets."""
    sbref = r"sbref", r"Single-band reference image", r""
    r"""Single-band reference for one or more multi-band `dwi` images."""
    scans = r"scans", r"Scans file", r""
    r"""The purpose of this file is to describe timing and other properties of each imaging acquisition
sequence (each run file) within one session.
Each neural recording file SHOULD be described by exactly one row. Some recordings consist of
multiple parts, that span several files, for example through echo-, part-, or split- entities.
Such recordings MUST be documented with one row per file.
Relative paths to files should be used under a compulsory filename header.
If acquisition time is included it should be listed under the acq_time header.
Acquisition time refers to when the first data point in each run was acquired.
Furthermore, if this header is provided, the acquisition times of all files that belong to a
recording MUST be identical.
Datetime should be expressed as described in Units.
Additional fields can include external behavioral measures relevant to the scan.
For example vigilance questionnaire score administered after a resting state scan.
All such included additional fields SHOULD be documented in an accompanying _scans.json file
that describes these fields in detail (see Tabular files)."""
    sessions = r"sessions", r"Sessions file", r""
    r"""In case of multiple sessions there is an option of adding additional sessions.tsv files
describing variables changing between sessions.
In such case one file per participant SHOULD be added.
These files MUST include a session_id column and describe each session by one and only one row.
Column names in sessions.tsv files MUST be different from group level participant key column
names in the participants.tsv file."""
    stim = r"stim", r"Continuous recording", r""
    r"""Continuous measures, such as parameters of a film or audio stimulus."""
    uCT = r"uCT", r"Micro-CT", r""
    r"""Micro-CT imaging data"""

    def __init__(self, literal, display_name_, unit_):
        self.literal_ = literal
        self.display_name_ = display_name_
        self.unit_ = unit_

class EntityEnum(Enum):
    subject = r"sub", r"Subject", r"string", r"label"
    r"""A person or animal participating in the study."""
    session = r"ses", r"Session", r"string", r"label"
    r"""A logical grouping of neuroimaging and behavioral data consistent across subjects.
Session can (but doesn't have to) be synonymous to a visit in a longitudinal study.
In general, subjects will stay in the scanner during one session.
However, for example, if a subject has to leave the scanner room and then
be re-positioned on the scanner bed, the set of MRI acquisitions will still
be considered as a session and match sessions acquired in other subjects.
Similarly, in situations where different data types are obtained over
several visits (for example fMRI on one day followed by DWI the day after)
those can be grouped in one session.

Defining multiple sessions is appropriate when several identical or similar
data acquisitions are planned and performed on all -or most- subjects,
often in the case of some intervention between sessions
(for example, training)."""
    sample = r"sample", r"Sample", r"string", r"label"
    r"""A sample pertaining to a subject such as tissue, primary cell or cell-free sample.
The `sample-<label>` entity is used to distinguish between different samples from the same subject.
The label MUST be unique per subject and is RECOMMENDED to be unique throughout the dataset."""
    task = r"task", r"Task", r"string", r"label"
    r"""A set of structured activities performed by the participant.
Tasks are usually accompanied by stimuli and responses, and can greatly vary in complexity.

In the context of brain scanning, a task is always tied to one data acquisition.
Therefore, even if during one acquisition the subject performed multiple conceptually different behaviors
(with different sets of instructions) they will be considered one (combined) task.

While tasks may be repeated across multiple acquisitions,
a given task may have different sets of stimuli (for example, randomized order) and participant responses
across subjects, sessions, and runs.

The `task-<label>` MUST be consistent across subjects and sessions.

Files with the `task-<label>` entity SHOULD have an associated
[events file](SPEC_ROOT/modality-specific-files/task-events.md#task-events),
as well as certain metadata fields in the associated JSON file.

For the purpose of this specification we consider the so-called "resting state" a task,
although events files are not expected for resting state data.
Additionally, a common convention in the specification is to include the word "rest" in
the `task` label for resting state files (for example, `task-rest`)."""
    acquisition = r"acq", r"Acquisition", r"string", r"label"
    r"""The `acq-<label>` entity corresponds to a custom label the user MAY use to distinguish
a different set of parameters used for acquiring the same modality.

For example, this should be used when a study includes two T1w images -
one full brain low resolution and one restricted field of view but high resolution.
In such case two files could have the following names:
`sub-01_acq-highres_T1w.nii.gz` and `sub-01_acq-lowres_T1w.nii.gz`;
however, the user is free to choose any other label than `highres` and `lowres` as long
as they are consistent across subjects and sessions.

In case different sequences are used to record the same modality
(for example, `RARE` and `FLASH` for T1w)
this field can also be used to make that distinction.
The level of detail at which the distinction is made
(for example, just between `RARE` and `FLASH`, or between `RARE`, `FLASH`, and `FLASHsubsampled`)
remains at the discretion of the researcher."""
    ceagent = r"ce", r"Contrast Enhancing Agent", r"string", r"label"
    r"""The `ce-<label>` entity can be used to distinguish sequences using different contrast enhanced images.
The label is the name of the contrast agent.

This entity represents the `"ContrastBolusIngredient"` metadata field.
Therefore, if the `ce-<label>` entity is present in a filename,
`"ContrastBolusIngredient"` MAY also be added in the JSON file, with the same label."""
    tracer = r"trc", r"Tracer", r"string", r"label"
    r"""The `trc-<label>` entity can be used to distinguish sequences using different tracers.

This entity represents the `"TracerName"` metadata field.
Therefore, if the `trc-<label>` entity is present in a filename,
`"TracerName"` MUST be defined in the associated metadata.
Please note that the `<label>` does not need to match the actual value of the field."""
    stain = r"stain", r"Stain", r"string", r"label"
    r"""The `stain-<label>` key/pair values can be used to distinguish image files
from the same sample using different stains or antibodies for contrast enhancement.

This entity represents the `"SampleStaining"` metadata field.
Therefore, if the `stain-<label>` entity is present in a filename,
`"SampleStaining"` SHOULD be defined in the associated metadata,
although the label may be different.

Descriptions of antibodies SHOULD also be indicated in the `"SamplePrimaryAntibodies"`
and/or `"SampleSecondaryAntobodies"` metadata fields, as appropriate."""
    reconstruction = r"rec", r"Reconstruction", r"string", r"label"
    r"""The `rec-<label>` entity can be used to distinguish different reconstruction algorithms
(for example, `MoCo` for the ones using motion correction)."""
    direction = r"dir", r"Phase-Encoding Direction", r"string", r"label"
    r"""The `dir-<label>` entity can be set to an arbitrary alphanumeric label
(for example, `dir-LR` or `dir-AP`)
to distinguish different phase-encoding directions.

This entity represents the `"PhaseEncodingDirection"` metadata field.
Therefore, if the `dir-<label>` entity is present in a filename,
`"PhaseEncodingDirection"` MUST be defined in the associated metadata.
Please note that the `<label>` does not need to match the actual value of the field."""
    run = r"run", r"Run", r"string", r"index"
    r"""The `run-<index>` entity is used to distinguish separate data acquisitions with the same acquisition parameters
and (other) entities.

If several data acquisitions (for example, MRI scans or EEG recordings)
with the same acquisition parameters are acquired in the same session,
they MUST be indexed with the [`run-<index>`](SPEC_ROOT/appendices/entities.md#run) entity:
`_run-1`, `_run-2`, `_run-3`, and so on
(only nonnegative integers are allowed as run indices).

If different entities apply,
such as a different session indicated by [`ses-<label>`][SPEC_ROOT/appendices/entities.md#ses),
or different acquisition parameters indicated by
[`acq-<label>`](SPEC_ROOT/appendices/entities.md#acq),
then `run` is not needed to distinguish the scans and MAY be omitted."""
    modality = r"mod", r"Corresponding Modality", r"string", r"label"
    r"""The `mod-<label>` entity corresponds to modality label for defacing
masks, for example, T1w, inplaneT1, referenced by a defacemask image.
For example, `sub-01_mod-T1w_defacemask.nii.gz`."""
    echo = r"echo", r"Echo", r"string", r"index"
    r"""If files belonging to an entity-linked file collection are acquired at different
echo times, the `echo-<index>` entity MUST be used to distinguish individual files.

This entity represents the `"EchoTime"` metadata field.
Therefore, if the `echo-<index>` entity is present in a filename,
`"EchoTime"` MUST be defined in the associated metadata.
Please note that the `<index>` denotes the number/index (in the form of a nonnegative integer),
not the `"EchoTime"` value of the separate JSON file."""
    flip = r"flip", r"Flip Angle", r"string", r"index"
    r"""If files belonging to an entity-linked file collection are acquired at different
flip angles, the `_flip-<index>` entity pair MUST be used to distinguish
individual files.

This entity represents the `"FlipAngle"` metadata field.
Therefore, if the `flip-<index>` entity is present in a filename,
`"FlipAngle"` MUST be defined in the associated metadata.
Please note that the `<index>` denotes the number/index (in the form of a nonnegative integer),
not the `"FlipAngle"` value of the separate JSON file."""
    inversion = r"inv", r"Inversion Time", r"string", r"index"
    r"""If files belonging to an entity-linked file collection are acquired at different inversion times,
the `inv-<index>` entity MUST be used to distinguish individual files.

This entity represents the `"InversionTime` metadata field.
Therefore, if the `inv-<index>` entity is present in a filename,
`"InversionTime"` MUST be defined in the associated metadata.
Please note that the `<index>` denotes the number/index (in the form of a nonnegative integer),
not the `"InversionTime"` value of the separate JSON file."""
    mtransfer = r"mt", r"Magnetization Transfer", r"string", r"label"
    r"""If files belonging to an entity-linked file collection are acquired at different
magnetization transfer (MT) states, the `_mt-<label>` entity MUST be used to
distinguish individual files.

This entity represents the `"MTState"` metadata field.
Therefore, if the `mt-<label>` entity is present in a filename,
`"MTState"` MUST be defined in the associated metadata.
Allowed label values for this entity are `on` and `off`,
for images acquired in presence and absence of an MT pulse, respectively."""
    part = r"part", r"Part", r"string", r"label"
    r"""This entity is used to indicate which component of the complex
representation of the MRI signal is represented in voxel data.
The `part-<label>` entity is associated with the DICOM Tag
`0008, 9208`.
Allowed label values for this entity are `phase`, `mag`, `real` and `imag`,
which are typically used in `part-mag`/`part-phase` or
`part-real`/`part-imag` pairs of files.

Phase images MAY be in radians or in arbitrary units.
The sidecar JSON file MUST include the units of the `phase` image.
The possible options are `"rad"` or `"arbitrary"`.

When there is only a magnitude image of a given type, the `part` entity MAY be
omitted."""
    processing = r"proc", r"Processed (on device)", r"string", r"label"
    r"""The proc label is analogous to rec for MR and denotes a variant of
a file that was a result of particular processing performed on the device.

This is useful for files produced in particular by Elekta's MaxFilter
(for example, `sss`, `tsss`, `trans`, `quat` or `mc`),
which some installations impose to be run on raw data because of active
shielding software corrections before the MEG data can actually be
exploited."""
    hemisphere = r"hemi", r"Hemisphere", r"string", r"label"
    r"""The `hemi-<label>` entity indicates which hemibrain is described by the file.
Allowed label values for this entity are `L` and `R`, for the left and right
hemibrains, respectively."""
    space = r"space", r"Space", r"string", r"label"
    r"""The `space-<label>` entity can be used to indicate the way in which electrode positions are interpreted
(for EEG/MEG/iEEG data)
or the spatial reference to which a file has been aligned (for MRI data).
The `<label>` MUST be taken from one of the modality specific lists in the
[Coordinate Systems Appendix](SPEC_ROOT/appendices/coordinate-systems.md).
For example, for iEEG data, the restricted keywords listed under
[iEEG Specific Coordinate Systems](SPEC_ROOT/appendices/coordinate-systems.md#ieeg-specific-coordinate-systems)
are acceptable for `<label>`.

For EEG/MEG/iEEG data, this entity can be applied to raw data,
but for other data types, it is restricted to derivative data."""
    split = r"split", r"Split", r"string", r"index"
    r"""In the case of long data recordings that exceed a file size of 2Gb,
`.fif` files are conventionally split into multiple parts.
Each of these files has an internal pointer to the next file.
This is important when renaming these split recordings to the BIDS convention.

Instead of a simple renaming, files should be read in and saved under their
new names with dedicated tools like [MNE-Python](https://mne.tools/),
which will ensure that not only the file names, but also the internal file pointers, will be updated.

It is RECOMMENDED that `.fif` files with multiple parts use the `split-<index>` entity to indicate each part.
If there are multiple parts of a recording and the optional `scans.tsv` is provided,
all files MUST be listed separately in `scans.tsv` and
the entries for the `acq_time` column in `scans.tsv` MUST all be identical,
as described in [Scans file](SPEC_ROOT/modality-agnostic-files.md#scans-file)."""
    recording = r"recording", r"Recording", r"string", r"label"
    r"""The `recording-<label>` entity can be used to distinguish continuous recording files.

This entity is commonly applied when continuous recordings have different sampling frequencies or start times.
For example, physiological recordings with different sampling frequencies may be distinguished using
labels like `recording-100Hz` and `recording-500Hz`."""
    chunk = r"chunk", r"Chunk", r"string", r"index"
    r"""The `chunk-<index>` key/value pair is used to distinguish between different regions,
2D images or 3D volumes files,
of the same physical sample with different fields of view acquired in the same imaging experiment."""
    atlas = r"atlas", r"Atlas", r"string", r"label"
    r"""The `atlas-<label>` key/value pair corresponds to a custom label the user
MAY use to distinguish a different atlas used for similar type of data.

This entity is only applicable to derivative data."""
    resolution = r"res", r"Resolution", r"string", r"label"
    r"""Resolution of regularly sampled N-dimensional data.

This entity represents the `"Resolution"` metadata field.
Therefore, if the `res-<label>` entity is present in a filename,
`"Resolution"` MUST also be added in the JSON file, to provide interpretation.

This entity is only applicable to derivative data."""
    density = r"den", r"Density", r"string", r"label"
    r"""Density of non-parametric surfaces.

This entity represents the `"Density"` metadata field.
Therefore, if the `den-<label>` entity is present in a filename,
`"Density"` MUST also be added in the JSON file, to provide interpretation.

This entity is only applicable to derivative data."""
    label = r"label", r"Label", r"string", r"label"
    r"""Tissue-type label, following a prescribed vocabulary.
Applies to binary masks and probabilistic/partial volume segmentations
that describe a single tissue type.

This entity is only applicable to derivative data."""
    description = r"desc", r"Description", r"string", r"label"
    r"""When necessary to distinguish two files that do not otherwise have a
distinguishing entity, the `desc-<label>` entity SHOULD be used.

This entity is only applicable to derivative data."""

    def __init__(self, literal, display_name_, type_, format_):
        self.literal_ = literal
        self.display_name_ = display_name_
        self.type_ = type_
        self.format_ = format_

