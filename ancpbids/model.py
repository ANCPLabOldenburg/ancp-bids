from enum import Enum
from typing import List, Union, Dict, Any

class Model(dict):
    pass

class MetadataFieldDefinition(Model):
    def __init__(self):
        super(MetadataFieldDefinition, self).__init__()
        self['name']: str = None
        self['description']: str = None
        self['type']: Dict = {}

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
            
    MEMBERS = {'name': {'type': 'str', 'list': False, 'kwargs': {}}, 'description': {'type': 'str', 'list': False, 'kwargs': {}}, 'type': {'type': 'Dict', 'list': False, 'kwargs': {}}}


class EntitiyDefinition(Model):
    def __init__(self):
        super(EntitiyDefinition, self).__init__()
        self['key']: str = None
        self['name']: str = None
        self['entity']: str = None
        self['description']: str = None
        self['type']: Dict = {}

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
            
    MEMBERS = {'key': {'type': 'str', 'list': False, 'kwargs': {}}, 'name': {'type': 'str', 'list': False, 'kwargs': {}}, 'entity': {'type': 'str', 'list': False, 'kwargs': {}}, 'description': {'type': 'str', 'list': False, 'kwargs': {}}, 'type': {'type': 'Dict', 'list': False, 'kwargs': {}}}


class SuffixDefinition(Model):
    def __init__(self):
        super(SuffixDefinition, self).__init__()
        self['name']: str = None
        self['description']: str = None
        self['type']: Dict = {}

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
            
    MEMBERS = {'name': {'type': 'str', 'list': False, 'kwargs': {}}, 'description': {'type': 'str', 'list': False, 'kwargs': {}}, 'type': {'type': 'Dict', 'list': False, 'kwargs': {}}}


class File(Model):
    def __init__(self):
        super(File, self).__init__()
        self['name']: str = None
        self['extension']: str = None
        self['uri']: str = None

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
            
    MEMBERS = {'name': {'type': 'str', 'list': False, 'kwargs': {}}, 'extension': {'type': 'str', 'list': False, 'kwargs': {}}, 'uri': {'type': 'str', 'list': False, 'kwargs': {}}}


class Folder(Model):
    def __init__(self):
        super(Folder, self).__init__()
        self['name']: str = None
        self['files']: List[File] = []
        self['folders']: List[Folder] = []

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
            
    MEMBERS = {'name': {'type': 'str', 'list': False, 'kwargs': {}}, 'files': {'type': 'File', 'list': True, 'kwargs': {}}, 'folders': {'type': 'Folder', 'list': True, 'kwargs': {}}}


class JsonFile(File):
    def __init__(self):
        super(JsonFile, self).__init__()
        self['contents']: Dict = {}

    @property
    def contents(self) -> 'Dict':
        return self['contents']
    
    @contents.setter
    def contents(self, contents: 'Dict'):
        self['contents'] = contents
            
    MEMBERS = {'contents': {'type': 'Dict', 'list': False, 'kwargs': {}}}


class EntityRef(Model):
    def __init__(self):
        super(EntityRef, self).__init__()
        self['key']: str = None
        self['value']: str = None

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
            
    MEMBERS = {'key': {'type': 'str', 'list': False, 'kwargs': {}}, 'value': {'type': 'str', 'list': False, 'kwargs': {}}}


class Artifact(File):
    """An artifact is a file whose name conforms to the BIDS file naming convention."""
    def __init__(self):
        super(Artifact, self).__init__()
        self['suffix']: str = None
        self['entities']: List[EntityRef] = []

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
            
    MEMBERS = {'suffix': {'type': 'str', 'list': False, 'kwargs': {}}, 'entities': {'type': 'EntityRef', 'list': True, 'kwargs': {}}}


