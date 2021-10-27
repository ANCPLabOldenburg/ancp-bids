import logging
from difflib import SequenceMatcher

from . import model

logger = logging.getLogger(__file__)


class Schema:
    def __init__(self, models: model):
        self.model: model = model

    def _trim_int(self, value):
        try:
            # remove paddings/fillers in index values: 001 -> 1, 000230 -> 230
            return str(int(value))
        except ValueError:
            return value

    def process_entity_value(self, key, value):
        if not value or key not in self.model.EntityEnum.__members__:
            return value
        sc_entity = self.model.EntityEnum[key]
        if value and sc_entity.format_ == 'index':
            if isinstance(value, list):
                return list(map(lambda v: self._trim_int(v), value))
            else:
                return self._trim_int(value)
        return value

    def fuzzy_match_entity_key(self, user_key):
        ratios = list(
            map(lambda item: (
                item,
                1.0 if item.name.startswith(user_key) else SequenceMatcher(None, user_key, item.name).quick_ratio()),
                list(self.model.EntityEnum)))
        ratios = sorted(ratios, key=lambda t: t[1])
        return ratios[-1][0].entity_
