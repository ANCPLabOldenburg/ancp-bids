import re
from typing import List

from . import model
from . import schema


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
        return all([op.eval(context) for op in self.bool_ops])


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


class EntityExpr(CompExpr):
    def __init__(self, key: model.EntityEnum, value, op=EqExpr):
        self.op = AllExpr(EqExpr(model.EntityRef.key, key.entity_), op(model.EntityRef.value, value))

    def eval(self, context) -> bool:
        if not isinstance(context, model.Artifact):
            raise ValueError('Entity expression can only operate on model.Artifact')
        return any([self.op.eval(e) for e in context.entities])


class DatatypeExpr(CompExpr):
    def __init__(self, key: model.DatatypeEnum, value, op=EqExpr):
        self.op = AllExpr(EqExpr(model.EntityRef.key, key.entity_), op(model.EntityRef.value, value))

    def eval(self, context) -> bool:
        if not isinstance(context, model.Artifact):
            raise ValueError('Datatype expression can only operate on model.Artifact')
        return any([self.op.eval(e) for e in context.entities])


class Select:
    def __init__(self, context: model.Model, filter_type):
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
        return self._exec(model.File.get_relative_path)

    def objects(self):
        return self._exec(lambda m: m)


class Query:
    def __init__(self, dataset: model.Dataset, scm: schema.Schema):
        self.dataset = dataset
        self.scm = scm
        self.id2x = {}
        self.x2id = {}
        self.root = dataset.to_etree(id2x=self.id2x, x2id=self.x2id, nsmap_={})

    def execute(self, expr, search_node=None, return_model_objects=True):
        raise NotImplemented()


class XPathQuery(Query):
    def __init__(self, dataset: model.Dataset, scm: schema.Schema):
        super(XPathQuery, self).__init__(dataset, scm)

    def execute(self, expr, search_node=None, return_lxml_objects=False):
        context = self.root
        if search_node:
            context = search_node
        result = context.xpath(expr)
        if return_lxml_objects:
            return result
        result = list(map(lambda e: self.x2id[e] if e in self.x2id else e, result))
        return result