class DatasetDescriptionFile(JsonFile):
    def __init__(self):
        super(DatasetDescriptionFile, self).__init__()
        self['Name']: str = None
        self['BIDSVersion']: str = None
        self['HEDVersion']: str = None
        self['DatasetType']: Enum = None
        self['License']: str = None
        self['Acknowledgements']: str = None
        self['HowToAcknowledge']: str = None
        self['DatasetDOI']: str = None
        self['Authors']: List[str] = []
        self['Funding']: List[str] = []
        self['EthicsApprovals']: List[str] = []
        self['ReferencesAndLinks']: List[str] = []

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
    def DatasetType(self) -> 'Enum':
        return self['DatasetType']
    
    @DatasetType.setter
    def DatasetType(self, DatasetType: 'Enum'):
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
            
    MEMBERS = {'Name': {'type': 'str', 'list': False, 'kwargs': {}}, 'BIDSVersion': {'type': 'str', 'list': False, 'kwargs': {}}, 'HEDVersion': {'type': 'str', 'list': False, 'kwargs': {'recommended': True}}, 'DatasetType': {'type': 'Enum', 'list': False, 'kwargs': {'recommended': True}}, 'License': {'type': 'str', 'list': False, 'kwargs': {'recommended': True}}, 'Acknowledgements': {'type': 'str', 'list': False, 'kwargs': {}}, 'HowToAcknowledge': {'type': 'str', 'list': False, 'kwargs': {}}, 'DatasetDOI': {'type': 'str', 'list': False, 'kwargs': {}}, 'Authors': {'type': 'str', 'list': True, 'kwargs': {}}, 'Funding': {'type': 'str', 'list': True, 'kwargs': {}}, 'EthicsApprovals': {'type': 'str', 'list': True, 'kwargs': {}}, 'ReferencesAndLinks': {'type': 'str', 'list': True, 'kwargs': {}}}


class DerivativeDatasetDescriptionFile(DatasetDescriptionFile):
    def __init__(self):
        super(DerivativeDatasetDescriptionFile, self).__init__()
        self['GeneratedBy']: List[GeneratedBy] = []
        self['SourceDatasets']: List[SourceDatasets] = []

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
            
    MEMBERS = {'GeneratedBy': {'type': 'GeneratedBy', 'list': True, 'kwargs': {}}, 'SourceDatasets': {'type': 'SourceDatasets', 'list': True, 'kwargs': {'recommended': True}}}


class DerivativeFolder(Folder):
    def __init__(self):
        super(DerivativeFolder, self).__init__()
        self['dataset_description']: DerivativeDatasetDescriptionFile = None
        self['derivatives']: List[DerivativeFolder] = []

    @property
    def dataset_description(self) -> 'DerivativeDatasetDescriptionFile':
        return self['dataset_description']
    
    @dataset_description.setter
    def dataset_description(self, dataset_description: 'DerivativeDatasetDescriptionFile'):
        self['dataset_description'] = dataset_description
            
    @property
    def derivatives(self) -> 'List[DerivativeFolder]':
        return self['derivatives']
    
    @derivatives.setter
    def derivatives(self, derivatives: 'List[DerivativeFolder]'):
        self['derivatives'] = derivatives
            
    MEMBERS = {'dataset_description': {'type': 'DerivativeDatasetDescriptionFile', 'list': False, 'kwargs': {}}, 'derivatives': {'type': 'DerivativeFolder', 'list': True, 'kwargs': {}}}


class Session(Folder):
    def __init__(self):
        super(Session, self).__init__()
        self['datatypes']: List[DatatypeFolder] = []

    @property
    def datatypes(self) -> 'List[DatatypeFolder]':
        return self['datatypes']
    
    @datatypes.setter
    def datatypes(self, datatypes: 'List[DatatypeFolder]'):
        self['datatypes'] = datatypes
            
    MEMBERS = {'datatypes': {'type': 'DatatypeFolder', 'list': True, 'kwargs': {}}}


