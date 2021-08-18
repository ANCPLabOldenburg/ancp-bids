import lxml

from . import model
from . import schema


class Query:
    def __init__(self, dataset: model.Dataset, scm: schema.Schema):
        self.dataset = dataset
        self.scm = scm
        self.mapping = {}
        self.root = dataset.to_etree(mapping_=self.mapping, nsmap_=schema.NS_MAP)

    def execute(self, expr):
        raise NotImplemented()


class XPathQuery(Query):
    def __init__(self, dataset: model.Dataset, scm: schema.Schema):
        super(XPathQuery, self).__init__(dataset, scm)

    def execute(self, expr):
        result = self.root.xpath(expr, namespaces=schema.NS_MAP)
        return result

class CSSQuery(Query):
    def __init__(self, dataset: model.Dataset, scm: schema.Schema):
        super(CSSQuery, self).__init__(dataset, scm)

    def execute(self, expr):
        raise NotImplemented()

class ObjectPathQuery(Query):
    def __init__(self, dataset: model.Dataset, scm: schema.Schema):
        super(ObjectPathQuery, self).__init__(dataset, scm)

    def execute(self, expr):
        raise NotImplemented()