import lxml

from . import model
from . import schema


class Query:
    def __init__(self, dataset: model.Dataset, scm: schema.Schema):
        self.dataset = dataset
        self.scm = scm
        self.id2x = {}
        self.x2id = {}
        self.root = dataset.to_etree(id2x=self.id2x, x2id=self.x2id,
                                     nsmap_={**self.scm.ns_map, None: self.scm.ns})

    def execute(self, expr, search_node=None):
        raise NotImplemented()


class XPathQuery(Query):
    def __init__(self, dataset: model.Dataset, scm: schema.Schema):
        super(XPathQuery, self).__init__(dataset, scm)

    def execute(self, expr, search_node=None):
        context = self.root
        if search_node:
            context = search_node
        result = context.xpath(expr, namespaces=self.scm.ns_map)
        result = list(map(lambda e: self.x2id[e] if e in self.x2id else e, result))
        return result


class CSSQuery(Query):
    def __init__(self, dataset: model.Dataset, scm: schema.Schema):
        super(CSSQuery, self).__init__(dataset, scm)

    def execute(self, expr, search_node=None):
        raise NotImplemented()


class ObjectPathQuery(Query):
    def __init__(self, dataset: model.Dataset, scm: schema.Schema):
        super(ObjectPathQuery, self).__init__(dataset, scm)

    def execute(self, expr, search_node=None):
        raise NotImplemented()
