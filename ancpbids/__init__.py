import logging
import os
import sys

import regex

from . import plugins
from . import files
from . import utils
from .plugin import get_plugins, load_plugins_by_package, DatasetPlugin, WritingPlugin, ValidationPlugin, SchemaPlugin
from .plugins.plugin_query import BoolExpr, Select, EqExpr, AnyExpr, AllExpr, ReExpr, CustomOpExpr, \
    EntityExpr

LOGGER = logging.getLogger("ancpbids")

ENTITIES_PATTERN = regex.compile(r'(([^\W_]+)-([^\W_]+)_)+([^\W_]+)((\.[^\W_]+)+)')


def load_dataset(base_dir: str):
    """
    Loads a dataset given its directory path on the file system.

    .. code-block::

        from ancpbids import load_dataset, validate_dataset
        dataset_path = 'path/to/your/dataset'
        dataset = load_dataset(dataset_path)

    :param base_dir: the dataset path to load from
    :return: an object instance of type :py:class:`ancpbids.model.Dataset` which represents the dataset as an in-memory graph
    """
    schema = load_schema(base_dir)
    ds = schema.Dataset()
    ds.name = os.path.basename(base_dir)
    ds.base_dir_ = base_dir
    dataset_plugins = get_plugins(DatasetPlugin)
    for dsplugin in dataset_plugins:
        dsplugin.execute(ds)
    return ds


def load_schema(base_dir):
    ds_descr_path = os.path.join(base_dir, "dataset_description.json")
    if os.path.exists(ds_descr_path):
        ds_descr = files.load_contents(ds_descr_path)
        if isinstance(ds_descr, dict) and 'BIDSVersion' in ds_descr:
            schema_version = ds_descr['BIDSVersion']
            schema_version = schema_version.replace('.', '_')
            schema_name = f'ancpbids.model_v{schema_version}'
            if schema_name in sys.modules:
                schema = sys.modules[schema_name]
                return schema
    # assume using the earliest supported schema
    from . import model_v1_7_0
    return model_v1_7_0


def save_dataset(ds, target_dir: str, context_folder=None):
    dataset_plugins = get_plugins(WritingPlugin)
    for dsplugin in dataset_plugins:
        dsplugin.execute(ds, target_dir, context_folder=context_folder)


def validate_dataset(dataset) -> ValidationPlugin.ValidationReport:
    """
    Validates a dataset and returns a report object containing any detected validation errors.

    Example:

    .. code-block::

        report = validate_dataset(dataset)
        for message in report.messages:
            print(message)
        if report.has_errors():
            raise "The dataset contains validation errors, cannot continue".


    :param dataset: the dataset to validate
    :return: a report object containing any detected validation errors or warning
    """
    return _internal_validate_dataset(dataset)


def _internal_validate_dataset(dataset, plugin_acceptor=None):
    validation_plugins = get_plugins(ValidationPlugin)
    report = ValidationPlugin.ValidationReport()
    for validation_plugin in validation_plugins:
        # if plugin is disabled, skip it
        if callable(plugin_acceptor) and not plugin_acceptor(validation_plugin):
            continue
        validation_plugin.execute(dataset=dataset, report=report)
    return report


def write_derivative(ds, derivative):
    save_dataset(ds, target_dir=ds.get_absolute_path(), context_folder=derivative)


# load system plugins using lowest rank value
load_plugins_by_package(plugins, ranking=0, system=True)

# execute all SchemaPlugins, these plugins may monkey-patch the schema
from ancpbids import model_v1_7_0, model_v1_7_1

for pl in get_plugins(SchemaPlugin):
    for model in [model_v1_7_0, model_v1_7_1]:
        pl.execute(model)

from .pybids_compat import BIDSLayout

select = Select
any_of = AnyExpr
all_of = AllExpr
eq = EqExpr
re = ReExpr
op = CustomOpExpr
entity = EntityExpr

from . import _version

__version__ = _version.get_versions()['version']
