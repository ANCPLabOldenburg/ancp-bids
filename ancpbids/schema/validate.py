"""Execute ``schema.document`` rules against a dataset graph.

Public entry points used by ``plugin_schema_validator``. Implementation lives in:

- ``session`` — shared validation session and selector indexing
- ``context`` — rich file context (sidecar, columns, associations, headers)
- ``values`` — value constraints and issue helpers
- ``rules`` — one module per schema rule family
"""
from .context import load_binary_headers as _load_binary_headers
from .rules.checks import validate_checks
from .rules.directories import validate_directories
from .rules.entities import validate_entities
from .rules.fields import validate_fields
from .rules.files import validate_files
from .rules.tabular import validate_tabular
from .session import get_session
from .values import value_matches as _value_matches


def files(dataset, report):
    validate_files(get_session(report, dataset), report)


def entities(dataset, report):
    validate_entities(get_session(report, dataset), report)


def directories(dataset, report):
    validate_directories(get_session(report, dataset), report)


def fields(dataset, report, section, data_key):
    validate_fields(get_session(report, dataset), report, section, data_key)


def tabular(dataset, report):
    validate_tabular(get_session(report, dataset), report)


def checks(dataset, report):
    validate_checks(get_session(report, dataset), report)
