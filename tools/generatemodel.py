import os.path

import math
from io import StringIO

import yaml


class ClassGenerator:
    def read_yaml(self, file):
        with open(file, 'r') as f:
            s_str = f.read()
        return yaml.load_all(s_str, Loader=yaml.FullLoader)

    def __init__(self, schema_file):
        docs_gen = self.read_yaml(schema_file)
        first_doc = next(docs_gen)
        self.elements = {**first_doc}
        remaining_docs = [doc for doc in docs_gen]
        self.types = {name: schema for doc in remaining_docs for name, schema in doc.items()}
        self.visited_types = {}
        self.output = StringIO()

    def generate(self):
        self.append("from enum import Enum, auto")
        self.append("from typing import List, Union, Dict, Any")
        self.append("from math import inf")
        self.append()
        self.append("class Model(dict):")
        self.append("    pass")
        self.append()

        # generate types first as they are referenced by the elements and need to be declared before usage
        for name, sub_schema in self.types.items():
            self.visit_schema(name, sub_schema)

        # generate remaining elements
        for name, schema_dict in self.elements.items():
            self.visit_schema(name, schema_dict)

    def append(self, line="", *args):
        self.output.write(line)
        self.output.write("\n")

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

        self.append(f"    def __init__(self):")
        self.append(f"        super({name}, self).__init__()")
        for key, type_info, doc in fields:
            var_init = f"self['{key}']: {type_info['typehint']} = {type_info['init']}"
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

    def generate_enum(self, yaml_path, name, *additional_fields, dict_transformer=None):
        dt_docs = generator.read_yaml(yaml_path)
        datatypes = [doc for doc in dt_docs]
        datatypes = {name: schema for doc in datatypes for name, schema in doc.items()}
        if dict_transformer:
            datatypes = dict_transformer(datatypes)
        generator.append(f"class {name}(Enum):")
        for name, schema in datatypes.items():
            fields = [f"r\"{schema['name']}\""]
            if additional_fields:
                fields += list(map(lambda f: f"r\"{schema[f] if f in schema else ''}\"", additional_fields))
            generator.append(f"    {name} = {', '.join(fields)}")
            if 'description' in schema and schema['description'] and schema['description'].strip():
                generator.append(f"    r\"\"\"{schema['description'].strip()}\"\"\"")
        generator.append()
        if additional_fields:
            fields = list(map(lambda f: f"{f}_", additional_fields))
            generator.append(f"    def __init__(self, value, {', '.join(fields)}):")
            for field in fields:
                generator.append(f"        self.{field} = {field}")
            generator.append()


if __name__ == '__main__':
    # extractor = MetadataExtractor("./test.yaml")
    version_tag = "v1_7_0"
    generator = ClassGenerator("../ancpbids/data/bids_%s.yaml" % version_tag)
    generator.generate()

    generator.generate_enum("../../bids-specification/src/schema/objects/datatypes.yaml", "DatatypeEnum")
    generator.generate_enum("../../bids-specification/src/schema/objects/modalities.yaml", "ModalityEnum")
    generator.generate_enum("../../bids-specification/src/schema/objects/suffixes.yaml", "SuffixEnum", "unit")


    def transformer(entities):
        order_docs = generator.read_yaml("../../bids-specification/src/schema/rules/entities.yaml")
        order_docs = [item for doc in order_docs for item in doc]
        new_order = {k: entities[k] for k in order_docs}
        return new_order


    generator.generate_enum("../../bids-specification/src/schema/objects/entities.yaml", "EntityEnum",
                            "entity", "type", "format", dict_transformer=transformer)

    generator.output.flush()
    generator.output.seek(0)
    with open("../ancpbids/model_%s.py" % version_tag, 'w') as f:
        f.write(generator.output.read())
