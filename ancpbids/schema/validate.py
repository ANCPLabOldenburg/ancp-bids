"""Execute ``schema.document`` rules against a dataset graph."""
import os
from collections import defaultdict

from ancpbids.model_base import Artifact, DatatypeFolder, DerivativeFolder, Folder

from .expr import evaluate


def files(dataset, report):
    _validate_files(_session(report, dataset), report)


def entities(dataset, report):
    _validate_entities(_session(report, dataset), report)


def directories(dataset, report):
    _validate_directories(_session(report, dataset), report)


def fields(dataset, report, section, data_key):
    _validate_fields(_session(report, dataset), report, section, data_key)


def tabular(dataset, report):
    _validate_tabular(_session(report, dataset), report)


def checks(dataset, report):
    _validate_checks(_session(report, dataset), report)


# --- shared session ------------------------------------------------------------

def _session(report, dataset):
    sess = getattr(report, '_schema_session', None)
    if sess is None or sess.dataset is not dataset:
        sess = _ValidationSession(dataset)
        report._schema_session = sess
    return sess


class _FileIndex:
    def __init__(self, dataset):
        self.paths = set()
        self.root_names = set()
        self.basenames = set()
        self.stimuli = set()
        schema = dataset.get_schema()
        for file in dataset.select(schema.File).objects():
            rel = _relpath(file)
            schema_path = _schema_path(file)
            self.paths.add(rel)
            self.paths.add(schema_path)
            self.basenames.add(file.name)
            if '/' not in rel:
                self.root_names.add(file.name)
            if rel.startswith('stimuli/'):
                self.stimuli.add(rel[len('stimuli/'):])
                self.stimuli.add(file.name)

    def count(self, arg, rule, ctx):
        items = arg if isinstance(arg, list) else [arg]
        return sum(1 for item in items if item is not None and self._exists_one(item, rule, ctx))

    def _exists_one(self, item, rule, ctx):
        item = str(item)
        if rule == 'bids-uri':
            return item.startswith('bids:')
        if rule == 'dataset':
            return self._has_dataset(item)
        if rule == 'file':
            return self._has_file(item)
        if rule == 'stimuli':
            return item in self.stimuli or self._has_dataset('stimuli/' + item)
        if rule == 'subject':
            subject = (ctx.get('entities') or {}).get('subject')
            if not subject:
                return False
            return self._has_dataset('sub-%s/%s' % (subject, item)) or self._has_file(item)
        return False

    def _has_dataset(self, item):
        item = item.lstrip('/')
        return item in self.paths or '/' + item in self.paths or item in self.root_names

    def _has_file(self, item):
        item = item.lstrip('/')
        if self._has_dataset(item):
            return True
        suffix = '/' + item
        return any(path.endswith(suffix) or path.endswith(item) for path in self.paths)


