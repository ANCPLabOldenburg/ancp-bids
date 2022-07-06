import logging
import os

FILE_READERS = {}
FILE_WRITERS = {}

LOGGER = logging.getLogger(__file__)


def parse_bids_name(name: str):
    """Parses a given string (file name) according to the BIDS naming scheme.

    Parameters
    ----------
    name
        The file name to parse. If a full path (with path separaters), the path segments will be ignored.

    Returns
    -------
    dict
        A dictionary describing the BIDS naming components.

    Examples
    --------

    >>> bids_obj = parse_bids_name("sub-11_task-mixedgamblestask_run-02_bold.nii.gz")
    {'entities': {'sub': '11', 'task': 'mixedgamblestask', 'run': '02'}, 'suffix': 'bold', 'extension': '.nii.gz'}

    """
    base_name = os.path.basename(name)
    parts = base_name.split(os.extsep, 1)
    if len(parts) != 2:
        # if extension missing, then not a valid BIDS file
        return None

    extension = os.extsep + parts[1]
    underscore_parts = parts[0].split('_')

    if len(underscore_parts) < 2:
        return None

    # last segment must be suffix
    suffix = underscore_parts[-1]
    if '-' in suffix:
        return None

    entities = {}
    for i in range(0, len(underscore_parts) - 1):
        dash_parts = underscore_parts[i].split('-')
        if len(dash_parts) < 2:
            # not a key-value pair
            return None
        entities[dash_parts[0]] = dash_parts[1]

    return {
        'entities': entities,
        'suffix': suffix,
        'extension': extension
    }


def load_contents(file_path, return_type: str = None):
    """Loads the contents of the provided file path.

    Parameters
    ----------
    file_path :
        the file path to load contents from
    return_type:
        A hint to consider when deciding how to load the contents of the provided file.
        For example, to load a TSV file as a pandas DataFrame the return_type should be 'dataframe',
        to load a numpy ndarray, the return_type should be 'ndarray'.
        It is up to the registered file handlers to correctly interpret the return_type.

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
    return reader(file_path, return_type=return_type)


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


def resolve_segments(root_folder, path_, last_seg_file=False, create_if_missing=False):
    context = root_folder
    if path_:
        normalized_path = os.path.normpath(path_)
        path_segments = normalized_path.split(os.sep)
        path_segments = list(filter(lambda s: s != '', path_segments))
        if last_seg_file:
            path_ = path_segments[-1]
            path_segments = path_segments[:-1]

        for seg in path_segments:
            context = context.get_folder(seg)
            if not context:
                if create_if_missing:
                    context.create_folder(seg)
                else:
                    break
    return context, path_


def convert_to_relative(dataset, path):
    if path and path.startswith(dataset.base_dir_):
        path = os.path.normpath(path)
        path = path[len(dataset.base_dir_):]
        path_segments = path.split(os.sep)
        path_segments = list(filter(lambda s: s != '', path_segments))
        path = os.path.join(*path_segments)
    return path
