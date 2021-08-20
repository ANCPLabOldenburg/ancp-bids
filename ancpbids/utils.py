import inspect

from ancpbids import model

_MODEL_CLASSES = {name: obj for name, obj in inspect.getmembers(model) if inspect.isclass(obj)}

def get_members(element_type, include_superclass=True):
    if element_type == model.File or element_type == model.Folder:
        return []
    super_members = []

    if include_superclass:
        try:
            if element_type.superclass:
                super_members = get_members(element_type.superclass, include_superclass)
        except AttributeError:
            pass

    element_members = []
    try:
        # name is the class member name compatible with Python naming conventions
        # name_raw contains the name as modeled in schema and may contain invalid characters such as dots
        element_members = list(
            map(lambda member: {'name_raw': member.child_attrs['name'], 'type': member.data_type, **member.child_attrs,
                                'name': member.name},
                element_type.member_data_items_.values()))
        element_members = list(map(_normalize, element_members))
    except AttributeError as ae:
        pass
    return super_members + element_members

def _to_type(model_type_name: str):
    if model_type_name == 'string':
        return str
    return _MODEL_CLASSES[model_type_name]


def _normalize(member):
    result = {'name': member['name'], 'name_raw': member['name_raw'], 'typ': _to_type(member['type'])}
    if 'use' in member:
        result['lower'] = 1 if member['use'] == 'required' else 0
        result['upper'] = 1
    else:
        result['lower'] = member['minOccurs']
        result['upper'] = member['maxOccurs']
    return result
