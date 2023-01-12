import logging
import os
import sys
from dataclasses import dataclass
from typing import Union, List, Optional

from . import plugins
from . import utils
from .plugin import get_plugins, load_plugins_by_package, DatasetPlugin, WritingPlugin, ValidationPlugin, SchemaPlugin, \
    FileHandlerPlugin
from .query import BoolExpr, Select, EqExpr, AnyExpr, AllExpr, ReExpr, CustomOpExpr, \
    EntityExpr
from . import model_v1_8_0
from . import model_v1_8_0 as model_latest

LOGGER = logging.getLogger("ancpbids")


# ENTITIES_PATTERN = regex.compile(r'(([^\W_]+)-([^\W_]+)_)+([^\W_]+)((\.[^\W_]+)+)')

@dataclass
class DatasetOptions(dict):
    """All options that can be set to influence handling of reading/writing a dataset from/to file system."""
    infer_artifact_datatype: bool = False
    """If True, will determine the datatype an Artifact is contained in, either directly or within a sub-directory.
        For example, given the path "sub-02/func/sub-02_task-mixedgamblestask_run-01_bold.nii.gz", the datatype will be "func".
        
        By default, this option is set to False as it may have a negative performance impact.
    """

    ignore: Union[bool, List[str]] = False
    """If a .bidsignore file is available at the root, all resources (files/folders) matching the filters
        in that file will not be added to the in-memory graph. Alternatively, a list of fnmatch patterns can be provided.
        
        By default, this option is set to False as it may have a negative performance impact."""


def load_dataset(base_dir: str, options: Optional[DatasetOptions] = None):
    """Loads a dataset given its directory path on the file system.

    .. code-block::

        from ancpbids import load_dataset, validate_dataset
        dataset_path = 'path/to/your/dataset'
        dataset = load_dataset(dataset_path, DatasetOptions(ignore=False, infer_artifact_datatype=True))

    Parameters
    ----------
    base_dir:
        the dataset path to load from
    options:
        the options to use, see :py:class:`DatasetOptions` class for available options

    Returns
    -------
    str
        a Dataset object depending on the used schema which represents the dataset as an in-memory graph
    """
    if not os.path.isdir(base_dir):
        raise ValueError("Invalid Directory")
    schema = load_schema(base_dir)
    ds = schema.Dataset()
    ds._versioned_schema = schema
    ds.options = options
    if ds.options is None:
        ds.options = DatasetOptions()
    ds.name = os.path.basename(base_dir)
    ds.base_dir_ = base_dir
    dataset_plugins = get_plugins(DatasetPlugin)
    for dsplugin in dataset_plugins:
        dsplugin.execute(ds, schema)
    return ds


def load_schema(base_dir):
    """Loads a BIDS schema object which represents the static/formal definition of the BIDS specification.

    As per BIDS spec, a BIDS compliant dataset must have a BIDSVersion field in the dataset_description.json
    file at the top level. This field is used to determine which BIDS schema to load.

    In case the BIDSVersion field is missing or not supported, the earliest supported schema will be returned.

    Parameters
    ----------
    base_dir:
        The dataset directory path where a dataset_description.json must be located.

    Returns
    -------
    object
        A BIDS schema object which represents the static/formal definition of the BIDS specification.
    """
    ds_descr_path = os.path.join(base_dir, "dataset_description.json")
    if os.path.exists(ds_descr_path):
        ds_descr = utils.load_contents(ds_descr_path)
        if isinstance(ds_descr, dict) and 'BIDSVersion' in ds_descr:
            schema_version = ds_descr['BIDSVersion']
            schema_version = schema_version.replace('.', '_')
            schema_name = f'ancpbids.model_v{schema_version}'
            if schema_name in sys.modules:
                schema = sys.modules[schema_name]
                return schema
    # assume using the latest supported schema
    return model_latest


def save_dataset(ds: object, target_dir: str, context_folder=None):
    """Copies the dataset graph into the provided target directory.

    EXPERIMENTAL/UNSTABLE

    Parameters
    ----------
    ds:
        the dataset graph to save
    target_dir
        the target directory to save to
    context_folder
        a folder node within the dataset graph to limit to

    """
    dataset_plugins = get_plugins(WritingPlugin)
    for dsplugin in dataset_plugins:
        dsplugin.execute(ds, target_dir, context_folder=context_folder)


def validate_dataset(dataset) -> ValidationPlugin.ValidationReport:
    """Validates a dataset and returns a report object containing any detected validation errors.

    Example:

    .. code-block::

        report = validate_dataset(dataset)
        for message in report.messages:
            print(message)
        if report.has_errors():
            raise "The dataset contains validation errors, cannot continue".

    Parameters
    ----------
    dataset:
        the dataset to validate

    Returns
    -------
    ValidationPlugin.ValidationReport
        a report object containing any detected validation errors or warning
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
    """Writes the provided derivative folder to the dataset.
    Note that a 'derivatives' folder will be created if not present.

    Parameters
    ----------
    ds:
        the dataset object to extend
    derivative:
        the derivative folder to write
    """
    save_dataset(ds, target_dir=ds.get_absolute_path(), context_folder=derivative)


# load system plugins using lowest rank value
load_plugins_by_package(plugins, ranking=0, system=True)

# execute all SchemaPlugins, these plugins may monkey-patch the schema
for pl in get_plugins(SchemaPlugin):
    for schema in [model_v1_8_0]:
        pl.execute(schema)

# load file handler plugins
for pl in get_plugins(FileHandlerPlugin):
    pl.execute(utils.FILE_READERS, utils.FILE_WRITERS)

select = Select
any_of = AnyExpr
all_of = AllExpr
eq = EqExpr
re = ReExpr
op = CustomOpExpr
entity = EntityExpr

from . import _version

__version__ = _version.get_versions()['version']
