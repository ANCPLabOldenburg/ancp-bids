from ancpbids import XPathQuery
from ancpbids.model import Dataset, GdsCollector_, Session, Subject, Datatype
from ancpbids.schema import Schema
from ancpbids.validator import ValidationRule, ValidationReport


class StaticStructureValidationRule(ValidationRule):
    def validate(self, dataset: Dataset, report: ValidationReport, **kwargs):
        collector = GdsCollector_()
        dataset.validate_(collector, recursive=True)
        for message in collector.messages:
            report.error(message)


class DatatypesValidationRule(ValidationRule):
    def validate(self, dataset: Dataset, report: ValidationReport, **kwargs):
        dangling_folders = []
        for subject in dataset.get_subjects():
            dangling_folders.extend(subject.get_folders())
            for session in subject.get_sessions():
                dangling_folders.extend(session.get_folders())

        for folder in dangling_folders:
            report.error("Unsupported datatype folder '%s'" % folder.get_relative_path())


class EntitiesValidationRule(ValidationRule):
    def validate(self, schema: Schema, dataset: Dataset, report: ValidationReport, query: XPathQuery):
        artifacts = query.execute('//bids:entities/..')
        expected_key_order = {k: i for i, k in enumerate(schema.entities.keys())}
        expected_order_key = {i: k for i, k in enumerate(schema.entities.keys())}
        for artifact in artifacts:
            entity_refs = artifact.get_entities()
            found_invalid_key = False
            for ref in entity_refs:
                if ref.key not in schema.entities:
                    report.error(
                        "Invalid entity '%s' in artifact '%s'" % (ref.key, artifact.get_relative_path()))
                    found_invalid_key = True
            if found_invalid_key:
                # we cannot check the order of entities if invalid entity found
                continue
            # now, check if order of entities matches order in schema
            keys = list(map(lambda e: e.key, entity_refs))
            actual_keys_order = list(map(lambda k: expected_key_order[k], keys))
            for i in range(0, len(actual_keys_order) - 1):
                if actual_keys_order[i] > actual_keys_order[i + 1]:
                    expected = tuple(map(lambda k: expected_order_key[k], sorted(actual_keys_order)))
                    report.error(
                        "Invalid entities order: expected=%s, found=%s, artifact=%s" % (
                        expected, tuple(keys), artifact.get_relative_path()))
                    break


class SuffixesValidationRule(ValidationRule):
    def validate(self, schema: Schema, dataset: Dataset, report: ValidationReport, query: XPathQuery):
        pass
