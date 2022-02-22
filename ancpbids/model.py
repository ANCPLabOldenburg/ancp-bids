from .model_v1_7_0 import *
from difflib import SequenceMatcher


def _trim_int(value):
    try:
        # remove paddings/fillers in index values: 001 -> 1, 000230 -> 230
        return str(int(value))
    except ValueError:
        return value


def process_entity_value(key, value):
    if not value or key not in EntityEnum.__members__:
        return value
    sc_entity = EntityEnum[key]
    if value and sc_entity.format_ == 'index':
        if isinstance(value, list):
            return list(map(lambda v: _trim_int(v), value))
        else:
            return _trim_int(value)
    return value


def fuzzy_match_entity_key(user_key):
    return fuzzy_match_entity(user_key).entity_


def fuzzy_match_entity(user_key):
    ratios = list(
        map(lambda item: (
            item,
            1.0 if item.name.startswith(user_key) else SequenceMatcher(None, user_key, item.name).quick_ratio()),
            list(EntityEnum)))
    ratios = sorted(ratios, key=lambda t: t[1])
    return ratios[-1][0]