class DatatypeFolder(Folder):
    def __init__(self):
        super(DatatypeFolder, self).__init__()
        self['artifacts']: List[Artifact] = []

    @property
    def artifacts(self) -> 'List[Artifact]':
        return self['artifacts']
    
    @artifacts.setter
    def artifacts(self, artifacts: 'List[Artifact]'):
        self['artifacts'] = artifacts
            
    MEMBERS = {'artifacts': {'type': 'Artifact', 'list': True, 'kwargs': {}}}


class Subject(Folder):
    def __init__(self):
        super(Subject, self).__init__()
        self['datatypes']: List[DatatypeFolder] = []
        self['sessions']: List[Session] = []

    @property
    def datatypes(self) -> 'List[DatatypeFolder]':
        return self['datatypes']
    
    @datatypes.setter
    def datatypes(self, datatypes: 'List[DatatypeFolder]'):
        self['datatypes'] = datatypes
            
    @property
    def sessions(self) -> 'List[Session]':
        return self['sessions']
    
    @sessions.setter
    def sessions(self, sessions: 'List[Session]'):
        self['sessions'] = sessions
            
    MEMBERS = {'datatypes': {'type': 'DatatypeFolder', 'list': True, 'kwargs': {}}, 'sessions': {'type': 'Session', 'list': True, 'kwargs': {'name_pattern': 'ses-.*'}}}


class GeneratedBy(Model):
    def __init__(self):
        super(GeneratedBy, self).__init__()
        self['Name']: str = None
        self['Version']: str = None
        self['Description']: str = None
        self['CodeURL']: str = None
        self['Container']: List[GeneratedByContainer] = []

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
            
    MEMBERS = {'Name': {'type': 'str', 'list': False, 'kwargs': {}}, 'Version': {'type': 'str', 'list': False, 'kwargs': {'recommended': True}}, 'Description': {'type': 'str', 'list': False, 'kwargs': {}}, 'CodeURL': {'type': 'str', 'list': False, 'kwargs': {}}, 'Container': {'type': 'GeneratedByContainer', 'list': True, 'kwargs': {}}}


class SourceDatasets(Model):
    def __init__(self):
        super(SourceDatasets, self).__init__()
        self['DOI']: str = None
        self['URL']: str = None
        self['Version']: str = None

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
            
    MEMBERS = {'DOI': {'type': 'str', 'list': False, 'kwargs': {}}, 'URL': {'type': 'str', 'list': False, 'kwargs': {}}, 'Version': {'type': 'str', 'list': False, 'kwargs': {}}}


class GeneratedByContainer(Model):
    def __init__(self):
        super(GeneratedByContainer, self).__init__()
        self['Type']: str = None
        self['Tag']: str = None
        self['URI']: str = None

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
            
    MEMBERS = {'Type': {'type': 'str', 'list': False, 'kwargs': {}}, 'Tag': {'type': 'str', 'list': False, 'kwargs': {}}, 'URI': {'type': 'str', 'list': False, 'kwargs': {}}}


class ParticipantsTsvFile(Model):
    def __init__(self):
        super(ParticipantsTsvFile, self).__init__()
        self['entries']: List[ParticipantsTsvFilEentry] = []

    @property
    def entries(self) -> 'List[ParticipantsTsvFilEentry]':
        return self['entries']
    
    @entries.setter
    def entries(self, entries: 'List[ParticipantsTsvFilEentry]'):
        self['entries'] = entries
            
    MEMBERS = {'entries': {'type': 'ParticipantsTsvFilEentry', 'list': True, 'kwargs': {}}}


