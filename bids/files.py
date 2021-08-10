import os
import logging
import fnmatch

logger = logging.getLogger(__file__)


def read_yaml(file_path: str):
    import yaml
    with open(file_path, 'r') as stream:
        try:
            return yaml.load(stream, Loader=yaml.FullLoader)
        except:
            return None


def read_json(file_path: str):
    # json is a subset of yaml, so, use the yaml reader
    return read_yaml(file_path)


def read_plain_text(file_path: str):
    with open(file_path, 'r') as file:
        return file.readlines()


def read_tsv(file_path: str):
    import pandas
    df = pandas.read_csv(file_path, sep='\t')
    return df


FILE_READERS = {
    'yaml': read_yaml,
    'json': read_json,
    'txt': read_plain_text,
    'tsv': read_tsv,
}


class File:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def name(self):
        return os.path.basename(self.file_path)

    def load_contents(self):
        reader = None
        file_name = self.name()
        parts = os.path.splitext(file_name)
        if len(parts) > 1:
            extension = parts[-1][1:]
            if extension in FILE_READERS:
                reader = FILE_READERS[extension]
        if reader is None:
            logger.debug("No reader found for file '%s', defaulting to 'txt' file reader" % file_name)
            reader = FILE_READERS['txt']
        return reader(self.file_path)


class Folder:
    def __init__(self, dir_path: str):
        self.dir_path = dir_path
        self.files = None

    def name(self):
        return os.path.basename(self.dir_path)

    def get_files(self, force_refresh: bool = False, include_folders: bool = True, fnmatch_pattern=None):
        if self.files is None or force_refresh:
            self.files = os.listdir(self.dir_path)
            self.files = list(map(lambda file: os.path.normpath(self.dir_path + "/" + file), self.files))
            self.files = sorted(self.files)
            self.files = list(map(lambda file: File(file) if not os.path.isdir(file) else Folder(file), self.files))
        files = self.files
        if not include_folders:
            files = list(filter(lambda file: not isinstance(file, Folder), files))
        if fnmatch_pattern:
            files = list(filter(lambda file: fnmatch.fnmatch(file.name(), fnmatch_pattern), files))
        return files

    def load_file(self, relative_name):
        file_path = os.path.join(self.dir_path, relative_name)
        file = File(file_path)
        return file.load_contents()
