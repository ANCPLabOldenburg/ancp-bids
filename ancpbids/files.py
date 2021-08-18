import os
import fnmatch
import logging

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


def load_contents(file_path):
    if not os.path.exists(file_path):
        return None
    reader = None
    file_name = os.path.basename(file_path)
    parts = os.path.splitext(file_name)
    if len(parts) > 1:
        extension = parts[-1][1:]
        if extension in FILE_READERS:
            reader = FILE_READERS[extension]
    if reader is None:
        logger.debug("No reader found for file '%s', defaulting to 'txt' file reader" % file_name)
        reader = FILE_READERS['txt']
    return reader(file_path)


def get_files(dir_path: str, include_folders: bool = False, fnmatch_pattern=None):
    files = os.listdir(dir_path)
    files = list(map(lambda file: os.path.normpath(dir_path + "/" + file), files))
    files = sorted(files)
    if not include_folders:
        files = list(filter(lambda file: not os.path.isdir(file), files))
    if fnmatch_pattern:
        files = list(filter(lambda file: fnmatch.fnmatch(os.path.basename(file), fnmatch_pattern), files))
    return files
