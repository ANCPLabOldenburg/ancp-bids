"""Schema-driven BIDS validator plugins.

One ``ValidationPlugin`` per ``schema.document`` rules section. Selectors use
the schema expression language; oracle is ``meta.expression_tests``.
"""
from ancpbids.plugin import ValidationPlugin, plugin
from ancpbids.schema import validate as schema_validate


@plugin(ranking=0, system=True)
class SchemaFilesPlugin(ValidationPlugin):
    """``rules.files``: naming contracts and required core files."""

    def execute(self, dataset, report: ValidationPlugin.ValidationReport):
        schema_validate.files(dataset, report)


@plugin(ranking=0, system=True)
class SchemaEntitiesPlugin(ValidationPlugin):
    """``rules.entities``: known keys and filename order."""

    def execute(self, dataset, report: ValidationPlugin.ValidationReport):
        schema_validate.entities(dataset, report)


@plugin(ranking=0, system=True)
class SchemaDirectoriesPlugin(ValidationPlugin):
    """``rules.directories``: folder tree and datatype names."""

    def execute(self, dataset, report: ValidationPlugin.ValidationReport):
        schema_validate.directories(dataset, report)


@plugin(ranking=0, system=True)
class SchemaSidecarsPlugin(ValidationPlugin):
    """``rules.sidecars``: sidecar metadata fields."""

    def execute(self, dataset, report: ValidationPlugin.ValidationReport):
        schema_validate.fields(dataset, report, 'sidecars', 'sidecar')


@plugin(ranking=0, system=True)
class SchemaJsonPlugin(ValidationPlugin):
    """``rules.json``: fields on JSON files themselves."""

    def execute(self, dataset, report: ValidationPlugin.ValidationReport):
        schema_validate.fields(dataset, report, 'json', 'json')


@plugin(ranking=0, system=True)
class SchemaTabularDataPlugin(ValidationPlugin):
    """``rules.tabular_data``: TSV columns."""

    def execute(self, dataset, report: ValidationPlugin.ValidationReport):
        schema_validate.tabular(dataset, report)


@plugin(ranking=0, system=True)
class SchemaDatasetMetadataPlugin(ValidationPlugin):
    """``rules.dataset_metadata``: dataset_description.json fields."""

    def execute(self, dataset, report: ValidationPlugin.ValidationReport):
        schema_validate.fields(dataset, report, 'dataset_metadata', 'json')


@plugin(ranking=0, system=True)
class SchemaChecksPlugin(ValidationPlugin):
    """``rules.checks``: expression checks and issue codes."""

    def execute(self, dataset, report: ValidationPlugin.ValidationReport):
        schema_validate.checks(dataset, report)
