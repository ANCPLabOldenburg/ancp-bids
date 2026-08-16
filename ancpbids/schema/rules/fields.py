"""Field rules for sidecars, JSON files, and dataset_metadata."""
from ..session import selectors_match
from ..values import field_spec, missing_field, relpath, value_matches

DERIVATIVE_SELECTOR = 'dataset.dataset_description.DatasetType == "derivative"'


def validate_fields(session, report, section, data_key):
    index = {
        'sidecars': session.sidecar_rules,
        'json': session.json_rules,
        'dataset_metadata': session.dataset_metadata_rules,
    }[section]
    key_type = 'SIDECAR_KEY' if section == 'sidecars' else 'JSON_KEY'
    objects = session.metadata_objects
    for file in session.iter_files():
        ctx = session.context(file, rich=True)
        data = ctx.get(data_key) or {}
        for bound in index.for_file(ctx.get('suffix'), ctx.get('datatype')):
            if not selectors_match(None, ctx, compiled=bound.selector_asts):
                continue
            apply_fields(
                bound.rule.get('fields') or {},
                data,
                objects,
                report,
                file,
                key_type,
                rule=bound.rule,
                ctx=ctx)


def apply_fields(fields, data, objects, report, file, key_type='JSON_KEY', rule=None, ctx=None):
    for name, spec in fields.items():
        level, issue = field_spec(spec)
        present = isinstance(data, dict) and name in data and data[name] is not None
        if not present:
            if (
                key_type == 'SIDECAR_KEY'
                and skip_derivative_sidecar_missing(ctx, rule)
            ):
                continue
            missing_field(level, issue, name, report, file, key_type=key_type)
            continue
        if level == 'deprecated':
            report.warn(
                "Deprecated metadata '%s' in '%s'" % (name, relpath(file)),
                file,
                code='SIDECAR_KEY_DEPRECATED' if key_type == 'SIDECAR_KEY' else 'JSON_KEY_DEPRECATED',
                sub_code=name)
        definition = objects.get(name) or {}
        session = getattr(report, '_schema_session', None)
        patterns = session.format_patterns if session is not None else {}
        if value_matches(data[name], definition, patterns):
            continue
        report.error(
            "Invalid type for '%s' in '%s'" % (name, relpath(file)),
            file,
            code='JSON_SCHEMA_VALIDATION_ERROR',
            sub_code=name)


def skip_derivative_sidecar_missing(ctx, rule):
    if not ctx or not rule:
        return False
    description = (ctx.get('dataset') or {}).get('dataset_description') or {}
    if description.get('DatasetType') != 'derivative':
        return False
    selectors = rule.get('selectors') or ()
    return DERIVATIVE_SELECTOR not in selectors
