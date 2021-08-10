import os
import unittest

BIDS_SCHEMA_DIR = os.path.expanduser("~/git/bids-specification/src/schema/")
TEST_FOLDER = os.path.dirname(__file__)
RESOURCES_FOLDER = TEST_FOLDER + "/data"

DS005_DIR = RESOURCES_FOLDER + "/ds005"
DS005_CONFLICT_DIR = RESOURCES_FOLDER + "/ds005_conflict"


class BaseTestCase(unittest.TestCase):
    pass
