from .schema import Schema
from .query import QueryExecutor, Query


class BIDSLayout:
    def __init__(self, ds_dir: str):
        sc = Schema()
        self.dataset = sc.load_dataset(ds_dir)
        self.query_exec = QueryExecutor(self.dataset, sc)

    def _query(self, expr: str):
        qry = Query(expr)
        qry_result = self.query_exec.execute(qry)
        return qry_result.result

    def get_subjects(self):
        return self._query('//ancpbids:subjects/@name')

    def get_sessions(self):
        return self._query('//ancpbids:sessions/@name')

    def get_tasks(self):
        tasks = self._query('//ancpbids:entities[@key = "task"]/@value')
        tasks = list(set(tasks))
        return tasks

    def _scalar_or_list(self, attr_name, v):
        if isinstance(v, list):
            values = list(map(lambda val: '@%s="%s"' % (attr_name, val), v))
            return '(' + ' or '.join(values) + ')'
        else:
            return '@%s="%s"' % (attr_name, v)

    def get(self, return_type='object', target=None, scope='all', extension=None, suffix=None,
            regex_search=False, absolute_paths=None, invalid_filters='error',
            **entities):
        expr = []
        if scope != 'all':
            expr.append('//ancpbids:%s' % scope)
        entity_filters = []
        for k, v in entities.items():
            v = self._scalar_or_list('value', v)
            entity_filters.append('ancpbids:entities[@key="%s" and %s]' % (k, v))
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
        artifacts = list(map(lambda e: self.query_exec.mapping[e], artifacts))
        if return_type and return_type.startswith("file"):
            artifacts = list(map(lambda e: e.get_absolute_path(), artifacts))
        return artifacts
