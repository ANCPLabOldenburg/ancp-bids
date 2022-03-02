from ancpbids import load_dataset, _internal_validate_dataset
from ..base_test_case import *
from ancpbids.plugin import ValidationPlugin
from ancpbids.plugins import plugin_dsvalidator


class ValidationTestCase(BaseTestCase):
    def createSUT(self, ds_dir, rule_class):
        test_ds = load_dataset(ds_dir)
        # only test this plugin
        report = _internal_validate_dataset(test_ds, lambda plugin: isinstance(plugin, rule_class))
        self.assertTrue(isinstance(report, ValidationPlugin.ValidationReport))
        return report

    def test_validate_static_structure(self):
        report = self.createSUT(DS005_CONFLICT_DIR, plugin_dsvalidator.StaticStructureValidationPlugin)
        self.assertEqual(1, len(report.messages))
        self.assertTrue('dataset_description' in report.messages[0]['message'],
                        'dataset_description file should have been reported as missing')

    def test_validate_datatypes(self):
        report = self.createSUT(DS005_CONFLICT_DIR, plugin_dsvalidator.DatatypesValidationPlugin)
        self.assertEqual(2, len(report.messages))
        self.assertEqual("Unsupported datatype folder 'sub-01/abc'", report.messages[0]['message'].replace('\\', '/'))
        self.assertEqual("Unsupported datatype folder 'sub-01/xyz'", report.messages[1]['message'].replace('\\', '/'))

    def test_validation_entities(self):
        report = self.createSUT(RESOURCES_FOLDER + "/ds005_entities_validation",
                                plugin_dsvalidator.EntitiesValidationPlugin)
        self.assertEqual(2, len(report.messages))
        self.assertEqual(
            "Invalid entities order: expected=('sub', 'task', 'run'), found=('sub', 'run', 'task'), "
            "artifact=sub-01/func/sub-01_run-03_task-mixedgamblestask_events.tsv",
            report.messages[0]['message'].replace('\\', '/'))
        self.assertEqual("Invalid entity 'xyz' in artifact "
                         "'sub-01/func/sub-01_task-mixedgamblestask_run-03_xyz-001_events.tsv'",
                         report.messages[1]['message'].replace('\\', '/'))


if __name__ == '__main__':
    unittest.main()
