"""Execute ``schema.document`` rules against a dataset graph."""
import os
import re
from collections import defaultdict

from ancpbids.model_base import Artifact, DatatypeFolder, DerivativeFolder, Folder, Subject

from .expr import evaluate, evaluate_ast, parse
from .headers import parse_gzip, parse_nifti_header, parse_tiff


_SUFFIX_EQ = re.compile(r"""(?:^|[\s(&|])suffix\s*==\s*['\"]([^'\"]+)['\"]""")
_DATATYPE_EQ = re.compile(r"""(?:^|[\s(&|])datatype\s*==\s*['\"]([^'\"]+)['\"]""")


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


class _BoundRule:
    __slots__ = ('rule', 'selector_asts')

    def __init__(self, rule):
        self.rule = rule
        selectors = rule.get('selectors') or ()
        compiled = []
        for expr in selectors:
            try:
                compiled.append(parse(expr))
            except Exception:
                # Keep the raw string; _safe_eval will handle/ignore failures.
                compiled.append(expr)
        self.selector_asts = tuple(compiled)


class _IndexedRules:
    """Bucket rules by simple suffix/datatype selector constraints."""

    def __init__(self, rules):
        self.wildcard = []
        self.by_suffix = defaultdict(list)
        self.by_datatype = defaultdict(list)
        for rule in rules:
            bound = _BoundRule(rule)
            suffixes, datatypes = _selector_constraints(rule.get('selectors') or ())
            if not suffixes and not datatypes:
                self.wildcard.append(bound)
                continue
            for suffix in suffixes:
                self.by_suffix[suffix].append(bound)
            for datatype in datatypes:
                self.by_datatype[datatype].append(bound)

    def for_file(self, suffix, datatype):
        seen = set()
        result = []
        for bound in self.wildcard:
            seen.add(id(bound))
            result.append(bound)
        if suffix:
            for bound in self.by_suffix.get(suffix, ()):
                bid = id(bound)
                if bid in seen:
                    continue
                seen.add(bid)
                result.append(bound)
        if datatype:
            for bound in self.by_datatype.get(datatype, ()):
                bid = id(bound)
                if bid in seen:
                    continue
                seen.add(bid)
                result.append(bound)
        return result


def _selector_constraints(selectors):
    suffixes = set()
    datatypes = set()
    for expr in selectors:
        suffixes.update(_SUFFIX_EQ.findall(expr))
        datatypes.update(_DATATYPE_EQ.findall(expr))
    return suffixes, datatypes


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
        self.format_patterns = {
            name: spec.get('pattern')
            for name, spec in (objects.get('formats') or {}).items()
            if isinstance(spec, dict) and spec.get('pattern')
        }
        self.entity_defs = objects.get('entities') or {}
        self.files_index = _FileIndex(dataset)
        self.dataset_description = _json_contents(dataset.dataset_description)
        self.suffix_rules = defaultdict(list)
        self.path_rules = []
        self.stem_rules = []
        self.required_core = []
        self.recommended_core = []
        self._load_file_rules(self.document['rules']['files'])
        self.sidecar_rules = _IndexedRules(_rule_leaves(self.document['rules'].get('sidecars')))
        self.json_rules = _IndexedRules(_rule_leaves(self.document['rules'].get('json')))
        self.tabular_rules = _IndexedRules(_rule_leaves(self.document['rules'].get('tabular_data')))
        self.dataset_metadata_rules = _IndexedRules(
            _rule_leaves(self.document['rules'].get('dataset_metadata')))
        self.check_rules = _IndexedRules(_rule_leaves(self.document['rules'].get('checks')))
        self._contexts = {}
        self._subject_ctx = {}
        self._files = None
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
        if _is_core_file_rule(rule):
            level = rule.get('level')
            if level == 'required':
                self.required_core.append(rule)
            elif level == 'recommended':
                self.recommended_core.append(rule)
        if 'path' in rule:
            self.path_rules.append(rule)
            return
        if 'stem' in rule:
            self.stem_rules.append(rule)
            return
        for suffix in rule.get('suffixes') or ():
            self.suffix_rules[suffix].append(rule)

    def subject_context(self, file):
        subject = _ancestor_subject(file)
        if subject is None:
            return None
        cached = self._subject_ctx.get(id(subject))
        if cached is not None:
            return cached
        ses_dirs = [session.name for session in (subject.sessions or [])]
        session_id = None
        for candidate in subject.files or []:
            if getattr(candidate, 'suffix', None) == 'sessions' and candidate.name.endswith('.tsv'):
                columns = _load_columns(candidate)
                if columns and 'session_id' in columns:
                    session_id = columns['session_id']
                break
        cached = {'sessions': {'ses_dirs': ses_dirs, 'session_id': session_id}}
        self._subject_ctx[id(subject)] = cached
        return cached

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
        if self._files is None:
            self._files = [
                file for file in self.dataset.select(self.schema.File).objects()
                if not file.name.startswith('.')
            ]
        return self._files

    def context(self, file, rich=False):
        file_id = id(file)
        if rich:
            cached = self._contexts.get((file_id, True))
            if cached is not None:
                return cached
            ctx = dict(_basic_context(file, self))
            ctx['subject'] = self.subject_context(file)
            ctx['sidecar'] = _sidecar(file)
            ctx['json'] = _load_json(file)
            ctx['columns'] = _load_columns(file)
            ctx['associations'] = _associations(file, self, ctx)
            ctx['size'] = _file_size(file)
            _load_binary_headers(file, ctx)
            self._contexts[(file_id, True)] = ctx
            # Rich context is a superset; reuse for plain consumers.
            self._contexts[(file_id, False)] = ctx
            return ctx

        cached = self._contexts.get((file_id, False))
        if cached is not None:
            return cached
        # Prefer already-built rich context when available.
        cached = self._contexts.get((file_id, True))
        if cached is not None:
            return cached
        ctx = _basic_context(file, self)
        self._contexts[(file_id, False)] = ctx
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
        'subject': None,
        'sidecar': {},
        'json': None,
        'columns': None,
        'associations': {},
        'nifti_header': None,
        'gzip': None,
        'ome': None,
        'tiff': None,
        'dataset': dataset_ctx,
        'schema': session.document,
        'size': None,
        '_files': session.files_index,
    }


