import itertools

from bids import schema as sc, dataset as ds, validator as vd


class TopLevelFilesValidationRule(vd.ValidationRule):
    def validate(self, schema: sc.Schema, dataset: ds.Dataset, report: vd.ValidationReport):
        top_level_files = schema.top_level_files.load_contents()
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
