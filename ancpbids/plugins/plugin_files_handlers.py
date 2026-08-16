from typing import Optional

from ancpbids.plugin import FileHandlerPlugin, hook


def read_yaml(file_path: str, **kwargs):
    import yaml
    with open(file_path, 'r') as stream:
        try:
            return yaml.load(stream, Loader=yaml.FullLoader)
        except:
            return None


def read_json(file_path: str, **kwargs):
    # we cannot use yaml to load json if it contains any TABs for indentation
    import json
    with open(file_path, 'r') as stream:
        try:
            return json.load(stream)
        except:
            return None


def read_plain_text(file_path: str, **kwargs):
    with open(file_path, 'r') as file:
        return file.readlines()


def read_tsv(file_path: str, return_type: Optional[str] = None, **kwargs):
    if return_type == "ndarray":
        import numpy

        return numpy.genfromtxt(
            file_path, delimiter='\t', dtype=None, names=True
        )
    elif return_type == "dataframe":
        import pandas

        return pandas.read_csv(file_path, delimiter='\t')
    else:
        import csv

        with open(file_path) as f:
            return list(csv.DictReader(f, dialect="excel-tab"))


def write_json(file_path: str, contents: dict, **kwargs):
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
        json.dump(contents, fp, indent=2)


def write_tsv(file_path: str, contents, **kwargs):
    """Writes tabular contents as a BIDS ``.tsv`` (tab-separated) file.

    Parameters
    ----------
    file_path:
        The path to the file to store the contents to.
    contents:
        One of:
        * ``str`` — written as-is (a trailing newline is added if missing)
        * ``list[dict]`` — rows written with ``csv.DictWriter`` (excel-tab)
        * a pandas ``DataFrame`` — written via ``DataFrame.to_csv``

    """
    if isinstance(contents, str):
        with open(file_path, 'w', newline='') as fp:
            fp.write(contents)
            if contents and not contents.endswith('\n'):
                fp.write('\n')
        return

    if hasattr(contents, 'to_csv') and hasattr(contents, 'columns'):
        contents.to_csv(file_path, sep='\t', index=False)
        return

    if isinstance(contents, list):
        import csv
        if not contents:
            with open(file_path, 'w', newline='') as fp:
                pass
            return
        if not isinstance(contents[0], dict):
            raise TypeError(
                "write_tsv list contents must be a list of dict rows, "
                f"got list of {type(contents[0]).__name__}"
            )
        fieldnames = list(contents[0].keys())
        with open(file_path, 'w', newline='') as fp:
            writer = csv.DictWriter(
                fp,
                fieldnames=fieldnames,
                delimiter='\t',
                lineterminator='\n',
                extrasaction='ignore',
            )
            writer.writeheader()
            writer.writerows(contents)
        return

    raise TypeError(
        "write_tsv expects str, list[dict], or pandas DataFrame, "
        f"got {type(contents).__name__}"
    )


def write_txt(file_path: str, contents: dict, **kwargs):
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


@hook(ranking=0, system=True)
class FilesHandlerPlugin(FileHandlerPlugin):
    def execute(self, file_readers_registry, file_writers_registry):
        file_readers_registry['yaml'] = read_yaml
        file_readers_registry['json'] = read_json
        file_readers_registry['txt'] = read_plain_text
        file_readers_registry['tsv'] = read_tsv

        file_writers_registry['json'] = write_json
        file_writers_registry['tsv'] = write_tsv
        file_writers_registry['txt'] = write_txt
