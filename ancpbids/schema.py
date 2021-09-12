import logging
import os
from collections import OrderedDict
from difflib import SequenceMatcher

from . import files

logger = logging.getLogger(__file__)


class Schema:
    def __init__(self, schema_path, ns, ns_prefix):
        self.schema_path = schema_path
        self.ns = ns
        self.ns_prefix = ns_prefix
        self.ns_map = {
            self.ns_prefix: self.ns
        }
        self.modalities = files.load_contents(schema_path + "/modalities.yaml")
        # self.modalities = list(map(lambda item: {'key': item[0], **item[1]}, self.modalities.items()))
        self.entities = files.load_contents(schema_path + "/entities.yaml")
        self.datatypes = self.merge_to_dict(schema_path + "/datatypes")

    def get_ns_map(self):
        return self.ns_map

    def merge_to_dict(self, dir_path):
        result = {}
        for file in files.get_files(dir_path, include_folders=False, fnmatch_pattern="*.yaml"):
            name_wo_ext = os.path.basename(file)[:-5]
            result[name_wo_ext] = files.load_contents(file)
        return result

    def _trim_int(self, value):
        try:
            # remove paddings/fillers in index values: 001 -> 1, 000230 -> 230
            return str(int(value))
        except ValueError:
            return value

    def process_entity_value(self, key, value):
        if not value or key not in self.entities:
            return value
        sc_entity = self.entities[key]
        if value and sc_entity and 'format' in sc_entity and sc_entity['format'] == 'index':
            if isinstance(value, list):
                return list(map(lambda v: self._trim_int(v), value))
            else:
                return self._trim_int(value)
        return value

    def fuzzy_match_entity_key(self, user_key):
        ratios = list(
            map(lambda item: (
                item[1], 1.0 if item[0].startswith(user_key) else SequenceMatcher(None, user_key, item[0]).quick_ratio()),
                self.entities.items()))
        ratios = sorted(ratios, key=lambda t: t[1])
        return ratios[-1][0]['entity']
