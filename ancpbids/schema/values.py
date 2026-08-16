"""Schema value constraints and issue helpers."""
import re


def field_spec(spec):
    if isinstance(spec, dict):
        return spec.get('level', 'optional'), spec.get('issue')
    return spec, None


def entity_spec(spec):
    if isinstance(spec, dict):
        return spec.get('level', 'optional'), spec.get('enum')
    return spec, None


def field_level_code(key_type, level):
    if key_type == 'TSV_COLUMN':
        return 'TSV_COLUMN_MISSING'
    if level == 'required':
        return '%s_REQUIRED' % key_type
    if level == 'recommended':
        return '%s_RECOMMENDED' % key_type
    return None


def emit_issue(report, issue, file, fallback, default_level='error', default_code=None, sub_code=None):
    issue = issue or {}
    if not isinstance(issue, dict):
        issue = {}
    code = issue.get('code') or default_code
    level = issue.get('level') or default_level
    message = (issue.get('message') or fallback).strip()
    rel = relpath(file) if file is not None else ''
    if rel:
        message = '%s [%s]' % (message, rel)
    if level in ('warning', 'warn', 'recommended'):
        report.warn(message, file, code=code, sub_code=sub_code)
        return
    report.error(message, file, code=code, sub_code=sub_code)


def missing_field(level, issue, name, report, file, key_type='JSON_KEY'):
    if level not in ('required', 'recommended'):
        return
    fallback = "Missing %s metadata '%s'" % (level, name)
    emit_issue(
        report,
        issue,
        file,
        fallback,
        default_level=level,
        default_code=field_level_code(key_type, level),
        sub_code=name)


def value_matches(value, definition, format_patterns=None):
    if not definition:
        return True
    if 'anyOf' in definition:
        return any(
            value_matches(value, option, format_patterns)
            for option in definition['anyOf'])
    expected = definition.get('type')
    if expected and not json_type_matches(value, expected):
        return False
    enum_values = definition.get('enum')
    if enum_values is not None and value not in enum_values:
        return False
    if expected in ('number', 'integer') and isinstance(value, (int, float)) and not isinstance(value, bool):
        if 'minimum' in definition and value < definition['minimum']:
            return False
        if 'exclusiveMinimum' in definition and value <= definition['exclusiveMinimum']:
            return False
        if 'maximum' in definition and value > definition['maximum']:
            return False
        if 'exclusiveMaximum' in definition and value >= definition['exclusiveMaximum']:
            return False
    if expected == 'array' and isinstance(value, list):
        if 'minItems' in definition and len(value) < definition['minItems']:
            return False
        if 'maxItems' in definition and len(value) > definition['maxItems']:
            return False
        item_def = definition.get('items')
        if isinstance(item_def, dict):
            return all(value_matches(item, item_def, format_patterns) for item in value)
    if expected == 'object' and isinstance(value, dict):
        props = definition.get('properties') or {}
        for key, prop_def in props.items():
            if key not in value:
                continue
            if not value_matches(value[key], prop_def, format_patterns):
                return False
    pattern = definition.get('pattern')
    format_name = definition.get('format')
    if not pattern and format_name and format_patterns:
        pattern = format_patterns.get(format_name)
    if pattern and isinstance(value, str) and not re.fullmatch(pattern, value):
        return False
    return True


def json_type_matches(value, expected):
    if expected == 'string':
        return isinstance(value, str)
    if expected == 'number':
        if isinstance(value, bool):
            return False
        if isinstance(value, (int, float)):
            return True
        if isinstance(value, str):
            try:
                float(value)
                return True
            except ValueError:
                return False
        return False
    if expected == 'integer':
        if isinstance(value, bool):
            return False
        if isinstance(value, int):
            return True
        if isinstance(value, str) and re.fullmatch(r'-?\d+', value):
            return True
        return False
    if expected == 'boolean':
        return isinstance(value, bool)
    if expected == 'array':
        return isinstance(value, list)
    if expected == 'object':
        return isinstance(value, dict)
    return True


def relpath(node):
    return node.get_relative_path().replace('\\', '/')


def schema_path(node):
    rel = relpath(node)
    if not rel or rel in ('.',):
        return '/'
    return rel if rel.startswith('/') else '/' + rel
