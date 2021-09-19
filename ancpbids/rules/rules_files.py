import lxml.etree
from yamale import YamaleError

from ancpbids import XPathQuery, model
from ancpbids.model import Dataset
from ancpbids.schema import Schema
from ancpbids.validator import ValidationRule, ValidationReport

from lxml.isoschematron import Schematron
import os
import yamale


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
        try:
            schema = yamale.make_schema(content=model.YAMALE_SCHEMA)
            yamale.validate(schema, [({'Dataset': dataset}, None)])
        except YamaleError as e:
            for result in e.results:
                for error in result.errors:
                    report.error(error)


class DatatypesValidationRule(ValidationRule):
    def validate(self, schema: Schema, dataset: Dataset, report: ValidationReport, **kwargs):
        invalid = []
        valid_datatypes = schema.datatypes.keys()
        for subject in dataset.subjects:
            invalid.extend([f for f in subject.datatypes if f.name not in valid_datatypes])
            for session in subject.sessions:
                invalid.extend([f for f in session.datatypes if f.name not in valid_datatypes])

        for folder in invalid:
            report.error("Unsupported datatype folder '%s'" % folder.get_relative_path())


class EntitiesValidationRule(ValidationRule):
    def validate(self, schema: Schema, dataset: Dataset, report: ValidationReport, query: XPathQuery):
        artifacts = query.execute('//entities/..')
        entities = list(map(lambda e: e['entity'], schema.entities.values()))
        expected_key_order = {k: i for i, k in enumerate(entities)}
        expected_order_key = {i: k for i, k in enumerate(entities)}
        for artifact in artifacts:
            entity_refs = artifact.entities
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
