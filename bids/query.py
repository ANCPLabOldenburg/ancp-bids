import bids.model as model
import bids.schema as schema


class Query:
    def __init__(self, expr: str):
        self.expr = expr

    def get_expression(self):
        return self.expr


class QueryResult:
    def __init__(self, result):
        self.result = result


class QueryExecutor:
    def __init__(self, dataset: model.Dataset, scm: schema.Schema):
        self.dataset = dataset
        self.scm = scm
        root = dataset.to_etree(nsmap_=schema.NS_MAP)
        self.root = root

    def execute(self, query: Query) -> QueryResult:
        expr = query.get_expression()
        result = self.root.xpath(expr, namespaces=schema.NS_MAP)
        return QueryResult(result)
