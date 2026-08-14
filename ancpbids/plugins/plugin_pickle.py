import os
import pickle
from types import ModuleType

from ancpbids import utils
from ancpbids.model_base import Dataset

ANCP_BIDS_SCHEMA_VERSION = "AncpBIDSSchemaVersion"

ANCPBIDS_PICKLE_FILE = ".ancpbids-dataset.pickle"


class DatasetPickler(pickle.Pickler):

    def persistent_id(self, obj):
        from ancpbids.schema import Schema
        if isinstance(obj, Schema):
            return (ANCP_BIDS_SCHEMA_VERSION, obj.VERSION)
        if isinstance(obj, ModuleType) and obj.__name__.startswith("ancpbids."):
            return (ANCP_BIDS_SCHEMA_VERSION, obj.VERSION)
        return None


class DatasetUnpickler(pickle.Unpickler):

    def persistent_load(self, pid):
        type_tag, key_id = pid
        if type_tag == "AncpBIDSSchemaVersion":
            return utils.get_schema_by_version(key_id)

        raise pickle.UnpicklingError(f"unsupported persistent object: {pid}")


def pickle_dataset(dataset, custom_dir=None):
    ds_path = os.path.join(custom_dir or dataset.get_absolute_path(), ANCPBIDS_PICKLE_FILE)
    with open(ds_path, 'wb') as f:
        DatasetPickler(f).dump(dataset)


def unpickle_dataset(dataset_path) -> Dataset:
    ds_path = os.path.join(dataset_path, ANCPBIDS_PICKLE_FILE)
    with open(ds_path, 'rb') as f:
        return DatasetUnpickler(f).load()
