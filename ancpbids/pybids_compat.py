from collections import OrderedDict
from functools import partial

import lxml.etree

from . import load_dataset, model, LOGGER
from .query import XPathQuery, CustomOpExpr
from .utils import deepupdate


class BIDSLayout:
    def __init__(self, ds_dir: str, **kwargs):
        self.dataset = load_dataset(ds_dir)
        self.sc = self.dataset._schema
        self.query = XPathQuery(self.dataset, self.sc)

    def _query(self, expr: str, search_node=None, return_lxml_objects=False):
        return self.query.execute(expr, search_node, return_lxml_objects)

    def __getattr__(self, key, **kwargs):
        k = key if not key.startswith("get_") else key[4:]
        return partial(self.get, return_type='id', target=k, **kwargs)

    def _gen_scalar_expr(self, k, v):
        if v is None:
            return 'not(%s)' % k
        if v == '*':
            return '%s' % k
        return '%s="%s"' % (k, v)

    def _scalar_or_list(self, attr_name, v):
        if isinstance(v, list):
            values = list(map(lambda val: self._gen_scalar_expr(attr_name, val), v))
            return '(' + ' or '.join(values) + ')'
        else:
            return self._gen_scalar_expr(attr_name, v)

    def get_metadata(self, *args, **kwargs):
        qry_result = self.get(return_type='lxml', element_source='metadatafiles', *args, **kwargs)
        # build lists of ancestors + the leaf (metadata file)
        ancestors = list(map(lambda e: (list(reversed(list(e.iterancestors()))), e), qry_result))
        # sort by number of ancestors
        # TODO must sort by the items within the list not just by length of list
        # example: [xyz,abc] would be treated the same when it should be [abc, xyz]
        ancestors.sort(key=lambda e: len(e[0]))

        metadata = {}
        if ancestors:
            # start with first metadata file
            deepupdate(metadata, self.query.x2id[ancestors[0][1]].contents)
            if len(ancestors) > 1:
                for i in range(1, len(ancestors)):
                    a0 = ancestors[i - 1][0]
                    a1 = ancestors[i][0]
                    # remove the ancestors from a0 and make sure it is empty
                    remaining_ancestors = set(a0).difference(a1)
                    if remaining_ancestors:
                        # if remaining ancestors list is not empty,
                        # this is interpreted as having the leaves from different branches
                        # for example, metadata from func/sub-01/...json must not be mixed with func/sub-02/...json
                        LOGGER.warn("Query returned metadata files from incompatible sources.")
                    deepupdate(metadata, self.query.x2id[ancestors[i][1]].contents)

        return metadata

    def get(self, return_type='object', target=None, scope: str = None,
            extension=None, suffix=None,
            regex_search=False, absolute_paths=None, invalid_filters='error', element_source='*',
            **entities):
        expr = []
        if scope:
            if scope == 'raw':
                # exclude the top level element named 'derivatives' which results
                # in only considering everything else of top level elements
                # TODO this has bad performance, manually filter artifacts after query execution
                expr.append('*[name()!="derivatives"]')
            else:
                expr.append('//%s' % scope)
        entity_filters = []
        result_extractor = None
        if target:
            if target in 'suffixes':
                suffix = '*'
                result_extractor = lambda artifacts: [a.suffix for a in artifacts]
            elif target in 'extensions':
                extension = '*'
                result_extractor = lambda artifacts: [a.extension for a in artifacts]
            else:
                target = self.sc.fuzzy_match_entity_key(target)
                entities = {**entities, target: '*'}
                result_extractor = lambda artifacts: [entity.value for a in artifacts for entity in
                                                      filter(lambda e: e.key == target, a.entities)]
        for k, v in entities.items():
            k = self.sc.fuzzy_match_entity_key(k)
            v = self.sc.process_entity_value(k, v)
            v = self._scalar_or_list('value/text()', v)
            entity_filters.append('entities[key/text()="%s" and %s]' % (k, v))
        if extension:
            v = self._scalar_or_list('extension/text()', extension)
            entity_filters.append(v)
        if suffix:
            v = self._scalar_or_list('suffix/text()', suffix)
            entity_filters.append(v)
        if entity_filters:
            entity_filters_str = ' and '.join(entity_filters)
            expr.append('//%s[%s]' % (element_source, entity_filters_str))
        expr_final = ''.join(expr)
        artifacts = self._query(expr_final, return_lxml_objects=return_type == 'lxml')
        if return_type and return_type.startswith("file"):
            return list(map(lambda e: e.get_absolute_path(), artifacts))
        elif result_extractor:
            return sorted(set(result_extractor(artifacts)))
        return artifacts

    def get_entities(self, scope=None, sort=False):
        select = self.dataset.select(model.EntityRef)
        if scope == 'raw':
            select.subtree(CustomOpExpr(lambda m: not isinstance(m, model.DerivativeFolder)))
        entities = select.objects()
        result = OrderedDict()
        for e in entities:
            if e.key not in result:
                result[e.key] = set()
            result[e.key].add(e.value)
        if sort:
            result = {k: sorted(v) for k, v in sorted(result.items())}
        return result
