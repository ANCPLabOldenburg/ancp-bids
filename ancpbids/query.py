import re
import sys
from collections import OrderedDict
from fnmatch import fnmatch
from typing import Union, List

from ancpbids.utils import resolve_segments


class Expr:
    def convert_value(self, value):
        if hasattr(self, 'value_converter'):
            value = self.value_converter(value)
        return value


class BoolExpr(Expr):
    pass


class CompExpr(Expr):
    pass


class TrueExpr(BoolExpr):
    def __init__(self, *args):
        pass

    def eval(self, context) -> bool:
        return True


class AnyExpr(BoolExpr):
    def __init__(self, *bool_ops: CompExpr):
        self.bool_ops = bool_ops

    def eval(self, context) -> bool:
        return any([op.eval(context) for op in self.bool_ops])


class AllExpr(BoolExpr):
    def __init__(self, *bool_ops: CompExpr):
        self.bool_ops = bool_ops

    def eval(self, context) -> bool:
        for op in self.bool_ops:
            if not op.eval(context):
                # early exit to prevent evaluating remaining ops
                return False
        return True


class EqExpr(CompExpr):
    def __init__(self, attr: property, value):
        self.attr = attr
        self.value = value

    def eval(self, context) -> bool:
        value = self.attr.fget(context)
        value = self.convert_value(value)
        return self.value == value


class ReExpr(CompExpr):
    def __init__(self, attr: property, regex_pattern: str):
        self.attr = attr
        self.regex_pattern = re.compile(regex_pattern)

    def eval(self, context) -> bool:
        value = self.attr.fget(context)
        value = self.convert_value(value)
        value = str(value)
        return self.regex_pattern.search(value)


class CustomOpExpr(CompExpr):
    def __init__(self, op):
        self.op = op

    def eval(self, context) -> bool:
        return self.op(context)


class FnMatchExpr(CompExpr):
    def __init__(self, attr: property, pattern):
        self.attr = attr
        self.pattern = pattern

    def eval(self, context) -> bool:
        value = self.attr.fget(context)
        value = self.convert_value(value)
        value = str(value)
        return value is not None and fnmatch(value, self.pattern)


class EntityExpr(CompExpr):
    def __init__(self, schema, key, pattern, op=FnMatchExpr):
        self.schema = schema
        if pattern is not None:
            pattern = schema.process_entity_value(key, pattern)
            if isinstance(pattern, list):
                pattern = list(map(lambda v: str(v), pattern))
            else:
                pattern = str(pattern)
        self.key = key
        self.pattern = pattern
        self.op = op(schema.EntityRef.value, pattern)
        self.op.value_converter = lambda v: schema.process_entity_value(key, v)

    def eval(self, context) -> bool:
        if not isinstance(context, self.schema.Artifact):
            # for non-Artifacts, for example File, just return false
            return False
        ents = list(filter(lambda e: e.key == self.key.literal_, context.entities))
        if not ents:
            # the entity must not exist
            if self.pattern is None:
                return True
            return False
        if self.pattern is None:
            # the entity must not exist, but we found one
            return False
        target_key = ents[0]
        return self.op.eval(target_key)


class Select:
    def __init__(self, context, filter_type):
        self.schema = context.get_schema()
        self.context = context
        self.filter_type = filter_type
        self._where = TrueExpr()
        self._subtree = TrueExpr()

    def subtree(self, bool_expr: BoolExpr):
        self._subtree = bool_expr

    def where(self, bool_expr: BoolExpr):
        self._where = bool_expr
        return self

    def _exec(self, callback, depth=sys.maxsize):
        for m in self.context.to_generator(filter_=lambda o: self._subtree.eval(o), depth=depth):
            if isinstance(m, self.filter_type) and self._where.eval(m):
                yield callback(m)

    def get_file_paths(self):
        return self._exec(self.schema.File.get_relative_path)

    def get_file_paths_absolute(self):
        return self._exec(self.schema.File.get_absolute_path)

    def get_artifacts(self):
        # TODO filter by Artifact instances
        return self.objects()

    def objects(self, as_list=False, depth=sys.maxsize):
        result = self._exec(callback=lambda m: m, depth=depth)
        if as_list:
            result = list(result)
        return result


def _to_any_expr(value, ctor, converter=lambda v: v):
    # if the value is a list, then wrap it in an AnyExpr
    if isinstance(value, list):
        ops = []
        for v in value:
            ops.append(ctor(converter(v)))
        return AnyExpr(*ops)
    # else just return using the constructor function
    return ctor(converter(value))


def _require_artifact(schema, expr) -> AllExpr:
    """Wraps the provided expression in an expression that makes sure the context of evaluation is an Artifact.

    Parameters
    ----------
    expr :
        the expression to wrap

    Returns
    -------
        a wrapping expression to make sure that the provided object is an instance of Artifact
    """
    return AllExpr(CustomOpExpr(lambda m: isinstance(m, schema.Artifact)), expr)


