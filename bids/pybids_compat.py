import bids.schema as bs
import bids.query as qr


class BIDSLayout:
    def __init__(self, ds_dir: str):
        sc = bs.Schema()
        self.dataset = sc.load_dataset(ds_dir)
        self.query_exec = qr.QueryExecutor(self.dataset, sc)

    def _query(self, expr: str):
        qry = qr.Query(expr)
        qry_result = self.query_exec.execute(qry)
        return qry_result.result

    def get_subjects(self):
        return self._query('//bids:subjects/@name')

    def get_sessions(self):
        return self._query('//bids:sessions/@name')

    def get_tasks(self):
        tasks = self._query('//bids:entities[@key = "task"]/@value')
        tasks = list(set(tasks))
        return tasks

    def get(self, return_type='object', target=None, scope='all', extension='.*', suffix='.*',
            regex_search=False, absolute_paths=None, invalid_filters='error',
            **entities):
        expr = []
        if scope != 'all':
            expr.append('//bids:%s' % scope)
        entity_filters = []
        for k, v in entities.items():
            if isinstance(v, list):
                values = list(map(lambda val: '@value="%s"' % val, v))
                v = '(' + ' or '.join(values) + ')'
            else:
                v = '@value="%s"' % v
            entity_filters.append('bids:entities[@key="%s" and %s]' % (k, v))
        if extension:
            entity_filters.append('@extension="%s"' % extension)
        if suffix:
            entity_filters.append('@suffix="%s"' % suffix)
        if entity_filters:
            entity_filters_str = ' and '.join(entity_filters)
            expr.append('//*[%s]' % entity_filters_str)
        expr_final = ''.join(expr)
        artifacts = self._query(expr_final)
        artifacts = list(map(lambda e: self.query_exec.mapping[e], artifacts))
        if return_type and return_type.startswith("file"):
            artifacts = list(map(lambda e: e.get_absolute_path(), artifacts))
        return artifacts
