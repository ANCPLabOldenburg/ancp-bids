import logging

from .schema import Schema
from .model import Dataset
from . import rules, XPathQuery

logger = logging.getLogger(__file__)


class Validator:
    def __init__(self):
        self.ruleAcceptor = None

    def validate(self, schema: Schema, dataset: Dataset):
        validation_rules = rules.collect_rules()
        report = ValidationReport()
        query = XPathQuery(dataset, schema)
        for rule in validation_rules:
            # if rule is disabled, skip it
            if self.ruleAcceptor is not None and not self.ruleAcceptor(rule):
                continue
            try:
                instance = rule()
                instance.validate(schema=schema, dataset=dataset, report=report, query=query)
            except Exception as e:
                logger.error("Could not execute validation rule %s: %s" % (rule.__name__, e))
                raise e
        return report


class ValidationReport:
    def __init__(self):
        self.messages = []

    def error(self, message):
        self.messages.append({
            'severity': 'error',
            'message': message
        })


class ValidationRule:
    def validate(self, **kwargs):
        raise NotImplemented()
