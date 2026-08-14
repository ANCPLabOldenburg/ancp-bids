"""Schema-driven BIDS validator plugins.

One ``ValidationPlugin`` per ``schema.document`` rules section. Selectors use
the schema expression language; oracle is ``meta.expression_tests``.
"""
from ancpbids.plugin import ValidationPlugin
from ancpbids.schema import validate as schema_validate


class SchemaFilesPlugin(ValidationPlugin):
    """``rules.files``: naming contracts and required core files."""

    def execute(self, dataset, report: ValidationPlugin.ValidationReport):
        schema_validate.files(dataset, report)


class SchemaEntitiesPlugin(ValidationPlugin):
    """``rules.entities``: known keys and filename order."""

    def execute(self, dataset, report: ValidationPlugin.ValidationReport):
        schema_validate.entities(dataset, report)


class SchemaDirectoriesPlugin(ValidationPlugin):
    """``rules.directories``: folder tree and datatype names."""

    def execute(self, dataset, report: ValidationPlugin.ValidationReport):
        schema_validate.directories(dataset, report)


class SchemaSidecarsPlugin(ValidationPlugin):
    """``rules.sidecars``: sidecar metadata fields."""

    def execute(self, dataset, report: ValidationPlugin.ValidationReport):
        schema_validate.fields(dataset, report, 'sidecars', 'sidecar')


class SchemaJsonPlugin(ValidationPlugin):
    """``rules.json``: fields on JSON files themselves."""

    def execute(self, dataset, report: ValidationPlugin.ValidationReport):
        schema_validate.fields(dataset, report, 'json', 'json')


class SchemaTabularDataPlugin(ValidationPlugin):
    """``rules.tabular_data``: TSV columns."""

    def execute(self, dataset, report: ValidationPlugin.ValidationReport):
        schema_validate.tabular(dataset, report)


class SchemaDatasetMetadataPlugin(ValidationPlugin):
    """``rules.dataset_metadata``: dataset_description.json fields."""

    def execute(self, dataset, report: ValidationPlugin.ValidationReport):
        schema_validate.fields(dataset, report, 'dataset_metadata', 'json')


class SchemaChecksPlugin(ValidationPlugin):
    """``rules.checks``: expression checks and issue codes."""

    def execute(self, dataset, report: ValidationPlugin.ValidationReport):
        schema_validate.checks(dataset, report)
