from base_test_case import *
from bids import schema, dataset, validator
from bids.rules import rules_files


class ValidationTestCase(BaseTestCase):
    def createSUT(self, ds_dir, rule_class):
        bids_schema = schema.Schema(BIDS_SCHEMA_DIR)
        test_ds = dataset.Dataset(ds_dir)
        val = validator.Validator()
        # only test this rule
        val.ruleAcceptor = lambda rule: rule == rule_class
        report = val.validate(bids_schema, test_ds)
        self.assertTrue(isinstance(report, validator.ValidationReport))
        return report

    def test_validation_top_level_files(self):
        report = self.createSUT(DS005_CONFLICT_DIR, rules_files.TopLevelFilesValidationRule)
        self.assertEqual(2, len(report.messages))
        self.assertEqual("Missing required top level file 'README'", report.messages[0]['message'])
        self.assertEqual("Missing required top level file 'CHANGES'", report.messages[1]['message'])

    def test_validate_datatypes(self):
        report = self.createSUT(DS005_CONFLICT_DIR, rules_files.DatatypesValidationRule)
        self.assertEqual(2, len(report.messages))
        self.assertEqual("Unsupported datatype folder 'sub-01/ses-01/abc'", report.messages[0]['message'])
        self.assertEqual("Unsupported datatype folder 'sub-01/ses-01/xyz'", report.messages[1]['message'])

    def test_validation_entities(self):
        report = self.createSUT(RESOURCES_FOLDER + "/ds005_entities_validation", rules_files.EntitiesValidationRule)
        self.assertEqual(2, len(report.messages))
        self.assertEqual("Artifact name does not match expected pattern 'abc.txt'",
                         report.messages[0]['message'])
        self.assertEqual("Invalid entity 'xyz' in artifact "
                         "'sub-01_task-mixedgamblestask_run-03_xyz-001_events.tsv'",
                         report.messages[1]['message'])


if __name__ == '__main__':
    unittest.main()
