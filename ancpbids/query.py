import lxml

from . import model
from . import schema


class Query:
    def __init__(self, dataset: model.Dataset, scm: schema.Schema):
        self.dataset = dataset
        self.scm = scm
        self.id2x = {}
        self.x2id = {}
        self.root = dataset.to_etree(mapping_=self.id2x, reverse_mapping_=self.x2id, nsmap_=schema.NS_MAP)

    def execute(self, expr, search_node: lxml.etree.Element = None):
        raise NotImplemented()


class XPathQuery(Query):
    def __init__(self, dataset: model.Dataset, scm: schema.Schema):
        super(XPathQuery, self).__init__(dataset, scm)

    def execute(self, expr, search_node: lxml.etree.Element = None):
        context = self.root
        if search_node:
            context = search_node
        result = context.xpath(expr, namespaces=schema.NS_MAP)
        result = list(map(lambda e: self.x2id[e] if e in self.x2id else e, result))
        return result


class CSSQuery(Query):
    def __init__(self, dataset: model.Dataset, scm: schema.Schema):
        super(CSSQuery, self).__init__(dataset, scm)

    def execute(self, expr, search_node: lxml.etree.Element = None):
        raise NotImplemented()


class ObjectPathQuery(Query):
    def __init__(self, dataset: model.Dataset, scm: schema.Schema):
        super(ObjectPathQuery, self).__init__(dataset, scm)

    def execute(self, expr, search_node: lxml.etree.Element = None):
        raise NotImplemented()
