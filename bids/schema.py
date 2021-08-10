import logging

from .files import File, Folder

logger = logging.getLogger(__file__)


class Schema:
    def __init__(self, dir_path):
        self.top_level_files = File(dir_path + "/top_level_files.yaml")
        self.modalities = File(dir_path + "/modalities.yaml")
        self.entities = File(dir_path + "/entities.yaml")
        self.associated_data = File(dir_path + "/associated_data.yaml")

        self.datatypes = self.merge_to_dict(Folder(dir_path + "/datatypes"))
        self.metadata = self.merge_to_dict(Folder(dir_path + "/metadata"))
        self.suffixes = self.merge_to_dict(Folder(dir_path + "/suffixes"))

    def merge_to_dict(self, folder: Folder):
        result = {}
        for file in folder.get_files(include_folders=False, fnmatch_pattern="*.yaml"):
            name_wo_ext = file.name()[:-5]
            result[name_wo_ext] = file.load_contents()
        return result

    def get_version(self):
        return "master"
