from functools import reduce

from .query import XPathQuery
from .schema import Schema, NS_PREFIX


class BIDSLayout:
    def __init__(self, ds_dir: str):
        self.sc = Schema()
        self.dataset = self.sc.load_dataset(ds_dir)
        self.query = XPathQuery(self.dataset, self.sc)

    def _query(self, expr: str):
        qry_result = self.query.execute(expr)
        return qry_result

    def get_subjects(self):
        return self._query('//bids:subjects/@name')

    def get_sessions(self):
        return self._query('//bids:sessions/@name')

    def get_tasks(self):
        tasks = self._query('//bids:entities[@key = "task"]/@value')
        tasks = list(set(tasks))
        return tasks

    def _gen_scalar_expr(self, k, v):
        if v is None:
            return 'not(@%s)' % k
        return '@%s="%s"' % (k, v)

    def _scalar_or_list(self, attr_name, v):
        if isinstance(v, list):
            values = list(map(lambda val: self._gen_scalar_expr(attr_name, val), v))
            return '(' + ' or '.join(values) + ')'
        else:
            return self._gen_scalar_expr(attr_name, v)

    def get(self, return_type='object', target=None, scope=None, extension=None, suffix=None,
            regex_search=False, absolute_paths=None, invalid_filters='error',
            **entities):
        expr = []
        if scope:
            expr.append('//%s:%s' % (NS_PREFIX, scope))
        entity_filters = []
        for k, v in entities.items():
            v = self.sc.process_entity_value(k, v)
            v = self._scalar_or_list('value', v)
            entity_filters.append('%s:entities[@key="%s" and %s]' % (NS_PREFIX, k, v))
        if extension:
            v = self._scalar_or_list('extension', extension)
            entity_filters.append(v)
        if suffix:
            v = self._scalar_or_list('suffix', suffix)
            entity_filters.append(v)
        if entity_filters:
            entity_filters_str = ' and '.join(entity_filters)
            expr.append('//*[%s]' % entity_filters_str)
        expr_final = ''.join(expr)
        artifacts = self._query(expr_final)
        artifacts = list(map(lambda e: self.query.mapping[e], artifacts))
        if return_type and return_type.startswith("file"):
            artifacts = list(map(lambda e: e.get_absolute_path(), artifacts))
        return artifacts
