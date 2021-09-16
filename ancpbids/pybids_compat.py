from functools import partial

from . import load_dataset
from .query import XPathQuery


class BIDSLayout:
    def __init__(self, ds_dir: str):
        self.dataset = load_dataset(ds_dir)
        self.sc = self.dataset._schema
        self.ns_prefix = self.sc.ns_prefix
        self.query = XPathQuery(self.dataset, self.sc)

    def _query(self, expr: str, search_node=None):
        qry_result = self.query.execute(expr, search_node)
        return qry_result

    def __getattr__(self, key):
        k = key if not key.startswith("get_") else key[4:]
        k = self.sc.fuzzy_match_entity_key(k)
        return partial(self.get, return_type='id', target=k)

    def _gen_scalar_expr(self, k, v):
        if v is None:
            return 'not(@%s)' % k
        if v == '*':
            return '@%s' % k
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
            expr.append('//%s:%s' % (self.ns_prefix, scope))
        entity_filters = []
        if target:
            target = self.sc.fuzzy_match_entity_key(target)
            entities = {**entities, target: '*'}
        for k, v in entities.items():
            k = self.sc.fuzzy_match_entity_key(k)
            v = self.sc.process_entity_value(k, v)
            v = self._scalar_or_list('value', v)
            entity_filters.append('%s:entities[@key="%s" and %s]' % (self.ns_prefix, k, v))
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
            return list(map(lambda e: e.get_absolute_path(), artifacts))
        elif return_type == 'id' and target is not None:
            keys = sorted(set(
                [entity.value for a in artifacts for entity in filter(lambda e: e.key == target, a.get_entities())]))
            return keys
        return artifacts