class _ValidationSession:
    def __init__(self, dataset):
        self.dataset = dataset
        self.schema = dataset.get_schema()
        self.document = self.schema.document
        objects = self.document['objects']
        self.datatypes = set(objects['datatypes'])
        self.entity_short = {
            name: spec['name'] for name, spec in objects['entities'].items()
        }
        self.entity_long = {short: name for name, short in self.entity_short.items()}
        self.ordered_short = [
            self.entity_short[name] for name in self.document['rules']['entities']
            if name in self.entity_short
        ]
        self.known_short = set(self.ordered_short)
        self.metadata_objects = objects.get('metadata') or {}
        self.column_objects = objects.get('columns') or {}
        self.files_index = _FileIndex(dataset)
        self.dataset_description = _json_contents(dataset.dataset_description)
        self.suffix_rules = defaultdict(list)
        self.path_rules = []
        self.stem_rules = []
        self.required_core = []
        self._load_file_rules(self.document['rules']['files'])
        self.sidecar_rules = list(_rule_leaves(self.document['rules'].get('sidecars')))
        self.json_rules = list(_rule_leaves(self.document['rules'].get('json')))
        self.tabular_rules = list(_rule_leaves(self.document['rules'].get('tabular_data')))
        self.dataset_metadata_rules = list(
            _rule_leaves(self.document['rules'].get('dataset_metadata')))
        self.check_rules = list(_rule_leaves(self.document['rules'].get('checks')))
        self._contexts = {}
        self.dataset_ctx = self._build_dataset_context()

    def _load_file_rules(self, node):
        if not isinstance(node, dict):
            return
        if _is_file_rule(node):
            self._register_file_rule(node)
            return
        for child in node.values():
            self._load_file_rules(child)

    def _register_file_rule(self, rule):
        if rule.get('level') == 'required' and _is_core_file_rule(rule):
            self.required_core.append(rule)
        if 'path' in rule:
            self.path_rules.append(rule)
            return
        if 'stem' in rule:
            self.stem_rules.append(rule)
            return
        for suffix in rule.get('suffixes') or ():
            self.suffix_rules[suffix].append(rule)

    def _build_dataset_context(self):
        subjects = list(self.dataset.subjects or [])
        sub_dirs = [subject.name for subject in subjects]
        participant_id = None
        participants = getattr(self.dataset, 'participants_tsv', None)
        columns = _load_columns(participants) if participants else None
        if columns and 'participant_id' in columns:
            participant_id = columns['participant_id']
        present = sorted({
            folder.name for folder in self.dataset.select(self.schema.DatatypeFolder).objects()
            if folder.name in self.datatypes
        })
        return {
            'dataset_description': self.dataset_description,
            'datatypes': present,
            'modalities': _modalities_for(present, self.document),
            'subjects': {'sub_dirs': sub_dirs, 'participant_id': participant_id},
            'ignored': [],
        }

    def iter_files(self):
        for file in self.dataset.select(self.schema.File).objects():
            if not file.name.startswith('.'):
                yield file

    def context(self, file, rich=False):
        cache_key = (id(file), rich)
        cached = self._contexts.get(cache_key)
        if cached is not None:
            return cached
        ctx = _basic_context(file, self)
        if rich:
            ctx = dict(ctx)
            ctx['sidecar'] = _sidecar(file)
            ctx['json'] = _load_json(file)
            ctx['columns'] = _load_columns(file)
            ctx['associations'] = _associations(file, self, ctx)
            ctx['size'] = _file_size(file)
        self._contexts[cache_key] = ctx
        return ctx


def _rule_leaves(node):
    if not isinstance(node, dict):
        return
    if _is_leaf_rule(node):
        yield node
        return
    for child in node.values():
        yield from _rule_leaves(child)


def _is_leaf_rule(node):
    return any(key in node for key in ('fields', 'columns', 'checks', 'selectors')) and (
        'fields' in node or 'columns' in node or 'checks' in node)


def _is_file_rule(node):
    return any(key in node for key in ('suffixes', 'extensions', 'entities', 'path', 'stem'))


def _is_core_file_rule(rule):
    if 'stem' in rule:
        return True
    path = rule.get('path')
    return bool(path) and '.' in path.rsplit('/', 1)[-1]


def _json_contents(file):
    if file is None:
        return {}
    value = getattr(file, 'contents', None)
    if value is None and hasattr(file, 'load_contents'):
        value = file.load_contents()
    return value if isinstance(value, dict) else {}


def _load_json(file):
    if file is None or not file.name.endswith('.json'):
        return None
    return _json_contents(file)


def _load_columns(file):
    if file is None or not file.name.endswith('.tsv'):
        return None
    rows = getattr(file, 'contents', None)
    if rows is None and hasattr(file, 'load_contents'):
        rows = file.load_contents()
    if not isinstance(rows, list) or not rows:
        return {}
    if not isinstance(rows[0], dict):
        return {}
    return {key: [row.get(key) for row in rows] for key in rows[0]}