def _ancestor_subject(file):
    current = file
    while current is not None:
        if isinstance(current, Subject):
            return current
        current = getattr(current, 'parent_object_', None)
    return None


def _load_binary_headers(file, ctx):
    path = file.get_absolute_path()
    extension = file.extension or ''
    if extension.endswith('.gz'):
        ctx['gzip'] = parse_gzip(path)
    if extension.startswith('.nii'):
        ctx['nifti_header'] = parse_nifti_header(path)
    if extension.endswith('.tif') or extension.endswith('.btf') or '.ome.tif' in file.name:
        ome = extension.startswith('.ome') or '.ome.' in file.name
        tiff, ome_meta = parse_tiff(path, ome=ome)
        ctx['tiff'] = tiff
        ctx['ome'] = ome_meta


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
    required_entities = target.get('entities') or []
    current = file.get_parent()
    while current is not None:
        match = _associated_in_folder(
            file, current, suffix, extensions, required_entities)
        if match is not None:
            return match
        if not inherit:
            return None
        current = current.get_parent()
    return None


def _associated_in_folder(file, folder, suffix, extensions, required_entities=None):
    file_ents = file.get_entities() if isinstance(file, Artifact) else {}
    required_entities = required_entities or []
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
            if required_entities:
                long_to_short = {}
                schema = file.get_schema()
                if schema is not None:
                    long_to_short = {
                        e.name: e.value['name'] for e in schema.EntityEnum
                    }
                missing = False
                for entity in required_entities:
                    short = long_to_short.get(entity, entity)
                    if short not in cand_ents:
                        missing = True
                        break
                if missing:
                    continue
        return candidate
    return None


def _association_context(file):
    if file is None:
        return None
    path = _schema_path(file)
    name = file.name
    if name.endswith('.bval') or name.endswith('.bvec'):
        return _bval_bvec_context(file, path)
    ctx = {'path': path, 'n_rows': None}
    columns = _load_columns(file)
    if columns:
        ctx['n_rows'] = len(next(iter(columns.values())))
        ctx.update(columns)
    if isinstance(file, Artifact) and file.extension == '.json':
        return {'path': path}
    if getattr(file, 'suffix', None) == 'events':
        try:
            ctx['sidecar'] = file.get_metadata() if isinstance(file, Artifact) else {}
        except Exception:
            ctx['sidecar'] = {}
    return ctx


def _bval_bvec_context(file, path):
    try:
        text = open(file.get_absolute_path(), 'r', encoding='utf-8').read()
    except OSError:
        return {'path': path, 'n_cols': 0, 'n_rows': 0, 'values': []}
    rows = [line.split() for line in text.strip().splitlines() if line.strip()]
    if not rows:
        return {'path': path, 'n_cols': 0, 'n_rows': 0, 'values': []}
    values = []
    for item in rows[0]:
        try:
            values.append(float(item))
        except ValueError:
            values.append(item)
    return {
        'path': path,
        'n_cols': len(rows[0]),
        'n_rows': len(rows),
        'values': values,
    }


def _selectors_match(selectors, context, compiled=None):
    if compiled is not None:
        if not compiled:
            return True
        for item in compiled:
            if isinstance(item, str):
                if _safe_eval(item, context) is not True:
                    return False
            elif _safe_eval_ast(item, context) is not True:
                return False
        return True
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


