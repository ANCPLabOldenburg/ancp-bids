import lxml.etree

from ancpbids import XPathQuery
from ancpbids.model import Dataset, GdsCollector_, Session, Subject, Datatype
from ancpbids.schema import Schema
from ancpbids.validator import ValidationRule, ValidationReport

from lxml.isoschematron import Schematron
import os


class SchematronValidationRule(ValidationRule):
    def validate(self, dataset: Dataset, report: ValidationReport, **kwargs):
        schema = dataset._schema
        schematron_rules_dir = schema.schema_path + "/validation-rules"
        xml_tree = dataset.to_etree(nsmap_=schema.ns_map)
        for root_dir, dirs, files in os.walk(schematron_rules_dir):
            for file in files:
                if file.endswith(".xml"):
                    file_abs_path = os.path.join(root_dir, file)
                    schematron = Schematron(file=file_abs_path, error_finder=Schematron.ASSERTS_AND_REPORTS)
                    schematron.validate(xml_tree)
                    for error in schematron.error_log:
                        message_xml = lxml.etree.XML(error.message)
                        role = message_xml.attrib['role'] if 'role' in message_xml.attrib else 'error'
                        getattr(report, role)(message_xml[0].text)



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
        entities = list(map(lambda e: e['entity'], schema.entities.values()))
        expected_key_order = {k: i for i, k in enumerate(entities)}
        expected_order_key = {i: k for i, k in enumerate(entities)}
        for artifact in artifacts:
            entity_refs = artifact.get_entities()
            found_invalid_key = False
            for ref in entity_refs:
                if ref.key not in entities:
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