class ParticipantsTsvFilEentry(Model):
    def __init__(self):
        super(ParticipantsTsvFilEentry, self).__init__()
        self['participant_id']: str = None
        self['age']: float = None
        self['sex']: Enum = None
        self['handedness']: Enum = None

    @property
    def participant_id(self) -> 'str':
        return self['participant_id']
    
    @participant_id.setter
    def participant_id(self, participant_id: 'str'):
        self['participant_id'] = participant_id
            
    @property
    def age(self) -> 'float':
        return self['age']
    
    @age.setter
    def age(self, age: 'float'):
        self['age'] = age
            
    @property
    def sex(self) -> 'Enum':
        return self['sex']
    
    @sex.setter
    def sex(self, sex: 'Enum'):
        self['sex'] = sex
            
    @property
    def handedness(self) -> 'Enum':
        return self['handedness']
    
    @handedness.setter
    def handedness(self, handedness: 'Enum'):
        self['handedness'] = handedness
            
    MEMBERS = {'participant_id': {'type': 'str', 'list': False, 'kwargs': {}}, 'age': {'type': 'float', 'list': False, 'kwargs': {}}, 'sex': {'type': 'Enum', 'list': False, 'kwargs': {}}, 'handedness': {'type': 'Enum', 'list': False, 'kwargs': {}}}


class TsvSidecarFile(Model):
    def __init__(self):
        super(TsvSidecarFile, self).__init__()
        self['columns']: List[SidecarColumnDescriptor] = []

    @property
    def columns(self) -> 'List[SidecarColumnDescriptor]':
        return self['columns']
    
    @columns.setter
    def columns(self, columns: 'List[SidecarColumnDescriptor]'):
        self['columns'] = columns
            
    MEMBERS = {'columns': {'type': 'SidecarColumnDescriptor', 'list': True, 'kwargs': {}}}


class SidecarColumnDescriptor(Model):
    def __init__(self):
        super(SidecarColumnDescriptor, self).__init__()
        self['Name']: str = None
        self['LongName']: str = None
        self['Description']: str = None
        self['Units']: str = None
        self['TermURL']: str = None
        self['Levels']: List[KeyValuePair] = []

    @property
    def Name(self) -> 'str':
        return self['Name']
    
    @Name.setter
    def Name(self, Name: 'str'):
        self['Name'] = Name
            
    @property
    def LongName(self) -> 'str':
        return self['LongName']
    
    @LongName.setter
    def LongName(self, LongName: 'str'):
        self['LongName'] = LongName
            
    @property
    def Description(self) -> 'str':
        return self['Description']
    
    @Description.setter
    def Description(self, Description: 'str'):
        self['Description'] = Description
            
    @property
    def Units(self) -> 'str':
        return self['Units']
    
    @Units.setter
    def Units(self, Units: 'str'):
        self['Units'] = Units
            
    @property
    def TermURL(self) -> 'str':
        return self['TermURL']
    
    @TermURL.setter
    def TermURL(self, TermURL: 'str'):
        self['TermURL'] = TermURL
            
    @property
    def Levels(self) -> 'List[KeyValuePair]':
        return self['Levels']
    
    @Levels.setter
    def Levels(self, Levels: 'List[KeyValuePair]'):
        self['Levels'] = Levels
            
    MEMBERS = {'Name': {'type': 'str', 'list': False, 'kwargs': {}}, 'LongName': {'type': 'str', 'list': False, 'kwargs': {}}, 'Description': {'type': 'str', 'list': False, 'kwargs': {}}, 'Units': {'type': 'str', 'list': False, 'kwargs': {}}, 'TermURL': {'type': 'str', 'list': False, 'kwargs': {}}, 'Levels': {'type': 'KeyValuePair', 'list': True, 'kwargs': {}}}


class KeyValuePair(Model):
    def __init__(self):
        super(KeyValuePair, self).__init__()
        self['key']: str = None
        self['value']: str = None

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
            
    MEMBERS = {'key': {'type': 'str', 'list': False, 'kwargs': {}}, 'value': {'type': 'str', 'list': False, 'kwargs': {}}}


