import os
import unittest

TEST_FOLDER = os.path.dirname(__file__)
RESOURCES_FOLDER = TEST_FOLDER + "/data"

DS005_DIR = RESOURCES_FOLDER + "/ds005"
DS005_CONFLICT_DIR = RESOURCES_FOLDER + "/ds005_conflict"
DS005_SMALL_DIR = RESOURCES_FOLDER + "/ds005-small"
DS005_SMALL2_DIR = RESOURCES_FOLDER + "/ds005-small2"
SYNTHETIC_DIR = RESOURCES_FOLDER + "/synthetic"
ENTITIES_DIR = RESOURCES_FOLDER + "/ds005_entities_validation"
DS005_DIR_IGNORED_RESOURCES = RESOURCES_FOLDER + "/ds005_ignore"
DS7t_trt_DIR = RESOURCES_FOLDER + "/7t_trt"


class BaseTestCase(unittest.TestCase):
    pass