def _safe_eval_ast(ast, context):
    try:
        return evaluate_ast(ast, context)
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
        report.error(
            "Missing required file '%s'" % missing,
            session.dataset,
            code='MISSING_REQUIRED_FILE')
    for rule in session.recommended_core:
        if any(_core_rule_covers(rule, file) for file in files):
            continue
        missing = rule.get('path') or rule.get('stem')
        report.warn(
            "Missing recommended file '%s'" % missing,
            session.dataset,
            code='MISSING_RECOMMENDED_FILE')


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
                    "Invalid entity '%s' in artifact '%s'" % (key, rel),
                    artifact,
                    code='ENTITY_NOT_IN_RULE',
                    sub_code=key)
            continue
        for key, value in artifact.entities.items():
            _check_entity_label(session, report, artifact, key, value)
        if not _entity_order_error(keys, session.ordered_short):
            continue
        expected = tuple(sorted(keys, key=session.ordered_short.index))
        report.error(
            "Invalid entities order: expected=%s, found=%s, artifact=%s" % (
                expected, tuple(keys), _relpath(artifact)),
            artifact,
            code='FILENAME_MISMATCH')


def _check_entity_label(session, report, artifact, short_key, value):
    long_name = session.entity_long.get(short_key)
    definition = session.entity_defs.get(long_name) or {}
    format_name = definition.get('format')
    pattern = session.format_patterns.get(format_name)
    if not pattern:
        return
    if re.fullmatch(pattern, str(value)):
        return
    report.error(
        "Invalid entity label '%s-%s' in '%s'" % (short_key, value, _relpath(artifact)),
        artifact,
        code='INVALID_ENTITY_LABEL',
        sub_code=short_key)


def _entity_order_error(keys, ordered_short):
    if len(keys) < 2:
        return False
    ranks = [ordered_short.index(key) for key in keys]
    return ranks != sorted(ranks)


# --- rules.directories --------------------------------------------------------

def _validate_directories(session, report):
    # Older schema versions (e.g. 1.8/1.9) omit rules.directories entirely.
    trees = session.document.get('rules', {}).get('directories') or {}
    if not trees:
        return
    dtype = session.dataset_description.get('DatasetType') or 'raw'
    if dtype in ('derivative', 'derivatives'):
        deriv_tree = trees.get('derivative')
        if deriv_tree:
            _check_tree(session.dataset, deriv_tree, report, session)
        return
    raw_tree = trees.get('raw')
    if raw_tree:
        _check_tree(session.dataset, raw_tree, report, session)
    deriv_root = session.dataset.derivatives
    if not deriv_root:
        return
    deriv_tree = trees.get('derivative')
    if not deriv_tree:
        return
    for child in deriv_root.folders or []:
        _check_tree(child, deriv_tree, report, session)


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
            report.error(
                "Unsupported datatype folder '%s'" % _relpath(child),
                child,
                code='DATATYPE_MISMATCH')
            continue
        report.error(
            "Unsupported folder '%s'" % _relpath(child),
            child,
            code='INVALID_LOCATION')


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
            if not _selectors_match(None, ctx, compiled=bound.selector_asts):
                continue
            _apply_fields(bound.rule.get('fields') or {}, data, objects, report, file, key_type)


def _apply_fields(fields, data, objects, report, file, key_type='JSON_KEY'):
    for name, spec in fields.items():
        level, issue = _field_spec(spec)
        present = isinstance(data, dict) and name in data and data[name] is not None
        if not present:
            _missing_field(level, issue, name, report, file, key_type=key_type)
            continue
        if level == 'deprecated':
            report.warn(
                "Deprecated metadata '%s' in '%s'" % (name, _relpath(file)),
                file,
                code='SIDECAR_KEY_DEPRECATED' if key_type == 'SIDECAR_KEY' else 'JSON_KEY_DEPRECATED',
                sub_code=name)
        definition = objects.get(name) or {}
        session = getattr(report, '_schema_session', None)
        patterns = session.format_patterns if session is not None else {}
        if _value_matches(data[name], definition, patterns):
            continue
        report.error(
            "Invalid type for '%s' in '%s'" % (name, _relpath(file)),
            file,
            code='JSON_SCHEMA_VALIDATION_ERROR',
            sub_code=name)


def _missing_field(level, issue, name, report, file, key_type='JSON_KEY'):
    if level not in ('required', 'recommended'):
        return
    fallback = "Missing %s metadata '%s'" % (level, name)
    _emit_issue(
        report,
        issue,
        file,
        fallback,
        default_level=level,
        default_code=_field_level_code(key_type, level),
        sub_code=name)


# --- rules.tabular_data -------------------------------------------------------

