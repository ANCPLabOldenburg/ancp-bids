"""Validation session, rule indexing, and selector evaluation."""
import re
from collections import defaultdict

from .expr import evaluate, evaluate_ast, parse
from .values import relpath, schema_path


_SUFFIX_EQ = re.compile(r"""(?:^|[\s(&|])suffix\s*==\s*['\"]([^'\"]+)['\"]""")
_DATATYPE_EQ = re.compile(r"""(?:^|[\s(&|])datatype\s*==\s*['\"]([^'\"]+)['\"]""")


def get_session(report, dataset):
    sess = getattr(report, '_schema_session', None)
    if sess is None or sess.dataset is not dataset:
        sess = ValidationSession(dataset)
        report._schema_session = sess
    sess.report = report
    flush_pending(sess, report)
    return sess


def flush_pending(session, report):
    pending = getattr(session, '_pending_issues', None)
    if not pending:
        return
    for severity, message, offender, code, sub_code in pending:
        if severity == 'warn':
            report.warn(message, offender, code=code, sub_code=sub_code)
        else:
            report.error(message, offender, code=code, sub_code=sub_code)
    pending.clear()


def queue_issue(session, severity, message, offender, code, sub_code=None):
    report = getattr(session, 'report', None)
    if report is not None:
        if severity == 'warn':
            report.warn(message, offender, code=code, sub_code=sub_code)
        else:
            report.error(message, offender, code=code, sub_code=sub_code)
        return
    session._pending_issues.append((severity, message, offender, code, sub_code))


class FileIndex:
    def __init__(self, dataset):
        self.paths = set()
        self.root_names = set()
        self.basenames = set()
        self.stimuli = set()
        schema = dataset.get_schema()
        for file in dataset.select(schema.File).objects():
            rel = relpath(file)
            path = schema_path(file)
            self.paths.add(rel)
            self.paths.add(path)
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


class BoundRule:
    __slots__ = ('rule', 'selector_asts')

    def __init__(self, rule):
        self.rule = rule
        selectors = rule.get('selectors') or ()
        compiled = []
        for expr in selectors:
            try:
                compiled.append(parse(expr))
            except Exception:
                compiled.append(expr)
        self.selector_asts = tuple(compiled)


class IndexedRules:
    """Bucket rules by simple suffix/datatype selector constraints."""

    def __init__(self, rules):
        self.wildcard = []
        self.by_suffix = defaultdict(list)
        self.by_datatype = defaultdict(list)
        for rule in rules:
            bound = BoundRule(rule)
            suffixes, datatypes = selector_constraints(rule.get('selectors') or ())
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


def selector_constraints(selectors):
    suffixes = set()
    datatypes = set()
    for expr in selectors:
        suffixes.update(_SUFFIX_EQ.findall(expr))
        datatypes.update(_DATATYPE_EQ.findall(expr))
    return suffixes, datatypes


def rule_leaves(node):
    if not isinstance(node, dict):
        return
    if is_leaf_rule(node):
        yield node
        return
    for child in node.values():
        yield from rule_leaves(child)


def is_leaf_rule(node):
    return any(key in node for key in ('fields', 'columns', 'checks', 'selectors')) and (
        'fields' in node or 'columns' in node or 'checks' in node)


def is_file_rule(node):
    return any(key in node for key in ('suffixes', 'extensions', 'entities', 'path', 'stem'))


def is_core_file_rule(rule):
    if 'stem' in rule:
        return True
    path = rule.get('path')
    return bool(path) and '.' in path.rsplit('/', 1)[-1]


def selectors_match(selectors, context, compiled=None):
    if compiled is not None:
        if not compiled:
            return True
        for item in compiled:
            if isinstance(item, str):
                if not selector_ok(safe_eval(item, context)):
                    return False
            elif not selector_ok(safe_eval_ast(item, context)):
                return False
        return True
    if not selectors:
        return True
    for expr in selectors:
        if not selector_ok(safe_eval(expr, context)):
            return False
    return True


def selector_ok(value):
    # Schema selectors follow JS truthiness for intersects() results (lists),
    # while failed intersects() returns False.
    return value is not False and value is not None


def safe_eval(expression, context):
    try:
        return evaluate(expression, context)
    except Exception:
        return None


def safe_eval_ast(ast, context):
    try:
        return evaluate_ast(ast, context)
    except Exception:
        return None


class ValidationSession:
    def __init__(self, dataset):
        from .context import json_contents, load_columns, modalities_for

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
        self.files_index = FileIndex(dataset)
        self.dataset_description = json_contents(dataset.dataset_description)
        self.suffix_rules = defaultdict(list)
        self.path_rules = []
        self.stem_rules = []
        self.required_core = []
        self.recommended_core = []
        self._load_file_rules(self.document['rules']['files'])
        self.sidecar_rules = IndexedRules(rule_leaves(self.document['rules'].get('sidecars')))
        self.json_rules = IndexedRules(rule_leaves(self.document['rules'].get('json')))
        self.tabular_rules = IndexedRules(rule_leaves(self.document['rules'].get('tabular_data')))
        self.dataset_metadata_rules = IndexedRules(
            rule_leaves(self.document['rules'].get('dataset_metadata')))
        self.check_rules = IndexedRules(rule_leaves(self.document['rules'].get('checks')))
        self._contexts = {}
        self._subject_ctx = {}
        self._files = None
        self._pending_issues = []
        self.report = None
        self._load_columns = load_columns
        self._modalities_for = modalities_for
        self.dataset_ctx = self._build_dataset_context()

    def _load_file_rules(self, node, section=None):
        if not isinstance(node, dict):
            return
        if is_file_rule(node):
            self._register_file_rule(node)
            return
        for key, child in node.items():
            if section is None and key == 'deriv':
                dtype = self.dataset_description.get('DatasetType') or 'raw'
                if dtype not in ('derivative', 'derivatives'):
                    continue
            self._load_file_rules(child, section or key)

    def _register_file_rule(self, rule):
        if is_core_file_rule(rule):
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
        from .context import ancestor_subject, load_columns

        subject = ancestor_subject(file)
        if subject is None:
            return None
        cached = self._subject_ctx.get(id(subject))
        if cached is not None:
            return cached
        ses_dirs = [session.name for session in (subject.sessions or [])]
        session_id = None
        for candidate in subject.files or []:
            if getattr(candidate, 'suffix', None) == 'sessions' and candidate.name.endswith('.tsv'):
                columns = load_columns(candidate, self)
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
        columns = self._load_columns(participants, self) if participants else None
        if columns and 'participant_id' in columns:
            participant_id = columns['participant_id']
        present = sorted({
            folder.name for folder in self.dataset.select(self.schema.DatatypeFolder).objects()
            if folder.name in self.datatypes
        })
        return {
            'dataset_description': self.dataset_description,
            'datatypes': present,
            'modalities': self._modalities_for(present, self.document),
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
        from .context import build_context

        return build_context(self, file, rich)
