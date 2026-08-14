
from ancpbids import load_dataset, _internal_validate_dataset
from ..base_test_case import DS005_CONFLICT_DIR, RESOURCES_FOLDER
from ancpbids.plugin import ValidationPlugin, get_plugins
from ancpbids.plugins import plugin_schema_validator as schema_plugins
from ancpbids.plugins.plugin_schema_validator import (
    SchemaDirectoriesPlugin,
    SchemaEntitiesPlugin,
)

import pytest
from ancpbids import DatasetOptions


def createSUT(ds_dir, rule_class, lazy_loading):
    test_ds = load_dataset(ds_dir, DatasetOptions(lazy_loading=lazy_loading))
    report = _internal_validate_dataset(test_ds, lambda plugin: isinstance(plugin, rule_class))
    assert isinstance(report, ValidationPlugin.ValidationReport)
    return report


def _messages(report):
    return [m['message'].replace('\\', '/') for m in report.messages]


def test_schema_rule_plugins_registered():
    names = {type(plugin).__name__ for plugin in get_plugins(ValidationPlugin)}
    assert names == {
        'SchemaChecksPlugin',
        'SchemaDatasetMetadataPlugin',
        'SchemaDirectoriesPlugin',
        'SchemaEntitiesPlugin',
        'SchemaFilesPlugin',
        'SchemaJsonPlugin',
        'SchemaSidecarsPlugin',
        'SchemaTabularDataPlugin',
    }
    for name in names:
        assert issubclass(getattr(schema_plugins, name), ValidationPlugin)


@pytest.mark.parametrize("lazy_loading", [True, False])
def test_validate_datatypes(lazy_loading):
    report = createSUT(DS005_CONFLICT_DIR, SchemaDirectoriesPlugin, lazy_loading)
    messages = _messages(report)
    assert "Unsupported datatype folder 'sub-01/abc'" in messages
    assert "Unsupported datatype folder 'sub-01/xyz'" in messages


@pytest.mark.parametrize("lazy_loading", [True, False])
def test_validation_entities(lazy_loading):
    report = createSUT(RESOURCES_FOLDER + "/ds005_entities_validation",
                       SchemaEntitiesPlugin, lazy_loading)
    messages = _messages(report)
    assert (
        "Invalid entities order: expected=('sub', 'task', 'run'), found=('sub', 'run', 'task'), "
        "artifact=sub-01/func/sub-01_run-03_task-mixedgamblestask_events.tsv"
    ) in messages
    assert (
        "Invalid entity 'xyz' in artifact "
        "'sub-01/func/sub-01_task-mixedgamblestask_run-03_xyz-001_events.tsv'"
    ) in messages
