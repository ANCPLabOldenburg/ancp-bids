import logging
import os

FILE_READERS = {}
FILE_WRITERS = {}

LOGGER = logging.getLogger(__file__)


def load_contents(file_path):
    """Loads the contents of the provided file path.

    Parameters
    ----------
    file_path :
        the file path to load contents from

    Returns
    -------
        The result depends on the extension of the file name.
        For example, a .json file may be returned as an ordinary Python dict or a .txt as a str value.

    """
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
        LOGGER.debug("No reader found for file '%s', defaulting to 'txt' file reader" % file_name)
        reader = FILE_READERS['txt']
    if reader is None:
        raise ValueError('No file reader registered to load file %s' % file_path)
    return reader(file_path)


def write_contents(file_path: str, contents):
    """Writes the provided contents to the target file path using a registered file writer.

    A valid file writer may be inferred by the file's extension and/or the given contents object.
    If no file writer is found for the given file, a `ValueError` is raised.

    Parameters
    ----------
    file_path:
        The file path to write to.
    contents:
        The contents to write to the target file.

    """
    writer = None
    parts = os.path.splitext(file_path)
    if len(parts) > 1:
        extension = parts[-1][1:]
        if extension in FILE_WRITERS:
            writer = FILE_WRITERS[extension]

    if not writer:
        raise ValueError("No file writer registered for file: %s" % file_path)

    writer(file_path, contents)


def deepupdate(target, src):
    """Deep update target dict with src
    For each k,v in src: if k doesn't exist in target, it is deep copied from
    src to target. Otherwise, if v is a list, target[k] is extended with
    src[k]. If v is a set, target[k] is updated with v, If v is a dict,
    recursively deep-update it.

    Examples:
    >>> t = {'name': 'Ferry', 'hobbies': ['programming', 'sci-fi']}
    >>> deepupdate(t, {'hobbies': ['gaming']})
    >>> print t
    {'name': 'Ferry', 'hobbies': ['programming', 'sci-fi', 'gaming']}

    Copyright Ferry Boender, released under the MIT license.
    """
    import copy
    for k, v in src.items():
        if type(v) == list:
            if k not in target:
                target[k] = copy.deepcopy(v)
            else:
                target[k].extend(v)
        elif type(v) == dict:
            if k not in target:
                target[k] = copy.deepcopy(v)
            else:
                deepupdate(target[k], v)
        elif type(v) == set:
            if k not in target:
                target[k] = v.copy()
            else:
                target[k].update(v.copy())
        else:
            target[k] = copy.copy(v)


def fetch_dataset(dataset_id: str, output_dir='~/.ancp-bids/datasets'):
    """Downloads and extracts an ancpBIDS  test dataset from Github.

    Parameters
    ----------
    dataset_id :
        The dataset ID of the ancp-bids-datasets github repository.
        See `https://github.com/ANCPLabOldenburg/ancp-bids-dataset` for more details.

    output_dir :
        The output directory to download and extract the dataset to.
        Default is to write to user's home directory at `~/.ancp-bids/datasets`

    Returns
    -------
        The path of the extracted dataset.
    """
    output_dir = os.path.expanduser(output_dir)
    output_dir = os.path.abspath(os.path.normpath(output_dir))
    output_path = os.path.join(output_dir, dataset_id)
    if os.path.exists(output_path):
        return output_path

    os.makedirs(output_path)

    download_file = f'{dataset_id}-testdata.zip'
    download_path = os.path.join(output_dir, download_file)

    if os.path.exists(download_path):
        return output_path

    url = f'https://github.com/ANCPLabOldenburg/ancp-bids-dataset/raw/main/{download_file}'
    import urllib.request, zipfile
    with urllib.request.urlopen(url) as dl_file:
        with open(download_path, 'wb') as out_file:
            out_file.write(dl_file.read())
    z = zipfile.ZipFile(download_path)
    z.extractall(output_dir)
    return output_path
