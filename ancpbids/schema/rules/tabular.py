"""``rules.tabular_data``: TSV / TSV.GZ column rules."""
from ancpbids.model_base import Artifact

from ..context import sidecar
from ..session import selectors_match
from ..values import field_spec, missing_field, relpath, value_matches


def validate_tabular(session, report):
    for file in session.iter_files():
        extension = getattr(file, 'extension', None) or ''
        if extension not in ('.tsv', '.tsv.gz'):
            continue
        ctx = session.context(file, rich=True)
        columns = ctx.get('columns')
        if columns is None:
            continue
        for bound in session.tabular_rules.for_file(ctx.get('suffix'), ctx.get('datatype')):
            if not selectors_match(None, ctx, compiled=bound.selector_asts):
                continue
            apply_tabular_rule(bound.rule, columns, session, report, file)


def apply_tabular_rule(rule, columns, session, report, file):
    headers = list(columns)
    allowed = set()
    for key, spec in (rule.get('columns') or {}).items():
        header = (session.column_objects.get(key) or {}).get('name', key)
        allowed.add(header)
        level, issue = field_spec(spec)
        if header in columns:
            continue
        missing_field(level, issue, header, report, file, key_type='TSV_COLUMN')
    extras = [header for header in headers if header not in allowed]
    additional = rule.get('additional_columns')
    if additional == 'not_allowed' and extras:
        report.error(
            "Additional columns not allowed in '%s': %s" % (relpath(file), extras),
            file,
            code='TSV_ADDITIONAL_COLUMNS_NOT_ALLOWED')
    elif additional == 'allowed_if_defined' and extras:
        meta = sidecar(file) if isinstance(file, Artifact) else {}
        undefined = [header for header in extras if header not in meta]
        if undefined:
            report.error(
                "Additional columns require sidecar definitions in '%s': %s" % (
                    relpath(file), undefined),
                file,
                code='TSV_ADDITIONAL_COLUMNS_UNDEFINED')
    for key, spec in (rule.get('columns') or {}).items():
        header = (session.column_objects.get(key) or {}).get('name', key)
        if header not in columns:
            continue
        definition = session.column_objects.get(key) or {}
        for cell in columns[header]:
            if cell in (None, 'n/a'):
                continue
            if value_matches(cell, definition, session.format_patterns):
                continue
            report.error(
                "Invalid value in column '%s' of '%s'" % (header, relpath(file)),
                file,
                code='TSV_VALUE_INCORRECT',
                sub_code=header)
            break
    initial = rule.get('initial_columns') or []
    initial_headers = [
        (session.column_objects.get(key) or {}).get('name', key) for key in initial
    ]
    if initial_headers and headers[:len(initial_headers)] != initial_headers:
        report.error(
            "Invalid initial columns in '%s': expected=%s, found=%s" % (
                relpath(file), initial_headers, headers[:len(initial_headers)]),
            file,
            code='TSV_COLUMN_ORDER_INCORRECT')
    for key in rule.get('index_columns') or []:
        header = (session.column_objects.get(key) or {}).get('name', key)
        values = columns.get(header) or []
        if len(values) != len(set(values)):
            report.error(
                "Duplicate index column '%s' in '%s'" % (header, relpath(file)),
                file,
                code='TSV_INDEX_VALUE_NOT_UNIQUE',
                sub_code=header)
