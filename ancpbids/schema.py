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
