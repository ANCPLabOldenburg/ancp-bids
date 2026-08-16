"""``rules.directories``: folder tree and datatype names."""
from ancpbids.model_base import Folder

from ..values import relpath


def validate_directories(session, report):
    # Older schema versions (e.g. 1.8/1.9) omit rules.directories entirely.
    trees = session.document.get('rules', {}).get('directories') or {}
    if not trees:
        return
    dtype = session.dataset_description.get('DatasetType') or 'raw'
    if dtype in ('derivative', 'derivatives'):
        deriv_tree = trees.get('derivative')
        if deriv_tree:
            check_tree(session.dataset, deriv_tree, report, session)
        return
    raw_tree = trees.get('raw')
    if raw_tree:
        check_tree(session.dataset, raw_tree, report, session)
    deriv_root = session.dataset.derivatives
    if not deriv_root:
        return
    deriv_tree = trees.get('derivative')
    if not deriv_tree:
        return
    for child in deriv_root.folders or []:
        check_tree(child, deriv_tree, report, session)


def check_tree(folder, tree, report, session):
    check_children(folder, tree, tree.get('root', {}).get('subdirs') or [], report, session)


def check_children(folder, tree, allowed_keys, report, session):
    named, entity_rules, has_datatype = classify_allowed(tree, allowed_keys)
    for child in child_folders(folder):
        if child.name.startswith('.'):
            continue
        spec = named.get(child.name)
        if spec is not None:
            if spec.get('opaque'):
                continue
            check_children(child, tree, spec.get('subdirs') or [], report, session)
            continue
        entity_spec = matching_entity_rule(child.name, entity_rules, session)
        if entity_spec is not None:
            if entity_spec.get('opaque'):
                continue
            check_children(child, tree, entity_spec.get('subdirs') or [], report, session)
            continue
        if has_datatype and child.name in session.datatypes:
            continue
        if has_datatype:
            report.error(
                "Unsupported datatype folder '%s'" % relpath(child),
                child,
                code='DATATYPE_MISMATCH')
            continue
        report.error(
            "Unsupported folder '%s'" % relpath(child),
            child,
            code='INVALID_LOCATION')


def classify_allowed(tree, allowed_keys):
    named = {}
    entity_rules = []
    has_datatype = False
    for key in expand_subdir_keys(allowed_keys):
        spec = tree.get(key)
        if not spec:
            continue
        if spec.get('value') == 'datatype':
            has_datatype = True
            continue
        if 'entity' in spec:
            entity_rules.append(spec)
            continue
        if 'name' in spec:
            named[spec['name']] = spec
    return named, entity_rules, has_datatype


def expand_subdir_keys(keys):
    result = []
    for key in keys:
        if isinstance(key, dict) and 'oneOf' in key:
            result.extend(key['oneOf'])
            continue
        result.append(key)
    return result


def matching_entity_rule(name, entity_rules, session):
    for spec in entity_rules:
        prefix = session.entity_short.get(spec['entity'], spec['entity']) + '-'
        if name.startswith(prefix) and len(name) > len(prefix):
            return spec
    return None


def child_folders(folder):
    children = []
    seen = set()
    for attr in ('folders', 'subjects', 'sessions', 'datatypes'):
        for child in getattr(folder, attr, None) or []:
            if not isinstance(child, Folder) or id(child) in seen:
                continue
            seen.add(id(child))
            children.append(child)
    return children