def _sidecar(file):
    if not isinstance(file, Artifact):
        return {}
    try:
        return file.get_metadata() or {}
    except Exception:
        return {}


def _file_size(file):
    try:
        return os.path.getsize(file.get_absolute_path())
    except OSError:
        return None


def _modalities_for(datatypes, document):
    found = []
    for name, spec in (document['rules'].get('modalities') or {}).items():
        if any(dt in datatypes for dt in spec.get('datatypes') or ()):
            found.append(name)
    return found


def _basic_context(file, session):
    entities = {}
    if isinstance(file, Artifact):
        for key, value in file.entities.items():
            entities[session.entity_long.get(key, key)] = value
    description = _local_dataset_description(file, session.dataset_description)
    dataset_ctx = dict(session.dataset_ctx)
    dataset_ctx['dataset_description'] = description
    return {
        'path': _schema_path(file),
        'suffix': getattr(file, 'suffix', None),
        'extension': file.extension,
        'datatype': _datatype(file),
        'modality': _modality(_datatype(file), session.document),
        'entities': entities,
        'sidecar': {},
        'json': None,
        'columns': None,
        'associations': {},
        'nifti_header': None,
        'gzip': None,
        'dataset': dataset_ctx,
        'schema': session.document,
        'size': None,
        '_files': session.files_index,
    }


def _local_dataset_description(file, root_description):
    current = file
    while current is not None:
        if isinstance(current, DerivativeFolder):
            contents = _json_contents(current.dataset_description)
            return contents or {'DatasetType': 'derivative'}
        current = getattr(current, 'parent_object_', None)
    return root_description


def _datatype(file):
    value = getattr(file, 'datatype', None)
    if value:
        return value
    current = file.get_parent()
    while current is not None:
        if isinstance(current, DatatypeFolder):
            return current.name
        current = current.get_parent()
    return None


def _modality(datatype, document):
    if not datatype:
        return None
    for name, spec in (document['rules'].get('modalities') or {}).items():
        if datatype in (spec.get('datatypes') or ()):
            return name
    return None


def _associations(file, session, ctx):
    result = {}
    for name, rule in (session.document.get('meta', {}).get('associations') or {}).items():
        if not _selectors_match(rule.get('selectors'), ctx):
            result[name] = None
            continue
        found = _find_associated(file, rule.get('target') or {}, rule.get('inherit', False))
        result[name] = _association_context(found)
    return result


def _find_associated(file, target, inherit):
    suffix = target.get('suffix')
    extensions = target.get('extension')
    if isinstance(extensions, str):
        extensions = [extensions]
    current = file.get_parent()
    while current is not None:
        match = _associated_in_folder(file, current, suffix, extensions)
        if match is not None:
            return match
        if not inherit:
            return None
        current = current.get_parent()
    return None


def _associated_in_folder(file, folder, suffix, extensions):
    file_ents = file.get_entities() if isinstance(file, Artifact) else {}
    for candidate in folder.files or []:
        if candidate is file:
            continue
        if suffix and getattr(candidate, 'suffix', None) != suffix:
            continue
        if extensions and candidate.extension not in extensions:
            continue
        if isinstance(candidate, Artifact) and file_ents:
            cand_ents = candidate.get_entities()
            if not cand_ents.items() <= file_ents.items():
                continue
        return candidate
    return None


def _association_context(file):
    if file is None:
        return None
    ctx = {'path': _schema_path(file), 'n_rows': None}
    columns = _load_columns(file)
    if columns:
        ctx['n_rows'] = len(next(iter(columns.values())))
        ctx.update(columns)
    return ctx


def _selectors_match(selectors, context):
    if not selectors:
        return True
    for expr in selectors:
        if _safe_eval(expr, context) is not True:
            return False
    return True


def _safe_eval(expression, context):
    try:
        return evaluate(expression, context)
    except Exception:
        return None


# --- rules.files --------------------------------------------------------------

