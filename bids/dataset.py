from .files import File, Folder


class Dataset:
    def __init__(self, dir_path):
        self.folder = Folder(dir_path)
        self.subjects = None
        self.name = self.folder.name()

    def get_subjects(self, force_refresh=False):
        if self.subjects is None or force_refresh:
            files = self.folder.get_files(force_refresh)
            subject_folders = filter(lambda file: isinstance(file, Folder) and file.name().startswith("sub-"), files)
            self.subjects = list(map(lambda folder: Subject(folder), subject_folders))
        return self.subjects


class Subject:
    def __init__(self, folder: Folder):
        self.folder = folder
        self.sessions = None
        self.name = self.folder.name()

    def get_sessions(self, force_refresh=False):
        if self.sessions is None or force_refresh:
            files = self.folder.get_files(force_refresh)
            session_folders = filter(lambda file: isinstance(file, Folder) and file.name().startswith("ses-"), files)
            self.sessions = list(map(lambda folder: Session(folder), session_folders))
        # if no sessions available, assume it is a single session dataset
        # and create a dummy session
        if len(self.sessions) == 0:
            self.sessions = [Session(self.folder, "ses-01")]
        return self.sessions


class Session:
    def __init__(self, folder: Folder, name: str = None):
        self.folder = folder
        self.datatypes = None
        self.name = name if name is not None else self.folder.name()

    def get_datatypes(self, force_refresh=False):
        if self.datatypes is None or force_refresh:
            files = self.folder.get_files(force_refresh)
            datatype_folders = filter(lambda file: isinstance(file, Folder), files)
            self.datatypes = list(map(lambda folder: Datatype(folder), datatype_folders))
        return self.datatypes


class Artifact:
    def __init__(self, file: File, name: str = None):
        self.file = file
        self.name = name if name is not None else self.file.name()

    def get_entities(self):
        pass


class Datatype:
    def __init__(self, folder: Folder, name: str = None):
        self.folder = folder
        self.name = name if name is not None else self.folder.name()

    def get_artifacts(self, force_refresh=False):
        files = self.folder.get_files(force_refresh, include_folders=False)
        return list(map(lambda file: Artifact(file), files))