def query(folder, return_type: str = 'object', target: str = None, scope: str = None,
          extension: Union[str, List[str]] = None, suffix: Union[str, List[str]] = None,
          regex_search=False,
          **entities) -> Union[List[str], List[object]]:
    """Depending on the return_type value returns either paths to files that matched the filtering criteria
    or :class:`Artifact <ancpbids.model_v1_7_0.Artifact>` objects for further processing by the caller.

    Note that all provided filter criteria are AND combined, i.e. subj='02',task='lang' will match files containing
    '02' as a subject AND 'lang' as a task. If you provide a list of values for a criteria, they will be OR combined.

    .. code-block::

        file_paths = layout.get(subj='02', task='lang', suffix='bold', return_type='files')

        file_paths = layout.get(subj=['02', '03'], task='lang', return_type='files')

    Parameters
    ----------
    folder:
            an entry-point of type Folder to search within
    return_type:
        Either 'files' to return paths of matched files
        or 'object' to return :class:`Artifact <ancpbids.model_v1_7_0.Artifact>` object, defaults to 'object'

    target:
        Either `suffixes`, `extensions` or one of any valid BIDS entities key
        (see :class:`EntityEnum <ancpbids.model_v1_7_0.EntityEnum>`, defaults to `None`
    scope:
        a hint where to search for files
        If passed, only nodes/directories that match the specified scope will be
        searched. Possible values include:
        'all' (default): search all available directories.
        'derivatives': search all derivatives directories.
        'raw': search only BIDS-Raw directories.
        'self': search only the directly called BIDSLayout.
        <PipelineName>: the name of a BIDS-Derivatives pipeline.
    extension:
        criterion to match any files containing the provided extension only
    suffix:
        criterion to match any files containing the provided suffix only
    entities
        a list of key-values to match the entities of interest, example: subj='02',task='lang'

    Returns
    -------
        depending on the return_type value either paths to files that matched the filtering criteria
        or Artifact objects for further processing by the caller
    """
    if scope is None:
        scope = 'all'
    if return_type == 'id':
        if not target:
            raise ValueError("return_type=id requires the target parameter to be set")

    schema = folder.get_schema()
    context = folder
    ops = []
    target_type = schema.File
    if scope not in ['all', 'raw', 'self']:
        context, _ = resolve_segments(folder, scope, False)

    if not context:
        return None

    select = context.select(target_type)

    if scope == 'raw':
        # the raw scope does not search in derivatives folder but everything else
        select.subtree(CustomOpExpr(lambda m: not isinstance(m, schema.DerivativeFolder)))

    result_extractor = None
    if target:
        if target in 'suffixes':
            suffix = '*'
            result_extractor = lambda artifacts: [a.suffix for a in artifacts]
        elif target in 'extensions':
            extension = '*'
            result_extractor = lambda artifacts: [a.extension for a in artifacts]
        else:
            target = schema.fuzzy_match_entity_key(target)
            entities = {**entities, target: '*'}
            result_extractor = lambda artifacts: [entity.value for a in artifacts for entity in
                                                  filter(lambda e: e.key == target, a.entities)]

    search_operator = FnMatchExpr
    if regex_search:
        search_operator = ReExpr

    for k, v in entities.items():
        entity_key = schema.fuzzy_match_entity(k)
        v = schema.process_entity_value(entity_key, v)
        ops.append(
            _require_artifact(schema,
                              _to_any_expr(v, lambda val: EntityExpr(schema, entity_key, val, op=search_operator))))

    if extension:
        converter = lambda v: "." + v if v != "*" and not v.startswith(".") else v
        any_expr = _to_any_expr(extension, lambda ext: search_operator(schema.Artifact.extension, ext), converter)
        require_expr = _require_artifact(schema, any_expr)
        ops.append(require_expr)

    if suffix:
        ops.append(
            _require_artifact(schema,
                              _to_any_expr(suffix, lambda suf: search_operator(schema.Artifact.suffix, suf))))

    select.where(AllExpr(*ops))

    if return_type:
        if return_type.startswith("file"):
            return list(select.get_file_paths_absolute())
        elif return_type == 'dir':
            result = filter(lambda o: isinstance(o, schema.File), select.objects())
            return set(map(lambda a: a.get_parent().get_relative_path(), result))

    artifacts = select.objects()
    if result_extractor:
        return sorted(set(result_extractor(artifacts)))
    return list(artifacts)


def query_entities(folder, scope: str = None, sort: bool = False, long_form=False) -> dict:
    """Returns a unique set of entities found within the dataset as a dict.
    Each key of the resulting dict contains a list of values (with at least one element).

    Example dict:
    .. code-block::

        {
            'sub': ['01', '02', '03'],
            'task': ['gamblestask']
        }

    Parameters
    ----------
    folder:
        an entry-point of type Folder to search within
    scope:
        see BIDSLayout.get()
    sort: default is `False`
        whether to sort the keys by name

    Returns
    -------
    dict
        a unique set of entities found within the dataset as a dict
    """
    schema = folder.get_schema()
    known_entities = {e.name: e.literal_ for e in list(schema.EntityEnum)}
    artifacts = filter(lambda m: isinstance(m, schema.Artifact), query(folder, scope=scope))
    result = {}
    for e in [e for a in artifacts for e in a.entities]:
        key = e.key
        if key not in result:
            result[key] = set()
        result[key].add(e.value)
    if long_form:
        result = {known_entities[k] if k in known_entities else k: v for k, v in result.items()}
    if sort:
        result = {k: sorted(v) for k, v in sorted(result.items())}
    return result
