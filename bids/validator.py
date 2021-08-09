import logging

from bids import rules
from .dataset import Dataset
from .schema import Schema

logger = logging.getLogger(__file__)


class Validator:
    def validate(self, schema: Schema, dataset: Dataset):
        validation_rules = rules.collect_rules()
        report = ValidationReport()
        for rule in validation_rules:
            try:
                instance = rule()
                instance.validate(schema, dataset, report)
            except Exception as e:
                logger.error("Could not execute validation rule %s: %s" % (rule.__name__, e))
        return report


class ValidationReport:
    messages = []

    def error(self, message):
        self.messages.append({
            'severity': 'error',
            'message': message
        })


class ValidationRule:
    def validate(self, schema: Schema, dataset: Dataset, report: ValidationReport):
        raise NotImplemented()
