import re
from fnmatch import fnmatch

from ancpbids.plugin import SchemaPlugin


class BoolExpr:
    pass


class CompExpr:
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
        return self.value == value


class ReExpr(CompExpr):
    def __init__(self, attr: property, regex_pattern: str):
        self.attr = attr
        self.regex_pattern = re.compile(regex_pattern)

    def eval(self, context) -> bool:
        value = self.attr.fget(context)
        value = str(value)
        return self.regex_pattern.match(value)


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
        return value is not None and fnmatch(value, self.pattern)


class EntityExpr(CompExpr):
    def __init__(self, schema, key, value, op=FnMatchExpr):
        self.schema = schema
        self.op = AllExpr(EqExpr(schema.EntityRef.key, key.entity_), op(schema.EntityRef.value, value))

    def eval(self, context) -> bool:
        if not isinstance(context, self.schema.Artifact):
            # for non-Artifacts, for example File, just return false
            return False
        return any([self.op.eval(e) for e in context.entities])


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

    def _exec(self, callback):
        for m in self.context.to_generator(filter_=lambda o: self._subtree.eval(o)):
            if isinstance(m, self.filter_type) and self._where.eval(m):
                yield callback(m)

    def get_file_paths(self):
        return self._exec(self.schema.File.get_relative_path)

    def get_file_paths_absolute(self):
        return self._exec(self.schema.File.get_absolute_path)

    def get_artifacts(self):
        # TODO filter by Artifact instances
        return self.objects()

    def objects(self, as_list=False):
        result = self._exec(lambda m: m)
        if as_list:
            result = list(result)
        return result


def select(context, target_type):
    return Select(context, target_type)


class QuerySchemaPlugin(SchemaPlugin):
    def execute(self, schema):
        schema.Model.select = select