def _validate_files(session, report):
    for file in session.iter_files():
        if isinstance(file, Artifact):
            if _matches_any_suffix_rule(file, session):
                continue
            if _matches_path_or_stem(file, session):
                continue
            _not_included(file, report)
            continue
        if _matches_path_or_stem(file, session):
            continue
        _not_included(file, report)
    files = list(session.iter_files())
    for rule in session.required_core:
        if any(_core_rule_covers(rule, file) for file in files):
            continue
        missing = rule.get('path') or rule.get('stem')
        report.error("Missing required file '%s'" % missing, session.dataset)


def _matches_any_suffix_rule(artifact, session):
    context = session.context(artifact, rich=False)
    for rule in session.suffix_rules.get(artifact.suffix, ()):
        if _file_rule_matches(rule, artifact, context, session):
            return True
    return False


def _file_rule_matches(rule, artifact, context, session):
    if not _selectors_match(rule.get('selectors'), context):
        return False
    extensions = rule.get('extensions')
    if extensions is not None and artifact.extension not in extensions:
        return False
    datatypes = rule.get('datatypes')
    if datatypes is not None and context['datatype'] not in datatypes:
        return False
    return _entities_match(rule.get('entities') or {}, artifact, session)


def _entities_match(rule_entities, artifact, session):
    present = dict(artifact.entities)
    allowed = set()
    for long_name, spec in rule_entities.items():
        short = session.entity_short.get(long_name)
        if short is None:
            return False
        allowed.add(short)
        level, enum_values = _entity_spec(spec)
        if level == 'required' and short not in present:
            return False
        if enum_values is not None and short in present:
            if str(present[short]) not in enum_values:
                return False
    return all(key in allowed for key in present)


def _matches_path_or_stem(file, session):
    rel = _relpath(file)
    for rule in session.path_rules:
        if _path_matches(rule, rel):
            return True
    for rule in session.stem_rules:
        if _stem_matches(rule, file.name):
            return True
    return False


def _path_matches(rule, rel):
    path = rule['path']
    return rel == path or rel.endswith('/' + path)


def _stem_matches(rule, name):
    stem = rule['stem']
    for ext in rule.get('extensions') or ('',):
        if name == stem + ext:
            return True
    return False


def _core_rule_covers(rule, file):
    rel = _relpath(file)
    if 'path' in rule:
        return _path_matches(rule, rel)
    if 'stem' in rule:
        return _stem_matches(rule, file.name)
    return False


def _not_included(file, report):
    rel = _relpath(file)
    report.error(
        "Files with such naming scheme are not part of BIDS specification: '%s'" % rel,
        file,
        code='NOT_INCLUDED')


# --- rules.entities -----------------------------------------------------------

def _validate_entities(session, report):
    for artifact in session.dataset.select(session.schema.Artifact).objects():
        keys = list(artifact.entities)
        unknown = [key for key in keys if key not in session.known_short]
        if unknown:
            rel = _relpath(artifact)
            for key in unknown:
                report.error(
                    "Invalid entity '%s' in artifact '%s'" % (key, rel), artifact)
            continue
        if not _entity_order_error(keys, session.ordered_short):
            continue
        expected = tuple(sorted(keys, key=session.ordered_short.index))
        report.error(
            "Invalid entities order: expected=%s, found=%s, artifact=%s" % (
                expected, tuple(keys), _relpath(artifact)),
            artifact)


def _entity_order_error(keys, ordered_short):
    if len(keys) < 2:
        return False
    ranks = [ordered_short.index(key) for key in keys]
    return ranks != sorted(ranks)


# --- rules.directories --------------------------------------------------------

def _validate_directories(session, report):
    trees = session.document['rules']['directories']
    dtype = session.dataset_description.get('DatasetType') or 'raw'
    if dtype in ('derivative', 'derivatives'):
        _check_tree(session.dataset, trees['derivative'], report, session)
        return
    _check_tree(session.dataset, trees['raw'], report, session)
    deriv_root = session.dataset.derivatives
    if not deriv_root:
        return
    for child in deriv_root.folders or []:
        _check_tree(child, trees['derivative'], report, session)


