"""``rules.files``: naming contracts and required core files."""
from ancpbids.model_base import Artifact

from ..values import entity_spec, relpath


def validate_files(session, report):
    for file in session.iter_files():
        identified = identify_filename_rules(file, session)
        if not identified:
            not_included(file, report)
            continue
        if isinstance(file, Artifact):
            validate_identified_rules(file, identified, session, report)
    files = list(session.iter_files())
    for rule in session.required_core:
        if any(core_rule_covers(rule, file) for file in files):
            continue
        missing = rule.get('path') or rule.get('stem')
        report.error(
            "Missing required file '%s'" % missing,
            session.dataset,
            code='MISSING_REQUIRED_FILE')
    for rule in session.recommended_core:
        if any(core_rule_covers(rule, file) for file in files):
            continue
        missing = rule.get('path') or rule.get('stem')
        report.warn(
            "Missing recommended file '%s'" % missing,
            session.dataset,
            code='MISSING_RECOMMENDED_FILE')


def identify_filename_rules(file, session):
    rules = []
    if isinstance(file, Artifact) and getattr(file, 'suffix', None):
        rules.extend(session.suffix_rules.get(file.suffix, ()))
    rel = relpath(file)
    for rule in session.path_rules:
        if path_matches(rule, rel):
            rules.append(rule)
    for rule in session.stem_rules:
        if stem_matches(rule, file.name):
            rules.append(rule)
    if len(rules) <= 1 or not isinstance(file, Artifact):
        return rules
    ctx = session.context(file, rich=False)
    datatype = ctx.get('datatype')
    by_datatype = [
        rule for rule in rules
        if rule.get('datatypes') and datatype in rule['datatypes']
    ]
    if by_datatype:
        rules = by_datatype
    if len(rules) <= 1:
        return rules
    by_entities = [
        rule for rule in rules
        if entities_extensions_in_rule(rule, file, session)
    ]
    if by_entities:
        return by_entities
    return rules


def entities_extensions_in_rule(rule, artifact, session):
    extensions = rule.get('extensions')
    if extensions is not None and artifact.extension not in extensions:
        return False
    rule_entities = rule.get('entities') or {}
    if not rule_entities:
        return True
    allowed = {
        session.entity_short.get(name, name) for name in rule_entities
    }
    return all(key in allowed for key in artifact.entities)


def validate_identified_rules(file, rules, session, report):
    ctx = session.context(file, rich=False)
    if len(rules) == 1:
        filename_rule_issues(rules[0], file, session, ctx, report)
        return
    clean = []
    for rule in rules:
        sink = []
        filename_rule_issues(rule, file, session, ctx, sink=sink)
        if not sink:
            clean.append(rule)
    if clean:
        return
    report.error(
        "All filename rules have issues for '%s'" % relpath(file),
        file,
        code='ALL_FILENAME_RULES_HAVE_ISSUES')


def filename_rule_issues(rule, file, session, ctx, report=None, sink=None):
    def add(code, message, sub_code=None):
        if sink is not None:
            sink.append(code)
            return
        report.error(message, file, code=code, sub_code=sub_code)

    rule_entities = rule.get('entities') or {}
    present = dict(file.entities)
    if rule_entities and not is_at_root(ctx):
        missing = []
        for long_name, spec in rule_entities.items():
            level, _enum = entity_spec(spec)
            short = session.entity_short.get(long_name)
            if short is None:
                continue
            if level == 'required' and short not in present:
                missing.append(short)
        if missing:
            add(
                'MISSING_REQUIRED_ENTITY',
                "Missing required entit%s %s in '%s'" % (
                    'y' if len(missing) == 1 else 'ies',
                    ', '.join(missing),
                    relpath(file)))
    if rule_entities:
        allowed = {
            session.entity_short.get(name, name) for name in rule_entities
        }
        extra = [key for key in present if key not in allowed]
        if extra:
            add(
                'ENTITY_NOT_IN_RULE',
                "Entit%s %s not allowed by filename rule in '%s'" % (
                    'y' if len(extra) == 1 else 'ies',
                    ', '.join(extra),
                    relpath(file)))
    extensions = rule.get('extensions')
    if extensions is not None and file.extension not in extensions:
        add(
            'EXTENSION_MISMATCH',
            "Extension '%s' does not match filename rule for '%s'" % (
                file.extension, relpath(file)))
    datatypes = rule.get('datatypes')
    if datatypes is not None and ctx.get('datatype') not in datatypes:
        add(
            'DATATYPE_MISMATCH',
            "Datatype '%s' does not match filename rule for '%s'" % (
                ctx.get('datatype'), relpath(file)))


def is_at_root(ctx):
    path = (ctx.get('path') or '').strip('/')
    return path != '' and '/' not in path


def path_matches(rule, rel):
    path = rule['path']
    return rel == path or rel.endswith('/' + path)


def stem_matches(rule, name):
    stem = rule['stem']
    for ext in rule.get('extensions') or ('',):
        if name == stem + ext:
            return True
    return False


def core_rule_covers(rule, file):
    rel = relpath(file)
    if 'path' in rule:
        return path_matches(rule, rel)
    if 'stem' in rule:
        return stem_matches(rule, file.name)
    return False


def not_included(file, report):
    rel = relpath(file)
    report.error(
        "Files with such naming scheme are not part of BIDS specification: '%s'" % rel,
        file,
        code='NOT_INCLUDED')
