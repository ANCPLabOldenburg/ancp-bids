
from ancpbids import load_dataset, _internal_validate_dataset
from ..base_test_case import DS005_CONFLICT_DIR, RESOURCES_FOLDER
from ancpbids.plugin import ValidationPlugin
from ancpbids.plugins import plugin_dsvalidator

def createSUT(ds_dir, rule_class):
    test_ds = load_dataset(ds_dir)
    # only test this plugin
    report = _internal_validate_dataset(test_ds, lambda plugin: isinstance(plugin, rule_class))
    assert isinstance(report, ValidationPlugin.ValidationReport)
    return report

def test_validate_static_structure():
    report = createSUT(DS005_CONFLICT_DIR, plugin_dsvalidator.StaticStructureValidationPlugin)
    assert len(report.messages) == 1
    assert 'dataset_description' in report.messages[0]['message']

def test_validate_datatypes():
    report = createSUT(DS005_CONFLICT_DIR, plugin_dsvalidator.DatatypesValidationPlugin)
    assert len(report.messages) == 2
    assert report.messages[0]['message'].replace('\\', '/') == "Unsupported datatype folder 'sub-01/abc'"
    assert report.messages[1]['message'].replace('\\', '/') == "Unsupported datatype folder 'sub-01/xyz'"

def test_validation_entities():
    report = createSUT(RESOURCES_FOLDER + "/ds005_entities_validation",
                       plugin_dsvalidator.EntitiesValidationPlugin)
    assert len(report.messages) == 2
    assert report.messages[0]['message'].replace('\\', '/') == (
        "Invalid entities order: expected=('sub', 'task', 'run'), found=('sub', 'run', 'task'), "
        "artifact=sub-01/func/sub-01_run-03_task-mixedgamblestask_events.tsv")
    assert report.messages[1]['message'].replace('\\', '/') == (
        "Invalid entity 'xyz' in artifact "
        "'sub-01/func/sub-01_task-mixedgamblestask_run-03_xyz-001_events.tsv'")