def _check_tree(folder, tree, report, session):
    _check_children(folder, tree, tree.get('root', {}).get('subdirs') or [], report, session)


def _check_children(folder, tree, allowed_keys, report, session):
    named, entity_rules, has_datatype = _classify_allowed(tree, allowed_keys)
    for child in _child_folders(folder):
        if child.name.startswith('.'):
            continue
        spec = named.get(child.name)
        if spec is not None:
            if spec.get('opaque'):
                continue
            _check_children(child, tree, spec.get('subdirs') or [], report, session)
            continue
        entity_spec = _matching_entity_rule(child.name, entity_rules, session)
        if entity_spec is not None:
            if entity_spec.get('opaque'):
                continue
            _check_children(child, tree, entity_spec.get('subdirs') or [], report, session)
            continue
        if has_datatype and child.name in session.datatypes:
            continue
        if has_datatype:
            report.error("Unsupported datatype folder '%s'" % _relpath(child), child)
            continue
        report.error("Unsupported folder '%s'" % _relpath(child), child)


def _classify_allowed(tree, allowed_keys):
    named = {}
    entity_rules = []
    has_datatype = False
    for key in _expand_subdir_keys(allowed_keys):
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


def _expand_subdir_keys(keys):
    result = []
    for key in keys:
        if isinstance(key, dict) and 'oneOf' in key:
            result.extend(key['oneOf'])
            continue
        result.append(key)
    return result


def _matching_entity_rule(name, entity_rules, session):
    for spec in entity_rules:
        prefix = session.entity_short.get(spec['entity'], spec['entity']) + '-'
        if name.startswith(prefix) and len(name) > len(prefix):
            return spec
    return None


def _child_folders(folder):
    children = []
    seen = set()
    for attr in ('folders', 'subjects', 'sessions', 'datatypes'):
        for child in getattr(folder, attr, None) or []:
            if not isinstance(child, Folder) or id(child) in seen:
                continue
            seen.add(id(child))
            children.append(child)
    return children


# --- field rules (sidecars / json / dataset_metadata) -------------------------

def _validate_fields(session, report, section, data_key):
    rules = {
        'sidecars': session.sidecar_rules,
        'json': session.json_rules,
        'dataset_metadata': session.dataset_metadata_rules,
    }[section]
    objects = session.metadata_objects
    for file in session.iter_files():
        ctx = session.context(file, rich=True)
        data = ctx.get(data_key) or {}
        for rule in rules:
            if not _selectors_match(rule.get('selectors'), ctx):
                continue
            _apply_fields(rule.get('fields') or {}, data, objects, report, file)


def _apply_fields(fields, data, objects, report, file):
    for name, spec in fields.items():
        level, issue = _field_spec(spec)
        present = isinstance(data, dict) and name in data and data[name] is not None
        if not present:
            _missing_field(level, issue, name, report, file)
            continue
        if level == 'deprecated':
            report.warn("Deprecated metadata '%s' in '%s'" % (name, _relpath(file)), file)
        definition = objects.get(name) or {}
        if _value_matches(data[name], definition):
            continue
        report.error(
            "Invalid type for '%s' in '%s'" % (name, _relpath(file)),
            file,
            code='JSON_SCHEMA_VALIDATION_ERROR')


def _missing_field(level, issue, name, report, file):
    if level not in ('required', 'recommended'):
        return
    fallback = "Missing %s metadata '%s'" % (level, name)
    _emit_issue(report, issue, file, fallback, default_level=level)


# --- rules.tabular_data -------------------------------------------------------

