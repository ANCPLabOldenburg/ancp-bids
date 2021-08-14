import itertools

from bids import schema as sc, model , validator as vd


class TopLevelFilesValidationRule(vd.ValidationRule):
    def validate(self, schema: sc.Schema, dataset: ds.Dataset, report: vd.ValidationReport):
        top_level_files = schema.top_level_files
        files = dataset.folder.get_files(include_folders=False)
        for key in top_level_files:
            file_schema = top_level_files[key]
            extensions = file_schema["extensions"]
            extensions = list(filter(lambda ext: ext != 'NONE' and ext.startswith('.'), extensions))
            probes = list(itertools.zip_longest([], extensions, fillvalue=key))
            probes = list(map(lambda probe: probe[0] + probe[1], probes))
            if not probes:
                probes = [key]
            found = list(filter(lambda file: file.name() in probes, files))
            if not found and file_schema['required']:
                report.error("Missing required top level file '%s'" % key)


class AssociatedDataValidationRule(vd.ValidationRule):
    def validate(self, schema: sc.Schema, dataset: ds.Dataset, report: vd.ValidationReport):
        pass


class DatatypesValidationRule(vd.ValidationRule):
    def validate(self, schema: sc.Schema, dataset: ds.Dataset, report: vd.ValidationReport):
        for subject in dataset.get_subjects():
            for session in subject.get_sessions():
                for datatype in session.get_datatypes():
                    if datatype.name not in schema.datatypes:
                        dt_path = "%s/%s/%s" % (subject.name, session.name, datatype.name)
                        report.error("Unsupported datatype folder '%s'" % dt_path)


class EntitiesValidationRule(vd.ValidationRule):
    def validate(self, schema: sc.Schema, dataset: ds.Dataset, report: vd.ValidationReport):
        for subject in dataset.get_subjects():
            for session in subject.get_sessions():
                for datatype in session.get_datatypes():
                    if datatype.name not in schema.datatypes:
                        continue
                    dt_config = schema.datatypes[datatype.name]
                    for artifact in datatype.get_artifacts():
                        entities = {**artifact.get_entities()}
                        if not entities:
                            report.error("Artifact name does not match expected pattern '%s'" % artifact.name)
                            continue
                        suffix = entities.pop('suffix')
                        if not suffix:
                            report.error(
                                "Artifact has no suffix '%s'" % artifact.file.file_path)
                            continue
                        dt_found = next(filter(lambda dt: suffix in dt['suffixes'], dt_config))
                        if not dt_found:
                            report.error("Datatype '%s' does not support suffix '%s'" % (datatype.name, suffix))
                            continue
                        extension = entities.pop('extension')
                        if extension not in dt_found['extensions']:
                            report.error(
                                "Datatype '%s' does not support artifact extension '%s'" % (datatype.name, extension))
                            continue
                        dt_entities = dt_found['entities']
                        for key in entities.keys():
                            entity_name = schema.get_entity_by_abbrev(key)
                            if entity_name is None:
                                report.error(
                                    "Invalid entity '%s' in artifact '%s'" % (key, artifact.name))
                                continue
                            if entity_name not in dt_entities:
                                report.error(
                                    "Datatype '%s' does not support entity '%s' in artifact  '%s'" % (
                                        datatype.name, key, artifact.name))
                                continue
                        # TODO check if order of entities is as expected
                        if False and list(dt_entities.keys()) != list(entities.keys()):
                            report.error(
                                "Invalid entities order in artifact: expected %s, encountered %s" % (
                                list(dt_entities.keys()), list(entities.keys())))
                            continue


class SuffixesValidationRule(vd.ValidationRule):
    def validate(self, schema: sc.Schema, dataset: ds.Dataset, report: vd.ValidationReport):
        pass