class Dataset(Folder):
    def __init__(self):
        super(Dataset, self).__init__()
        self['subjects']: List[Subject] = []
        self['dataset_description']: DatasetDescriptionFile = None
        self['README']: File = None
        self['CHANGES']: File = None
        self['LICENSE']: File = None
        self['genetic_info']: JsonFile = None
        self['samples']: JsonFile = None
        self['participants_tsv']: ParticipantsTsvFile = None
        self['participants_json']: TsvSidecarFile = None
        self['code']: Folder = None
        self['derivatives']: DerivativeFolder = None
        self['sourcedata']: Folder = None
        self['stimuli']: Folder = None

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
    def participants_tsv(self) -> 'ParticipantsTsvFile':
        return self['participants_tsv']
    
    @participants_tsv.setter
    def participants_tsv(self, participants_tsv: 'ParticipantsTsvFile'):
        self['participants_tsv'] = participants_tsv
            
    @property
    def participants_json(self) -> 'TsvSidecarFile':
        return self['participants_json']
    
    @participants_json.setter
    def participants_json(self, participants_json: 'TsvSidecarFile'):
        self['participants_json'] = participants_json
            
    @property
    def code(self) -> 'Folder':
        return self['code']
    
    @code.setter
    def code(self, code: 'Folder'):
        self['code'] = code
            
    @property
    def derivatives(self) -> 'DerivativeFolder':
        return self['derivatives']
    
    @derivatives.setter
    def derivatives(self, derivatives: 'DerivativeFolder'):
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
            
    MEMBERS = {'subjects': {'type': 'Subject', 'list': True, 'kwargs': {'name_pattern': 'sub-.*'}}, 'dataset_description': {'type': 'DatasetDescriptionFile', 'list': False, 'kwargs': {}}, 'README': {'type': 'File', 'list': False, 'kwargs': {}}, 'CHANGES': {'type': 'File', 'list': False, 'kwargs': {}}, 'LICENSE': {'type': 'File', 'list': False, 'kwargs': {}}, 'genetic_info': {'type': 'JsonFile', 'list': False, 'kwargs': {}}, 'samples': {'type': 'JsonFile', 'list': False, 'kwargs': {}}, 'participants_tsv': {'type': 'ParticipantsTsvFile', 'list': False, 'kwargs': {}}, 'participants_json': {'type': 'TsvSidecarFile', 'list': False, 'kwargs': {}}, 'code': {'type': 'Folder', 'list': False, 'kwargs': {}}, 'derivatives': {'type': 'DerivativeFolder', 'list': False, 'kwargs': {}}, 'sourcedata': {'type': 'Folder', 'list': False, 'kwargs': {}}, 'stimuli': {'type': 'Folder', 'list': False, 'kwargs': {}}}


