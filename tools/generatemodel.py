import collections
from io import StringIO

import yaml
import yamale


class ClassGenerator:
    def __init__(self, schema, metadata):
        self.schema = schema
        self.metadata = metadata
        self.visited_includes = {}

        self.output = StringIO()
        self.append("from enum import Enum")
        self.append("from typing import List, Union, Dict")
        self.append()
        self.append("class Model(dict):")
        self.append("    pass")
        self.append()

        for name, sub_schema in schema.includes.items():
            self.visit_schema(name, sub_schema.dict)

        for name, schema_dict in schema.dict.items():
            self.visit_schema(name, schema_dict)

    def append(self, line="", *args):
        self.output.write(line % args)
        self.output.write("\n")

    def to_type_name(self, name):
        return name

    def to_python_type(self, val):
        tag = val.tag
        if tag == 'list':
            sub_type = ''
            if val.args:
                sub_type_descr = val.args[0]
                sub_type = sub_type_descr.tag
                if sub_type == 'include':
                    sub_type = self.to_type_name(sub_type_descr.args[0])
            # return ': List[%s] = []' % sub_type
            return {'type': sub_type, 'list': True, 'init': '[]'}
        if tag == 'enum':
            # return ' = None'
            return {'type': 'Enum', 'list': False, 'init': 'None', 'options': []}
        if tag == 'include':
            # return ': %s = None' % self.to_type_name(val.args[0])
            return {'type': self.to_type_name(val.args[0]), 'list': False, 'init': 'None'}
        if tag == 'map':
            # return ': Dict = {}'
            return {'type': 'Dict', 'list': False, 'init': '{}'}

        if tag == 'num':
            tag = 'float'

        # ": %s = None" % tag
        return {'type': tag, 'list': False, 'init': 'None'}

    def visit_schema(self, name, schema_dict):
        items = {**schema_dict}
        _extends = 'Model'
        md_class_extends = f'/{name}/extends'
        if md_class_extends in self.metadata:
            _extends = self.metadata[md_class_extends]
            _extends = "%s" % self.to_type_name(_extends)
        self.append("class %s(%s):", self.to_type_name(name), _extends)

        md_class_doc = f'/{name}/doc'
        if md_class_doc in self.metadata:
            self.append(f'    """{self.metadata[md_class_doc]}"""')

        fields = []
        collected_members = {}
        for key, val in items.items():
            type_info = self.to_python_type(val)
            typ = type_info['type']
            if type_info['list']:
                typ = f"List[{typ}]"
            collected_members[key] = {
                'type': type_info['type'],
                'list': type_info['list'],
                'kwargs': val.kwargs
            }
            md_doc = f'/{name}/{key}/doc'
            doc = None
            if md_doc in self.metadata:
                doc = self.metadata[md_doc]
            fields.append((key, val, type_info, typ, doc))

        self.append(f"    def __init__(self):")
        self.append(f"        super({name}, self).__init__()")
        for key, val, type_info, typ, doc in fields:
            var_init = f"self['{key}']: {typ} = {type_info['init']}"
            self.append("        %s", var_init)

        self.append()
        for key, val, type_info, typ, doc in fields:
            self.append(f"""    @property
    def {key}(self) -> '{typ}':
        return self['{key}']
    
    @{key}.setter
    def {key}(self, {key}: '{typ}'):
        self['{key}'] = {key}
            """)

        self.append(f"    MEMBERS = {str(collected_members)}")
        self.append("\n")


class MetadataExtractor:
    def __init__(self, schema_path):
        with open(schema_path, 'r') as f:
            s_str = f.read()
        schema_docs = yaml.load_all(s_str, Loader=yaml.FullLoader)
        self.metadata = {}
        self.extends = []
        modified_schemas = []
        for schema_doc in schema_docs:
            modified_schemas.append(schema_doc)
            self._strip_off_metadata(schema_doc)
        self.result_wo_extensions = yaml.dump_all(modified_schemas, sort_keys=False)

        all_schemas = {t: d for s in modified_schemas for t, d in s.items()}
        for obj_dict, super_type in self.extends:
            extends = all_schemas[super_type]
            obj_dict.update(extends)

        self.result_w_extensions = yaml.dump_all(modified_schemas, sort_keys=False)

    def _strip_off_metadata(self, obj_dict, context='', parent_dict=None, parent_key=None):
        for k, v in {**obj_dict}.items():
            if isinstance(v, collections.abc.Mapping):
                self._strip_off_metadata(v, '%s/%s' % (context, k), obj_dict, k)
            else:
                if k.startswith('.'):
                    obj_dict.pop(k)
                    k = k[1:]
                    if k == 'rule':
                        parent_dict[parent_key] = v
                    else:
                        path = '%s/%s' % (context, k)
                        self.metadata[path] = v

                    if k == 'extends':
                        self.extends.append((obj_dict, v))


if __name__ == '__main__':
    # extractor = MetadataExtractor("./test.yaml")
    extractor = MetadataExtractor("../ancpbids/data/schema-files/v1_6/bids.yaml")
    schema = yamale.make_schema(content=extractor.result_wo_extensions)
    visitor = ClassGenerator(schema, extractor.metadata)
    visitor.append(f'YAMALE_SCHEMA = """\n{extractor.result_w_extensions}"""')
    visitor.output.flush()
    visitor.output.seek(0)
    with open("../ancpbids/model.py", 'w') as f:
        f.write(visitor.output.read())
