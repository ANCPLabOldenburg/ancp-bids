"""``rules.entities``: known keys, label formats, and filename order."""
import re

from ..values import relpath


def validate_entities(session, report):
    for artifact in session.dataset.select(session.schema.Artifact).objects():
        keys = list(artifact.entities)
        unknown = [key for key in keys if key not in session.known_short]
        if unknown:
            rel = relpath(artifact)
            for key in unknown:
                report.error(
                    "Invalid entity '%s' in artifact '%s'" % (key, rel),
                    artifact,
                    code='ENTITY_NOT_IN_RULE',
                    sub_code=key)
            continue
        for key, value in artifact.entities.items():
            check_entity_label(session, report, artifact, key, value)
        if not entity_order_error(keys, session.ordered_short):
            continue
        expected = tuple(sorted(keys, key=session.ordered_short.index))
        report.error(
            "Invalid entities order: expected=%s, found=%s, artifact=%s" % (
                expected, tuple(keys), relpath(artifact)),
            artifact,
            code='FILENAME_MISMATCH')


def check_entity_label(session, report, artifact, short_key, value):
    long_name = session.entity_long.get(short_key)
    definition = session.entity_defs.get(long_name) or {}
    format_name = definition.get('format')
    pattern = session.format_patterns.get(format_name)
    if not pattern:
        return
    if re.fullmatch(pattern, str(value)):
        return
    report.error(
        "Invalid entity label '%s-%s' in '%s'" % (short_key, value, relpath(artifact)),
        artifact,
        code='INVALID_ENTITY_LABEL',
        sub_code=short_key)


def entity_order_error(keys, ordered_short):
    if len(keys) < 2:
        return False
    ranks = [ordered_short.index(key) for key in keys]
    return ranks != sorted(ranks)