def _validate_tabular(session, report):
    for file in session.iter_files():
        if not file.name.endswith('.tsv'):
            continue
        ctx = session.context(file, rich=True)
        columns = ctx.get('columns')
        if columns is None:
            continue
        for rule in session.tabular_rules:
            if not _selectors_match(rule.get('selectors'), ctx):
                continue
            _apply_tabular_rule(rule, columns, session, report, file)


def _apply_tabular_rule(rule, columns, session, report, file):
    headers = list(columns)
    allowed = set()
    for key, spec in (rule.get('columns') or {}).items():
        header = (session.column_objects.get(key) or {}).get('name', key)
        allowed.add(header)
        level, issue = _field_spec(spec)
        if header in columns:
            continue
        _missing_field(level, issue, header, report, file)
    extras = [header for header in headers if header not in allowed]
    additional = rule.get('additional_columns')
    if additional == 'not_allowed' and extras:
        report.error(
            "Additional columns not allowed in '%s': %s" % (_relpath(file), extras),
            file)
    initial = rule.get('initial_columns') or []
    initial_headers = [
        (session.column_objects.get(key) or {}).get('name', key) for key in initial
    ]
    if initial_headers and headers[:len(initial_headers)] != initial_headers:
        report.error(
            "Invalid initial columns in '%s': expected=%s, found=%s" % (
                _relpath(file), initial_headers, headers[:len(initial_headers)]),
            file)
    for key in rule.get('index_columns') or []:
        header = (session.column_objects.get(key) or {}).get('name', key)
        values = columns.get(header) or []
        if len(values) != len(set(values)):
            report.error("Duplicate index column '%s' in '%s'" % (header, _relpath(file)), file)


# --- rules.checks -------------------------------------------------------------

def _validate_checks(session, report):
    for file in session.iter_files():
        ctx = session.context(file, rich=True)
        for rule in session.check_rules:
            if not _selectors_match(rule.get('selectors'), ctx):
                continue
            if _checks_pass(rule.get('checks') or [], ctx):
                continue
            _emit_issue(report, rule.get('issue') or {}, file, 'Schema check failed')


def _checks_pass(checks, ctx):
    for expr in checks:
        if _safe_eval(expr, ctx) is False:
            return False
    return True


# --- reporting / path helpers -------------------------------------------------

def _field_spec(spec):
    if isinstance(spec, dict):
        return spec.get('level', 'optional'), spec.get('issue')
    return spec, None


def _entity_spec(spec):
    if isinstance(spec, dict):
        return spec.get('level', 'optional'), spec.get('enum')
    return spec, None


def _emit_issue(report, issue, file, fallback, default_level='error'):
    issue = issue or {}
    if not isinstance(issue, dict):
        issue = {}
    code = issue.get('code')
    level = issue.get('level') or default_level
    message = (issue.get('message') or fallback).strip()
    rel = _relpath(file) if file is not None else ''
    if rel:
        message = '%s [%s]' % (message, rel)
    if level in ('warning', 'warn', 'recommended'):
        report.warn(message, file, code=code)
        return
    report.error(message, file, code=code)


def _value_matches(value, definition):
    if not definition:
        return True
    if 'anyOf' in definition:
        return any(_value_matches(value, option) for option in definition['anyOf'])
    expected = definition.get('type')
    if expected and not _json_type_matches(value, expected):
        return False
    enum_values = definition.get('enum')
    if enum_values is not None and value not in enum_values:
        return False
    return True


def _json_type_matches(value, expected):
    if expected == 'string':
        return isinstance(value, str)
    if expected == 'number':
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == 'integer':
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == 'boolean':
        return isinstance(value, bool)
    if expected == 'array':
        return isinstance(value, list)
    if expected == 'object':
        return isinstance(value, dict)
    return True


def _relpath(node):
    return node.get_relative_path().replace('\\', '/')


def _schema_path(node):
    rel = _relpath(node)
    if not rel or rel in ('.',):
        return '/'
    return rel if rel.startswith('/') else '/' + rel
