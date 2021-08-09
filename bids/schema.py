import logging

from .files import File, Folder

logger = logging.getLogger(__file__)


class Schema:
    def __init__(self, dir_path):
        self.top_level_files = File(dir_path + "/top_level_files.yaml")
        self.modalities = File(dir_path + "/modalities.yaml")
        self.entities = File(dir_path + "/entities.yaml")
        self.associated_data = File(dir_path + "/associated_data.yaml")

        self.datatypes = Folder(dir_path + "/datatypes")
        self.metadata = Folder(dir_path + "/metadata")
        self.suffixes = Folder(dir_path + "/suffixes")

    def get_version(self):
        return "master"