YAMALE_SCHEMA = """
Dataset:
  subjects: list(include('Subject'), required=False, name_pattern='sub-.*')
  dataset_description: include('DatasetDescriptionFile')
  README: include('File', required=False)
  CHANGES: include('File', required=False)
  LICENSE: include('File', required=False)
  genetic_info: include('JsonFile', required=False)
  samples: include('JsonFile', required=False)
  participants_tsv: include('ParticipantsTsvFile', required=False)
  participants_json: include('TsvSidecarFile', required=False)
  code: include('Folder', required=False)
  derivatives: include('DerivativeFolder', required=False)
  sourcedata: include('Folder', required=False)
  stimuli: include('Folder', required=False)
  name: str()
  files: list(include('File'), required=False)
  folders: list(include('Folder'), required=False)
---
MetadataFieldDefinition:
  name: str()
  description: str()
  type: map(required=False)
EntitiyDefinition:
  key: str()
  name: str()
  entity: str()
  description: str()
  type: map(required=False)
SuffixDefinition:
  name: str()
  description: str()
  type: map(required=False)
File:
  name: str()
  extension: str(required=False)
  uri: str(required=False)
Folder:
  name: str()
  files: list(include('File'), required=False)
  folders: list(include('Folder'), required=False)
JsonFile:
  contents: map(required=False)
  name: str()
  extension: str(required=False)
  uri: str(required=False)
EntityRef:
  key: str()
  value: str()
Artifact:
  suffix: str()
  entities: list(include('EntityRef'))
  name: str()
  extension: str(required=False)
  uri: str(required=False)
DatasetDescriptionFile:
  Name: str()
  BIDSVersion: str()
  HEDVersion: str(required=False, recommended=True)
  DatasetType: enum('raw', 'derivative', required=False, recommended=True)
  License: str(required=False, recommended=True)
  Acknowledgements: str(required=False)
  HowToAcknowledge: str(required=False)
  DatasetDOI: str(required=False)
  Authors: list(str(), required=False)
  Funding: list(str(), required=False)
  EthicsApprovals: list(str(), required=False)
  ReferencesAndLinks: list(str(), required=False)
  contents: map(required=False)
  name: str()
  extension: str(required=False)
  uri: str(required=False)
DerivativeDatasetDescriptionFile:
  GeneratedBy: list(include('GeneratedBy'))
  SourceDatasets: list(include('SourceDatasets'), required=False, recommended=True)
  Name: str()
  BIDSVersion: str()
  HEDVersion: str(required=False, recommended=True)
  DatasetType: enum('raw', 'derivative', required=False, recommended=True)
  License: str(required=False, recommended=True)
  Acknowledgements: str(required=False)
  HowToAcknowledge: str(required=False)
  DatasetDOI: str(required=False)
  Authors: list(str(), required=False)
  Funding: list(str(), required=False)
  EthicsApprovals: list(str(), required=False)
  ReferencesAndLinks: list(str(), required=False)
  contents: map(required=False)
  name: str()
  extension: str(required=False)
  uri: str(required=False)
DerivativeFolder:
  dataset_description: include('DerivativeDatasetDescriptionFile', required=False)
  derivatives: list(include('DerivativeFolder'), required=False)
  name: str()
  files: list(include('File'), required=False)
  folders: list(include('Folder'), required=False)
Session:
  datatypes: list(include('DatatypeFolder'), required=False)
  name: str()
  files: list(include('File'), required=False)
  folders: list(include('Folder'), required=False)
DatatypeFolder:
  artifacts: list(include('Artifact'), required=False)
  name: str()
  files: list(include('File'), required=False)
  folders: list(include('Folder'), required=False)
Subject:
  datatypes: list(include('DatatypeFolder', required=False))
  sessions: list(include('Session'), required=False, name_pattern='ses-.*')
  name: str()
  files: list(include('File'), required=False)
  folders: list(include('Folder'), required=False)
GeneratedBy:
  Name: str()
  Version: str(required=False, recommended=True)
  Description: str(required=False)
  CodeURL: str(required=False)
  Container: list(include('GeneratedByContainer'), required=False)
SourceDatasets:
  DOI: str()
  URL: str()
  Version: str()
GeneratedByContainer:
  Type: str(required=False)
  Tag: str(required=False)
  URI: str(required=False)
ParticipantsTsvFile:
  entries: list(include('ParticipantsTsvFilEentry'))
ParticipantsTsvFilEentry:
  participant_id: str()
  age: num(required=False)
  sex: enum('m', 'M', 'male', 'Male', 'MALE', 'f', 'F', 'female', 'Female', 'FEMALE',
    'o', 'O', 'other', 'Other', 'OTHER', required=False)
  handedness: enum('l', 'L', 'Left', 'LEFT', 'r', 'R', 'Right', 'RIGHT', 'ambidextrous',
    'AMBIDEXTROUS', 'Ambidextrous', required=False)
TsvSidecarFile:
  columns: list(include('SidecarColumnDescriptor'))
SidecarColumnDescriptor:
  Name: str()
  LongName: str(required=False)
  Description: str(required=False)
  Units: str(required=False)
  TermURL: str(required=False)
  Levels: list(include('KeyValuePair'), required=False)
KeyValuePair:
  key: str()
  value: str()
"""