def _validate_tabular(session, report):
    for file in session.iter_files():
        if not file.name.endswith('.tsv'):
            continue
        ctx = session.context(file, rich=True)
        columns = ctx.get('columns')
        if columns is None:
            continue
        for bound in session.tabular_rules.for_file(ctx.get('suffix'), ctx.get('datatype')):
            if not _selectors_match(None, ctx, compiled=bound.selector_asts):
                continue
            _apply_tabular_rule(bound.rule, columns, session, report, file)


def _apply_tabular_rule(rule, columns, session, report, file):
    headers = list(columns)
    allowed = set()
    for key, spec in (rule.get('columns') or {}).items():
        header = (session.column_objects.get(key) or {}).get('name', key)
        allowed.add(header)
        level, issue = _field_spec(spec)
        if header in columns:
            continue
        _missing_field(level, issue, header, report, file, key_type='TSV_COLUMN')
    extras = [header for header in headers if header not in allowed]
    additional = rule.get('additional_columns')
    if additional == 'not_allowed' and extras:
        report.error(
            "Additional columns not allowed in '%s': %s" % (_relpath(file), extras),
            file,
            code='TSV_ADDITIONAL_COLUMNS_NOT_ALLOWED')
    elif additional == 'allowed_if_defined' and extras:
        sidecar = _sidecar(file) if isinstance(file, Artifact) else {}
        undefined = [header for header in extras if header not in sidecar]
        if undefined:
            report.error(
                "Additional columns require sidecar definitions in '%s': %s" % (
                    _relpath(file), undefined),
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
            if _value_matches(cell, definition, session.format_patterns):
                continue
            report.error(
                "Invalid value in column '%s' of '%s'" % (header, _relpath(file)),
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
                _relpath(file), initial_headers, headers[:len(initial_headers)]),
            file,
            code='TSV_COLUMN_ORDER_INCORRECT')
    for key in rule.get('index_columns') or []:
        header = (session.column_objects.get(key) or {}).get('name', key)
        values = columns.get(header) or []
        if len(values) != len(set(values)):
            report.error(
                "Duplicate index column '%s' in '%s'" % (header, _relpath(file)),
                file,
                code='TSV_INDEX_VALUE_NOT_UNIQUE',
                sub_code=header)


# --- rules.checks -------------------------------------------------------------

def _validate_checks(session, report):
    for file in session.iter_files():
        ctx = session.context(file, rich=True)
        for bound in session.check_rules.for_file(ctx.get('suffix'), ctx.get('datatype')):
            if not _selectors_match(None, ctx, compiled=bound.selector_asts):
                continue
            rule = bound.rule
            if _checks_pass(rule.get('checks') or [], ctx):
                continue
            _emit_issue(
                report,
                rule.get('issue') or {},
                file,
                'Schema check failed',
                default_code='CHECK_ERROR')


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


def _field_level_code(key_type, level):
    if key_type == 'TSV_COLUMN':
        return 'TSV_COLUMN_MISSING'
    if level == 'required':
        return '%s_REQUIRED' % key_type
    if level == 'recommended':
        return '%s_RECOMMENDED' % key_type
    return None


def _emit_issue(report, issue, file, fallback, default_level='error', default_code=None, sub_code=None):
    issue = issue or {}
    if not isinstance(issue, dict):
        issue = {}
    code = issue.get('code') or default_code
    level = issue.get('level') or default_level
    message = (issue.get('message') or fallback).strip()
    rel = _relpath(file) if file is not None else ''
    if rel:
        message = '%s [%s]' % (message, rel)
    if level in ('warning', 'warn', 'recommended'):
        report.warn(message, file, code=code, sub_code=sub_code)
        return
    report.error(message, file, code=code, sub_code=sub_code)


def _value_matches(value, definition, format_patterns=None):
    if not definition:
        return True
    if 'anyOf' in definition:
        return any(
            _value_matches(value, option, format_patterns)
            for option in definition['anyOf'])
    expected = definition.get('type')
    if expected and not _json_type_matches(value, expected):
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
            return all(_value_matches(item, item_def, format_patterns) for item in value)
    if expected == 'object' and isinstance(value, dict):
        props = definition.get('properties') or {}
        for key, prop_def in props.items():
            if key not in value:
                continue
            if not _value_matches(value[key], prop_def, format_patterns):
                return False
    pattern = definition.get('pattern')
    format_name = definition.get('format')
    if not pattern and format_name and format_patterns:
        pattern = format_patterns.get(format_name)
    if pattern and isinstance(value, str) and not re.fullmatch(pattern, value):
        return False
    return True


def _json_type_matches(value, expected):
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


def _relpath(node):
    return node.get_relative_path().replace('\\', '/')


def _schema_path(node):
    rel = _relpath(node)
    if not rel or rel in ('.',):
        return '/'
    return rel if rel.startswith('/') else '/' + rel
