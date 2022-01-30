import logging
import os

import ancpbids.plugins
from . import files
from . import model
from . import utils
from .plugin import get_plugins, load_plugins_by_package, DatasetPlugin, WritingPlugin, ValidationPlugin
from .query import XPathQuery, BoolExpr, Select, EqExpr, AnyExpr, AllExpr, ReExpr, CustomOpExpr, EntityExpr, \
    DatatypeExpr
from .schema import Schema

LOGGER = logging.getLogger("ancpbids")
SCHEMA_LATEST = Schema(model)


def load_dataset(base_dir: str, bids_schema=SCHEMA_LATEST):
    ds = model.Dataset()
    ds._schema = bids_schema
    ds.name = os.path.basename(base_dir)
    ds.base_dir_ = base_dir
    dataset_plugins = get_plugins(DatasetPlugin)
    for dsplugin in dataset_plugins:
        dsplugin.execute(ds)
    return ds


def save_dataset(ds: model.Dataset, target_dir: str, context_folder: model.Folder = None):
    dataset_plugins = get_plugins(WritingPlugin)
    for dsplugin in dataset_plugins:
        dsplugin.execute(ds, target_dir, context_folder=context_folder)


def validate_dataset(dataset: model.Dataset, plugin_acceptor=None):
    validation_plugins = get_plugins(ValidationPlugin)
    report = ValidationPlugin.ValidationReport()
    for validation_plugin in validation_plugins:
        # if plugin is disabled, skip it
        if callable(plugin_acceptor) and not plugin_acceptor(validation_plugin):
            continue
        validation_plugin.execute(dataset=dataset, report=report)
    return report


def write_derivative(ds: model.Dataset, derivative: model.DerivativeFolder):
    save_dataset(ds, target_dir=ds.get_absolute_path(), context_folder=derivative)


# load system plugins using lowest rank value
load_plugins_by_package(ancpbids.plugins, ranking=0, system=True)

from .pybids_compat import BIDSLayout

select = Select
any_of = AnyExpr
all_of = AllExpr
eq = EqExpr
re = ReExpr
op = CustomOpExpr
entity = EntityExpr
datatype = DatatypeExpr

from . import _version

__version__ = _version.get_versions()['version']
