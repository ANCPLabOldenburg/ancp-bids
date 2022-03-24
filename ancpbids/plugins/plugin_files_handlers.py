from ancpbids.plugin import FileHandlerPlugin


def read_yaml(file_path: str):
    import yaml
    with open(file_path, 'r') as stream:
        try:
            return yaml.load(stream, Loader=yaml.FullLoader)
        except:
            return None


def read_json(file_path: str):
    # we cannot use yaml to load json if it contains any TABs for indentation
    import json
    with open(file_path, 'r') as stream:
        try:
            return json.load(stream)
        except:
            return None


def read_plain_text(file_path: str):
    with open(file_path, 'r') as file:
        return file.readlines()


def read_tsv(file_path: str):
    import numpy
    df = numpy.genfromtxt(file_path, delimiter='\t', dtype=None, names=True)
    return df


def write_json(file_path: str, contents: dict):
    """Writes the contents as a .json file to the given file path.

    Parameters
    ----------
    file_path:
        The path to the file to store the contents to.
    contents:
        The contents of the target .json file.

    """
    import json
    with open(file_path, 'w') as fp:
        json.dump(contents, fp)

def write_txt(file_path: str, contents: dict):
    """Writes the contents as a .txt file to the given file path.

    Parameters
    ----------
    file_path:
        The path to the file to store the contents to.
    contents:
        The contents of the target .txt file.

    """
    with open(file_path, 'w') as fp:
        fp.write(str(contents))


class FilesHandlerPlugin(FileHandlerPlugin):
    def execute(self, file_readers_registry, file_writers_registry):
        file_readers_registry['yaml'] = read_yaml
        file_readers_registry['json'] = read_json
        file_readers_registry['txt'] = read_plain_text
        file_readers_registry['tsv'] = read_tsv

        file_writers_registry['json'] = write_json
        file_writers_registry['txt'] = write_txt
