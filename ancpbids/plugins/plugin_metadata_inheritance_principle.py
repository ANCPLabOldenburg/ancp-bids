from typing import List

from ancpbids.plugin import SchemaPlugin
from ancpbids.utils import deepupdate


def _get_metadata(artifact, include_entities=False):
    schema = artifact.get_schema()
    parent = artifact.get_parent()
    artifact_entities = {e.key : e.value for e in artifact.entities}
    # first, collect all metadata files matching the artifact
    metadata_levels = []
    while parent is not None:
        parent_metadata_files = parent.select(schema.MetadataArtifact).objects(depth=1)
        # check if a metadata file matches the artifact and merge its fields into the resulting metadata dict
        for parent_mdf in parent_metadata_files:
            match = parent_mdf.suffix == artifact.suffix
            if not match:
                continue
            mdf_entities = {e.key : e.value for e in parent_mdf.entities}
            match = mdf_entities.items() <= artifact_entities.items()
            if match:
                metadata_levels.append(parent_mdf.contents)
        parent = parent.get_parent()

    metadata = {}
    # now apply all metadata fields in reverse order, i.e. by starting from root down to the artifact level
    # this is important as the nearer the file is to the Artifact the higher its priority is
    for mdf in reversed(metadata_levels):
        deepupdate(metadata, mdf)

    if include_entities:
        schema_entities = {e.value['name']: e.name for e in list(schema.EntityEnum)}
        metadata.update({schema_entities[key]: value for key, value in artifact_entities.items()})

    return metadata


class MetadataSchemaPlugin(SchemaPlugin):
    def execute(self, schema):
        schema.Artifact.get_metadata = _get_metadata