import inspect
import os

from ancpbids import model

_MODEL_CLASSES = {name: obj for name, obj in inspect.getmembers(model) if inspect.isclass(obj)}


def get_members(element_type, include_superclass=True):
    if element_type == model.Model:
        return []
    super_members = []

    if include_superclass:
        try:
            superclass = inspect.getmro(element_type)[1]
            if superclass:
                super_members = get_members(superclass, include_superclass)
        except AttributeError:
            pass

    element_members = []
    try:
        members = element_type.MEMBERS
        element_members = list(
            map(lambda item: {'name': item[0], **item[1], 'type': _to_type(item[1]['type'])},
                members.items()))
    except AttributeError as ae:
        pass
    return super_members + element_members


def _to_type(model_type_name: str):
    if model_type_name in _MODEL_CLASSES:
        return _MODEL_CLASSES[model_type_name]
    if model_type_name in __builtins__:
        return __builtins__[model_type_name]
    return model_type_name


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
    import urllib.request, zipfile, io
    with urllib.request.urlopen(url) as dl_file:
        with open(download_path, 'wb') as out_file:
            out_file.write(dl_file.read())
    z = zipfile.ZipFile(download_path)
    z.extractall(output_dir)

