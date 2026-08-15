
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


def test_directories_rule_missing_is_skipped(tmp_path):
    """Schemas without rules.directories (e.g. 1.8.0) must not crash validation."""
    import json
    from ancpbids import validate_dataset

    root = tmp_path / "ds"
    root.mkdir()
    (root / "dataset_description.json").write_text(json.dumps({
        "Name": "NoDirectoriesRule",
        "BIDSVersion": "1.8.0",
        "DatasetType": "raw",
    }))
    sub = root / "sub-01" / "anat"
    sub.mkdir(parents=True)
    (sub / "sub-01_T1w.nii.gz").write_bytes(b"\0")

    ds = load_dataset(str(root), DatasetOptions(lazy_loading=True, ignore_pickle_file=True))
    assert ds.get_schema().VERSION == "1.8.0"
    assert "directories" not in ds.get_schema().document.get("rules", {})

    report = createSUT(str(root), SchemaDirectoriesPlugin, True)
    assert isinstance(report, ValidationPlugin.ValidationReport)

    # Full validate must also succeed without KeyError.
    full = validate_dataset(ds)
    assert isinstance(full, ValidationPlugin.ValidationReport)


def test_validation_report_includes_issue_codes(tmp_path):
    import json
    from ancpbids import validate_dataset
    from ancpbids.plugins.plugin_schema_validator import SchemaSidecarsPlugin

    root = tmp_path / "ds"
    root.mkdir()
    (root / "dataset_description.json").write_text(json.dumps({
        "Name": "CodeCheck",
        "BIDSVersion": "1.10.1",
        "DatasetType": "raw",
    }))
    func = root / "sub-01" / "func"
    func.mkdir(parents=True)
    (func / "sub-01_task-rest_bold.nii.gz").write_bytes(b"\0")
    (func / "sub-01_task-rest_bold.json").write_text(json.dumps({
        "RepetitionTime": 2.0,
        "TaskName": "rest",
    }))

    report = createSUT(str(root), SchemaSidecarsPlugin, True)
    assert report.messages
    assert all('code' in m for m in report.messages)
    assert 'SIDECAR_KEY_RECOMMENDED' in report.codes()
    manufacturer = next(
        m for m in report.messages
        if m.get('code') == 'SIDECAR_KEY_RECOMMENDED' and m.get('sub_code') == 'Manufacturer'
    )
    assert manufacturer['severity'] == 'warn'

    full = validate_dataset(load_dataset(str(root), DatasetOptions(lazy_loading=True)))
    assert all('code' in m for m in full.messages)


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
