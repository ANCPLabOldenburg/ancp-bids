from enum import Enum, auto
from typing import List, Union, Dict, Any
from math import inf
import sys

class Model(dict):
    def __init__(self, *args, **kwargs):
        pass

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
    def __init__(self, suffix: 'str' = None, datatype: 'str' = None, entities: 'List[EntityRef]' = None, name: 'str' = None, extension: 'str' = None, uri: 'str' = None):
        super(Artifact, self).__init__(name or None, extension or None, uri or None)
        self['suffix'] = suffix or None
        self['datatype'] = datatype or None
        self['entities'] = entities or []

    @property
    def suffix(self) -> 'str':
        return self['suffix']

    @suffix.setter
    def suffix(self, suffix: 'str'):
        self['suffix'] = suffix
            
    @property
    def datatype(self) -> 'str':
        return self['datatype']

    @datatype.setter
    def datatype(self, datatype: 'str'):
        self['datatype'] = datatype
            
    @property
    def entities(self) -> 'List[EntityRef]':
        return self['entities']

    @entities.setter
    def entities(self, entities: 'List[EntityRef]'):
        self['entities'] = entities
            
    MEMBERS = {
        'suffix': {'type': 'str', 'min': 0, 'max': 1, 'use': 'required', 'meta': {}},
        'datatype': {'type': 'str', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'entities': {'type': 'EntityRef', 'min': 1, 'max': inf, 'use': 'optional', 'meta': {}},
    }


class MetadataArtifact(Artifact):
    def __init__(self, contents: 'Dict' = None, suffix: 'str' = None, datatype: 'str' = None, entities: 'List[EntityRef]' = None, name: 'str' = None, extension: 'str' = None, uri: 'str' = None):
        super(MetadataArtifact, self).__init__(suffix or None, datatype or None, entities or [], name or None, extension or None, uri or None)
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


class MetadataFile(File):
    def __init__(self, contents: 'Dict' = None, name: 'str' = None, extension: 'str' = None, uri: 'str' = None):
        super(MetadataFile, self).__init__(name or None, extension or None, uri or None)
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


class TSVArtifact(Artifact):
    def __init__(self, delimiter: 'str' = None, contents: 'Dict' = None, suffix: 'str' = None, datatype: 'str' = None, entities: 'List[EntityRef]' = None, name: 'str' = None, extension: 'str' = None, uri: 'str' = None):
        super(TSVArtifact, self).__init__(suffix or None, datatype or None, entities or [], name or None, extension or None, uri or None)
        self['delimiter'] = delimiter or None
        self['contents'] = contents or None

    @property
    def delimiter(self) -> 'str':
        return self['delimiter']

    @delimiter.setter
    def delimiter(self, delimiter: 'str'):
        self['delimiter'] = delimiter
            
    @property
    def contents(self) -> 'Dict':
        return self['contents']

    @contents.setter
    def contents(self, contents: 'Dict'):
        self['contents'] = contents
            
    MEMBERS = {
        'delimiter': {'type': 'str', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'contents': {'type': 'dict', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
    }


class TSVFile(File):
    def __init__(self, delimiter: 'str' = None, contents: 'Dict' = None, name: 'str' = None, extension: 'str' = None, uri: 'str' = None):
        super(TSVFile, self).__init__(name or None, extension or None, uri or None)
        self['delimiter'] = delimiter or None
        self['contents'] = contents or None

    @property
    def delimiter(self) -> 'str':
        return self['delimiter']

    @delimiter.setter
    def delimiter(self, delimiter: 'str'):
        self['delimiter'] = delimiter
            
    @property
    def contents(self) -> 'Dict':
        return self['contents']

    @contents.setter
    def contents(self, contents: 'Dict'):
        self['contents'] = contents
            
    MEMBERS = {
        'delimiter': {'type': 'str', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'contents': {'type': 'dict', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
    }


class Folder(Model):
    def __init__(self, name: 'str' = None, files: 'List[File]' = None, folders: 'List[Folder]' = None):
        super(Folder, self).__init__()
        self['name'] = name or None
        self['files'] = files or []
        self['folders'] = folders or []

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
            
    MEMBERS = {
        'name': {'type': 'str', 'min': 0, 'max': 1, 'use': 'required', 'meta': {}},
        'files': {'type': 'File', 'min': 0, 'max': inf, 'use': 'optional', 'meta': {}},
        'folders': {'type': 'Folder', 'min': 0, 'max': inf, 'use': 'optional', 'meta': {}},
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
    def __init__(self, dataset_description: 'DerivativeDatasetDescriptionFile' = None, name: 'str' = None, files: 'List[File]' = None, folders: 'List[Folder]' = None):
        super(DerivativeFolder, self).__init__(name or None, files or [], folders or [])
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


class SessionFolder(Folder):
    def __init__(self, datatypes: 'List[DatatypeFolder]' = None, name: 'str' = None, files: 'List[File]' = None, folders: 'List[Folder]' = None):
        super(SessionFolder, self).__init__(name or None, files or [], folders or [])
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
    def __init__(self, name: 'str' = None, files: 'List[File]' = None, folders: 'List[Folder]' = None):
        super(DatatypeFolder, self).__init__(name or None, files or [], folders or [])

    MEMBERS = {
    }


class Subject(Folder):
    def __init__(self, sessions: 'List[SessionFolder]' = None, datatypes: 'List[DatatypeFolder]' = None, name: 'str' = None, files: 'List[File]' = None, folders: 'List[Folder]' = None):
        super(Subject, self).__init__(name or None, files or [], folders or [])
        self['sessions'] = sessions or []
        self['datatypes'] = datatypes or []

    @property
    def sessions(self) -> 'List[SessionFolder]':
        return self['sessions']

    @sessions.setter
    def sessions(self, sessions: 'List[SessionFolder]'):
        self['sessions'] = sessions
            
    @property
    def datatypes(self) -> 'List[DatatypeFolder]':
        return self['datatypes']

    @datatypes.setter
    def datatypes(self, datatypes: 'List[DatatypeFolder]'):
        self['datatypes'] = datatypes
            
    MEMBERS = {
        'sessions': {'type': 'SessionFolder', 'min': 0, 'max': inf, 'use': 'optional', 'meta': {'name_pattern': 'ses-.*'}},
        'datatypes': {'type': 'DatatypeFolder', 'min': 0, 'max': inf, 'use': 'optional', 'meta': {'name_pattern': '.*'}},
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
        'Version': {'type': 'str', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
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
    def __init__(self, subjects: 'List[Subject]' = None, dataset_description: 'DatasetDescriptionFile' = None, README: 'File' = None, CHANGES: 'File' = None, LICENSE: 'File' = None, genetic_info: 'JsonFile' = None, samples: 'JsonFile' = None, participants_tsv: 'File' = None, participants_json: 'JsonFile' = None, code: 'Folder' = None, derivatives: 'Folder' = None, sourcedata: 'Folder' = None, stimuli: 'Folder' = None, name: 'str' = None, files: 'List[File]' = None, folders: 'List[Folder]' = None):
        super(Dataset, self).__init__(name or None, files or [], folders or [])
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
        'participants_tsv': {'type': 'File', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {'name_pattern': 'participants.tsv'}},
        'participants_json': {'type': 'JsonFile', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {'name_pattern': 'participants.json'}},
        'code': {'type': 'Folder', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'derivatives': {'type': 'Folder', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'sourcedata': {'type': 'Folder', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
        'stimuli': {'type': 'Folder', 'min': 0, 'max': 1, 'use': 'optional', 'meta': {}},
    }


class DatatypeEnum(Enum):
 pass
class ModalityEnum(Enum):
 pass
class SuffixEnum(Enum):
 pass
class EntityEnum(Enum):
 pass
