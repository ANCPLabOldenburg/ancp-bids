from ancpbids import validator, load_dataset
from ancpbids.rules import rules_files
from base_test_case import *


class ValidationTestCase(BaseTestCase):
    def createSUT(self, ds_dir, rule_class):
        test_ds = load_dataset(ds_dir)
        bids_schema = test_ds._schema
        val = validator.Validator()
        # only test this rule
        val.ruleAcceptor = lambda rule: rule == rule_class
        report = val.validate(bids_schema, test_ds)
        self.assertTrue(isinstance(report, validator.ValidationReport))
        return report

    def test_validate_static_structure(self):
        report = self.createSUT(DS005_CONFLICT_DIR, rules_files.StaticStructureValidationRule)
        self.assertEqual(2, len(report.messages))
        self.assertTrue('README' in report.messages[0]['message'], 'README file not expected')
        self.assertTrue('CHANGES' in report.messages[1]['message'], 'CHANGES file not expected')

    def test_validate_datatypes(self):
        report = self.createSUT(DS005_CONFLICT_DIR, rules_files.DatatypesValidationRule)
        self.assertEqual(2, len(report.messages))
        self.assertEqual("Unsupported datatype folder 'sub-01/abc'", report.messages[0]['message'])
        self.assertEqual("Unsupported datatype folder 'sub-01/xyz'", report.messages[1]['message'])

    def test_validation_entities(self):
        report = self.createSUT(RESOURCES_FOLDER + "/ds005_entities_validation", rules_files.EntitiesValidationRule)
        self.assertEqual(2, len(report.messages))
        self.assertEqual(
            "Invalid entities order: expected=('sub', 'task', 'run'), found=('sub', 'run', 'task'), "
            "artifact=sub-01/func/sub-01_run-03_task-mixedgamblestask_events.tsv",
            report.messages[0]['message'])
        self.assertEqual("Invalid entity 'xyz' in artifact "
                         "'sub-01/func/sub-01_task-mixedgamblestask_run-03_xyz-001_events.tsv'",
                         report.messages[1]['message'])


if __name__ == '__main__':
    unittest.main()
