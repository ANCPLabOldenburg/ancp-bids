import json
import math
import sys
from io import StringIO

import yaml


class ClassGenerator:
    def read_yaml(self, file):
        with open(file, 'r') as f:
            s_str = f.read()
        return yaml.load_all(s_str, Loader=yaml.FullLoader)

    def __init__(self, base_schema_file, bids_schema_file, module_version_tag):
        self.module_version_tag = module_version_tag
        docs_gen = self.read_yaml(base_schema_file)
        first_doc = next(docs_gen)
        self.elements = {**first_doc}
        remaining_docs = [doc for doc in docs_gen]
        self.types = {name: schema for doc in remaining_docs for name, schema in doc.items()}
        self.visited_types = {}
        self.base_output = StringIO()
        self.version_output = StringIO()
        self.known_classes = {
            'Model': {
                'fields': [],
                'parent': None
            }
        }

        with open(bids_schema_file, 'r') as stream:
            self.bids_schema = json.load(stream)

    def generate(self, version='0.0.0'):
        self.append(f"""\
from enum import Enum, auto
from typing import List, Union, Dict, Any
from math import inf
import sys

class Model(dict):
    def __init__(self, *args, **kwargs):
        pass

    def __repr__(self):
        return str({{key: (str(value)[:32] + '[...]') if len(str(value)) > 32 else value
                    for key, value in self.items()
                    if value is not None and not isinstance(value, (dict, list))}})
        """)

        self.append_ver(f"""\
from .model_base import *

VERSION = '{version}'
SCHEMA = sys.modules[__name__]
                """)

        # generate types first as they are referenced by the elements and need to be declared before usage
        for name, sub_schema in self.types.items():
            self.visit_schema(name, sub_schema)

        # generate remaining elements
        for name, schema_dict in self.elements.items():
            self.visit_schema(name, schema_dict)

    def append(self, line="", *args):
        self.base_output.write(line)
        self.base_output.write("\n")

    def append_ver(self, line="", *args):
        self.version_output.write(line)
        self.version_output.write("\n")

    def to_python_type(self, class_name, field_name, field_def):
        typ = field_def['type']
        min = int(field_def['min']) if 'min' in field_def else 0
        if min < 0:
            min = 0
        max = int(field_def['max']) if 'max' in field_def else 1
        if max < 0:
            max = math.inf

        meta = field_def['meta'] if 'meta' in field_def else {}
        use = field_def['use'] if 'use' in field_def else 'optional'
        enums = []
        ret = {'type': typ, 'min': min, 'max': max, 'init': 'None', 'meta': meta, 'typehint': typ, 'use': use,
               'enums': enums}

        if max > 1:
            ret['init'] = '[]'
            ret['typehint'] = f'List[{ret["type"]}]'

        if typ == 'enum':
            enum_name = field_name[0].capitalize() + field_name[1:] + "Enum"
            enums.append({'name': enum_name, 'literals': field_def['literals']})
            ret['type'] = enum_name
            ret['typehint'] = class_name + "." + enum_name
        elif typ == 'dict':
            ret['typehint'] = 'Dict'
        elif typ == 'any':
            ret['typehint'] = 'Any'

        return ret

    def init_params(self, class_name):
        if not class_name:
            return []
        current_class_name = class_name
        init_params = []
        parent_init_params = []
        collect_parent_params = False
        while current_class_name is not None:
            known_class = self.known_classes[current_class_name]
            fields = known_class['fields']
            init_params = init_params + fields
            current_class_name = known_class['parent']
            if collect_parent_params:
                parent_init_params = parent_init_params + fields
            # start collecting when processing of first parent starts
            collect_parent_params = True
        return init_params, parent_init_params

    def visit_schema(self, name, schema_dict):
        _extends = 'Model'
        if ".extends" in schema_dict:
            _extends = schema_dict.pop(".extends")
        self.append(f"class {name}({_extends}):")

        if ".doc" in schema_dict:
            self.append(f'    r"""{schema_dict.pop(".doc")}"""')

        fields = []
        collected_members = {}
        for field_name, field_def in schema_dict.items():
            type_info = self.to_python_type(name, field_name, field_def)
            collected_members[field_name] = type_info
            doc = None
            if ".doc" in field_def:
                doc = field_def[".doc"]
            fields.append((field_name, type_info, doc))

            for nested_enum in type_info['enums']:
                self.append(f"    class {nested_enum['name']}(Enum):")
                for literal in nested_enum['literals']:
                    self.append(f"        {literal} = auto()")
                self.append()
        self.known_classes[name] = {
            'fields': fields,
            'parent': _extends
        }

        init_params, parent_init_params = self.init_params(name)
        init_params_str = ', '.join(["%s: '%s' = None" % (key, ti['typehint']) for key, ti, _ in init_params])
        parent_init_params_str = ', '.join(["%s or %s" % (key, ti['init']) for key, ti, _ in parent_init_params])
        self.append(f"    def __init__(self, %s):" % init_params_str)
        self.append(f"        super({name}, self).__init__(%s)" % parent_init_params_str)
        for key, type_info, doc in fields:
            var_init = f"self['{key}'] = {key} or {type_info['init']}"
            self.append(f"        {var_init}")

        self.append()
        for key, type_info, doc in fields:
            if doc:
                doc = "\n        r\"\"\"" + doc + "\"\"\""
            else:
                doc = ""
            typehint = type_info['typehint']
            self.append(f"""    @property
    def {key}(self) -> '{typehint}':{doc}
        return self['{key}']

    @{key}.setter
    def {key}(self, {key}: '{typehint}'):
        self['{key}'] = {key}
            """)

        self.append("    MEMBERS = {")
        for name, type_info in collected_members.items():
            type_ = type_info['type']
            min_ = type_info['min']
            max_ = type_info['max']
            use_ = type_info['use']
            meta_ = str(type_info['meta'])
            self.append(
                f"        '{name}': " + "{" + f"'type': '{type_}', 'min': {min_}, 'max': {max_}, 'use': '{use_}', 'meta': {meta_}" + "},")
        self.append("    }")
        self.append("\n")

    def generate_enum(self, class_name, literals_path, sorter=None):
        generator.append(f"class {class_name}(Enum):")
        generator.append(f" pass")

        generator.append_ver(f"class {class_name}({class_name}):")
        context = self.bids_schema
        for path in literals_path.split("/"):
            context = context[path]
        if callable(sorter):
            context = sorter(context)
        for k, v in context.items():
            generator.append_ver(f" {k} = {v}")


if __name__ == '__main__':
    # extractor = MetadataExtractor("./test.yaml")
    version_tag = 'v1.9.0'
    module_version_tag = version_tag.replace('.', '_')
    generator = ClassGenerator("../schema/model_base.yaml", f"../schema/schema_{version_tag}.json", module_version_tag)
    generator.generate(version_tag)

    generator.generate_enum("DatatypeEnum", "objects/datatypes")
    generator.generate_enum("ModalityEnum", "objects/modalities")
    generator.generate_enum("SuffixEnum", "objects/suffixes")
    #generator.generate_enum("ExtensionEnum", "objects/extensions")

    def sorter(unordered_entities):
        ordered_entities_names = generator.bids_schema["rules"]["entities"]
        ordered_entities = {k: unordered_entities[k] for k in ordered_entities_names}
        return ordered_entities
    generator.generate_enum("EntityEnum", "objects/entities", sorter=sorter)

    generator.base_output.flush()
    generator.base_output.seek(0)
    with open("../ancpbids/model_base.py", 'w') as f:
        f.write(generator.base_output.read())

    generator.version_output.flush()
    generator.version_output.seek(0)
    with open("../ancpbids/model_%s.py" % module_version_tag, 'w') as f:
        f.write(generator.version_output.read())
