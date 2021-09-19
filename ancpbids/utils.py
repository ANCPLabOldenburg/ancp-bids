import inspect

from ancpbids import model

_MODEL_CLASSES = {name: obj for name, obj in inspect.getmembers(model) if inspect.isclass(obj)}


def get_members(element_type, include_superclass=True):
    if element_type == model.File or element_type == model.Folder:
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
        # name is the class member name compatible with Python naming conventions
        # name_raw contains the name as modeled in schema and may contain invalid characters such as dots
        members = element_type.MEMBERS
        element_members = list(
            map(lambda item: {'name': item[0], 'name_raw': item[0], 'type': _to_type(item[1]['type']),
                              'list': item[1]['list'], 'kwargs': item[1]['kwargs']},
                members.items()))
    except AttributeError as ae:
        pass
    return super_members + element_members


def _to_type(model_type_name: str):
    if model_type_name in _MODEL_CLASSES:
        return _MODEL_CLASSES[model_type_name]
    return model_type_name
