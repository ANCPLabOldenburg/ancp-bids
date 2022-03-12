from ancpbids.plugin import ValidationPlugin


class StaticStructureValidationPlugin(ValidationPlugin):
    def execute(self, dataset, report: ValidationPlugin.ValidationReport):
        self.schema = dataset.get_schema()
        gen = dataset.to_generator()
        for obj in gen:
            top_path = obj.get_relative_path().replace("\\", "/") if isinstance(obj, (
                self.schema.File, self.schema.Folder)) else '???'
            members = self.schema.get_members(type(obj))
            for member in members:
                typ = member['type']
                name = member['name']
                lb = member['min']
                ub = member['max']
                val = getattr(obj, name)
                use = member['use']
                if (lb > 0 or use == 'required') and not val:
                    report.error(f"Missing required field {name} at {top_path}.")
                if use == 'recommended' and not val:
                    report.warn(f"Missing recommended field {name} at {top_path}.")


class DatatypesValidationPlugin(ValidationPlugin):
    def execute(self, dataset, report: ValidationPlugin.ValidationReport):
        invalid = []
        valid_datatypes = [v.literal_ for v in dataset.get_schema().DatatypeEnum.__members__.values()]
        for subject in dataset.subjects:
            invalid.extend([f for f in subject.datatypes if f.name not in valid_datatypes])
            for session in subject.sessions:
                invalid.extend([f for f in session.datatypes if f.name not in valid_datatypes])

        for folder in invalid:
            report.error("Unsupported datatype folder '%s'" % folder.get_relative_path())


class EntitiesValidationPlugin(ValidationPlugin):
    def execute(self, dataset, report: ValidationPlugin.ValidationReport):
        schema = dataset.get_schema()
        artifacts = dataset.select(schema.Artifact).get_artifacts()
        entities = list(map(lambda e: e.entity_, list(schema.EntityEnum)))
        expected_key_order = {k: i for i, k in enumerate(entities)}
        expected_order_key = {i: k for i, k in enumerate(entities)}
        for artifact in artifacts:
            entity_refs = artifact.entities
            found_invalid_key = False
            for ref in entity_refs:
                if ref.key not in entities:
                    report.error(
                        "Invalid entity '%s' in artifact '%s'" % (ref.key, artifact.get_relative_path()))
                    found_invalid_key = True
            if found_invalid_key:
                # we cannot check the order of entities if invalid entity found
                continue
            # now, check if order of entities matches order in schema
            keys = list(map(lambda e: e.key, entity_refs))
            actual_keys_order = list(map(lambda k: expected_key_order[k], keys))
            for i in range(0, len(actual_keys_order) - 1):
                if actual_keys_order[i] > actual_keys_order[i + 1]:
                    expected = tuple(map(lambda k: expected_order_key[k], sorted(actual_keys_order)))
                    report.error(
                        "Invalid entities order: expected=%s, found=%s, artifact=%s" % (
                            expected, tuple(keys), artifact.get_relative_path()))
                    break


class SuffixesValidationPlugin(ValidationPlugin):
    def execute(self, dataset, report: ValidationPlugin.ValidationReport):
        pass
