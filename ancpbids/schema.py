import logging
import os
from collections import OrderedDict

from . import files

logger = logging.getLogger(__file__)

SCHEMA_PATH = os.path.dirname(__file__) + '/data/schema-files'

NS = 'https://bids.neuroimaging.io/1.6'
NS_PREFIX = 'bids'
NS_MAP = {NS_PREFIX: NS}


class Schema:
    def __init__(self):
        self.modalities = files.load_contents(SCHEMA_PATH + "/modalities.yaml")
        self.entities = files.load_contents(SCHEMA_PATH + "/entities.yaml")
        # convert to dictionary for faster lookup by entity keys
        # and keep order of entities in sync with entries in file
        self.entities = OrderedDict([(e['key'], e) for e in self.entities])
        self.datatypes = self.merge_to_dict(SCHEMA_PATH + "/datatypes")

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