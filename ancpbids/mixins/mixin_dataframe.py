from ancpbids.plugin import mixin


@mixin(target="ancpbids.pybids_compat:BIDSLayout", ranking=0)
class DataFrameMixin:
    """Adds a pandas export for files tracked by a layout."""

    def to_df(self, metadata=False, **filters):
        """Return information for files tracked in Layout as a pandas DataFrame.

        Parameters
        ----------
        metadata : bool, optional
            If True, includes columns for all metadata fields.
            If False, only filename-based entities are included as columns.
        filters : dict, optional
            Optional keyword arguments passed on to get(). This allows
            one to easily select only a subset of files for export.

        Returns
        -------
        :obj:`pandas.DataFrame`
            A pandas DataFrame, where each row is a file, and each column is
            a tracked entity. NaNs are injected whenever a file has no
            value for a given attribute.
        """
        try:
            import pandas as pd
        except ImportError as exc:
            raise ImportError('Missing dependency: "pandas"') from exc

        filters.pop('return_type', None)
        files = self.get(return_type='object', **filters)
        if not files:
            return pd.DataFrame(columns=['path'])

        entity_names = {e.value['name']: e.name for e in self.schema.EntityEnum}
        rows = [self._file_to_row(file, entity_names, metadata) for file in files]
        df = pd.DataFrame(rows)
        return df[['path'] + [c for c in df.columns if c != 'path']]

    def _file_to_row(self, file, entity_names, metadata):
        row = {'path': file.get_absolute_path()}
        if file.extension:
            row['extension'] = file.extension
        if not isinstance(file, self.schema.Artifact):
            return row
        if file.suffix:
            row['suffix'] = file.suffix
        if file.datatype:
            row['datatype'] = file.datatype
        for entity in file.entities:
            row[entity_names.get(entity.key, entity.key)] = entity.value
        if metadata:
            sidecar = file.get_metadata(include_entities=False) or {}
            for key, value in sidecar.items():
                if key not in row:
                    row[key] = value
        return row
