from . import load_dataset
from .query import XPathQuery
from .schema import NS_PREFIX


class BIDSLayout:
    def __init__(self, ds_dir: str):
        self.dataset = load_dataset(ds_dir)
        self.sc = self.dataset._schema
        self.query = XPathQuery(self.dataset, self.sc)

    def _query(self, expr: str, search_node=None):
        qry_result = self.query.execute(expr, search_node)
        return qry_result

    def _query_entities(self, entity_key):
        entities = self._query('//bids:entities[@key = "%s"]/@value' % entity_key)
        entities = sorted(list(set(entities)))
        return entities

    def get_subjects(self):
        return self._query_entities('sub')

    def get_sessions(self):
        return self._query_entities('ses')

    def get_tasks(self):
        return self._query_entities('task')

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

    def get(self, return_type='object', target=None, scope: str = None, extension=None, suffix=None,
            regex_search=False, absolute_paths=None, invalid_filters='error',
            **entities):
        expr = []
        if scope:
            # TODO split into paths and set the last path as search context
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
        if return_type and return_type.startswith("file"):
            artifacts = list(map(lambda e: e.get_absolute_path(), artifacts))
        return artifacts
