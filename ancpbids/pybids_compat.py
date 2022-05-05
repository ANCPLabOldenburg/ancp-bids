import os.path
from collections import OrderedDict
from functools import partial
from typing import List, Union, Dict

import ancpbids
from ancpbids import CustomOpExpr, EntityExpr, AllExpr, ValidationPlugin
from . import load_dataset, LOGGER
from .plugins.plugin_query import FnMatchExpr, AnyExpr
from .utils import deepupdate


class BIDSLayout:
    """A convenience class to provide access to an in-memory representation of a BIDS dataset.

    .. code-block::

        dataset_path = 'path/to/your/dataset'
        layout = BIDSLayout(dataset_path)

    Parameters
    ----------
    ds_dir:
        the (absolute) path to the dataset to load
    """

    def __init__(self, ds_dir: str, **kwargs):
        self.dataset = load_dataset(ds_dir)
        self.schema = self.dataset.get_schema()

    def _to_any_expr(self, value, ctor):
        # if the value is a list, then wrap it in an AnyExpr
        if isinstance(value, list):
            ops = []
            for v in value:
                ops.append(ctor(v))
            return AnyExpr(*ops)
        # else just return using the constructor function
        return ctor(value)

    def __getattr__(self, key):
        # replace arbitrary get functions with calls to get
        if key.startswith("get_"):
            return partial(self.get, "id", key[4:])

        # give up if the above don't work
        raise AttributeError(key)

    def get_metadata(self, path, include_entities=False, scope='all'):
        """Return metadata found in JSON sidecars for the specified file.

        Parameters
        ----------
        path : str
            Path to the file to get metadata for.
        include_entities : bool, optional
            If True, all available entities extracted
            from the filename (rather than JSON sidecars) are included in
            the returned metadata dictionary.
        scope : str or list, optional
            The scope of the search space. Each element must
            be one of 'all', 'raw', 'self', 'derivatives', or a
            BIDS-Derivatives pipeline name. Defaults to searching all
            available datasets.

        Returns
        -------
        dict
            A dictionary of key/value pairs extracted from all of the
            target file's associated JSON sidecars.

        Notes
        -----
        A dictionary containing metadata extracted from all matching .json
        files is returned. In cases where the same key is found in multiple
        files, the values in files closer to the input filename will take
        precedence, per the inheritance rules in the BIDS specification.

        """
        path = os.path.normpath(path)
        # make relative to dataset root, i.e., remove base path
        if path.startswith(self.dataset.base_dir_):
            path = path[len(self.dataset.base_dir_):].strip(os.sep)
        file = self.dataset.get_file(path)
        md = file.get_metadata()
        if md and include_entities:
            schema_entities = {e.entity_: e.literal_ for e in list(self.schema.EntityEnum)}
            md.update({schema_entities[e.key]: e.value for e in file.entities})
        return md

    def _require_artifact(self, expr) -> AllExpr:
        """Wraps the provided expression in an expression that makes sure the context of evaluation is an Artifact.

        Parameters
        ----------
        expr :
            the expression to wrap

        Returns
        -------
            a wrapping expression to make sure that the provided object is an instance of Artifact
        """
        return AllExpr(CustomOpExpr(lambda m: isinstance(m, self.schema.Artifact)), expr)

    def get(self, return_type: str = 'object', target: str = None, scope: str = None,
            extension: Union[str, List[str]] = None, suffix: Union[str, List[str]] = None,
            **entities) -> Union[List[str], List[object]]:
        """Depending on the return_type value returns either paths to files that matched the filtering criteria
        or :class:`Artifact <ancpbids.model_v1_7_0.Artifact>` objects for further processing by the caller.

        Note that all provided filter criteria are AND combined, i.e. subj='02',task='lang' will match files containing
        '02' as a subject AND 'lang' as a task. If you provide a list of values for a criteria, they will be OR combined.

        .. code-block::

            file_paths = layout.get(subj='02', task='lang', suffix='bold', return_type='files')

            file_paths = layout.get(subj=['02', '03'], task='lang', return_type='files')

        Parameters
        ----------
        return_type:
            Either 'files' to return paths of matched files
            or 'object' to return :class:`Artifact <ancpbids.model_v1_7_0.Artifact>` object, defaults to 'object'

        target:
            Either `suffixes`, `extensions` or one of any valid BIDS entities key
            (see :class:`EntityEnum <ancpbids.model_v1_7_0.EntityEnum>`, defaults to `None`
        scope:
            a hint where to search for files
            If passed, only nodes/directories that match the specified scope will be
            searched. Possible values include:
            'all' (default): search all available directories.
            'derivatives': search all derivatives directories.
            'raw': search only BIDS-Raw directories.
            'self': search only the directly called BIDSLayout.
            <PipelineName>: the name of a BIDS-Derivatives pipeline.
        extension:
            criterion to match any files containing the provided extension only
        suffix:
            criterion to match any files containing the provided suffix only
        entities
            a list of key-values to match the entities of interest, example: subj='02',task='lang'

        Returns
        -------
            depending on the return_type value either paths to files that matched the filtering criteria
            or Artifact objects for further processing by the caller
        """
        if scope is None:
            scope = 'all'
        if return_type == 'id':
            if not target:
                raise ValueError("return_type=id requires the target parameter to be set")

        context = self.dataset
        ops = []
        target_type = self.schema.File
        if scope.startswith("derivatives"):
            context = self.dataset.derivatives
            # we already consumed the first path segment
            segments = os.path.normpath(scope).split(os.sep)[1:]
            for segment in segments:
                context = context.get_folder(segment)
            # derivatives may contain non-artifacts which should also be considered
            target_type = self.schema.File

        select = context.select(target_type)

        if scope == 'raw':
            # the raw scope does not consider derivatives folder but everything else
            select.subtree(CustomOpExpr(lambda m: not isinstance(m, self.schema.DerivativeFolder)))

        result_extractor = None
        if target:
            if target in 'suffixes':
                suffix = '*'
                result_extractor = lambda artifacts: [a.suffix for a in artifacts]
            elif target in 'extensions':
                extension = '*'
                result_extractor = lambda artifacts: [a.extension for a in artifacts]
            else:
                target = self.schema.fuzzy_match_entity_key(target)
                entities = {**entities, target: '*'}
                result_extractor = lambda artifacts: [entity.value for a in artifacts for entity in
                                                      filter(lambda e: e.key == target, a.entities)]

        for k, v in entities.items():
            entity_key = self.schema.fuzzy_match_entity(k)
            v = self.schema.process_entity_value(k, v)
            ops.append(
                self._require_artifact(self._to_any_expr(v, lambda val: EntityExpr(self.schema, entity_key, val))))

        if extension:
            ops.append(self._require_artifact(
                self._to_any_expr(extension, lambda ext: FnMatchExpr(self.schema.Artifact.extension, ext))))

        if suffix:
            ops.append(
                self._require_artifact(
                    self._to_any_expr(suffix, lambda suf: FnMatchExpr(self.schema.Artifact.suffix, suf))))

        select.where(AllExpr(*ops))

        if return_type and return_type.startswith("file"):
            return list(select.get_file_paths_absolute())
        else:
            artifacts = select.objects()
            if result_extractor:
                return sorted(set(result_extractor(artifacts)))
            return list(artifacts)

    def get_entities(self, scope: str = None, sort: bool = False) -> dict:
        """Returns a unique set of entities found within the dataset as a dict.
        Each key of the resulting dict contains a list of values (with at least one element).

        Example dict:
        .. code-block::

            {
                'sub': ['01', '02', '03'],
                'task': ['gamblestask']
            }

        Parameters
        ----------
        scope:
            see BIDSLayout.get()
        sort: default is `False`
            whether to sort the keys by name

        Returns
        -------
        dict
            a unique set of entities found within the dataset as a dict
        """
        artifacts = filter(lambda m: isinstance(m, self.schema.Artifact), self.get(scope=scope))
        result = OrderedDict()
        for e in [e for a in artifacts for e in a.entities]:
            if e.key not in result:
                result[e.key] = set()
            result[e.key].add(e.value)
        if sort:
            result = {k: sorted(v) for k, v in sorted(result.items())}
        return result

    def get_dataset_description(self, scope='self', all_=False) -> Union[List[Dict], Dict]:
        """Return contents of dataset_description.json.

        Parameters
        ----------
        scope : str
            The scope of the search space. Only descriptions of
            BIDSLayouts that match the specified scope will be returned.
            See :obj:`bids.layout.BIDSLayout.get` docstring for valid values.
            Defaults to 'self' --i.e., returns the dataset_description.json
            file for only the directly-called BIDSLayout.
        all_ : bool
            If True, returns a list containing descriptions for
            all matching layouts. If False (default), returns for only the
            first matching layout.

        Returns
        -------
        dict or list of dict
            a dictionary or list of dictionaries (depending on all_).
        """
        all_descriptions = self.dataset.select(self.schema.DatasetDescriptionFile).objects(as_list=True)
        if all_:
            return all_descriptions
        return all_descriptions[0] if all_descriptions else None

    def get_dataset(self) -> object:
        """
        Returns
        -------
            the in-memory representation of this layout/dataset
        """
        return self.dataset

    def add_derivatives(self, path):
        # TODO: properly add to graph
        if not hasattr(self, 'derivatives'):
            self.derivatives = dict()
        if not isinstance(path, list):
            path = [path]
        for p in path:
            tmp_layout = BIDSLayout(p)
            self.derivatives[tmp_layout.dataset.name] = tmp_layout
            del tmp_layout

    def write_derivative(self, derivative):
        """Writes the provided derivative folder to the dataset.
        Note that a 'derivatives' folder will be created if not present.

        Parameters
        ----------
        derivative:
            the derivative folder to write
        """
        assert isinstance(derivative, self.schema.DerivativeFolder)
        ancpbids.write_derivative(self.dataset, derivative)

    def validate(self) -> ValidationPlugin.ValidationReport:
        """Validates a dataset and returns a report object containing any detected validation errors.

        Example
        ----------

        .. code-block::

            report = layout.validate()
            for message in report.messages:
                print(message)
            if report.has_errors():
                raise "The dataset contains validation errors, cannot continue".

        Returns
        -------
            a report object containing any detected validation errors or warning
        """
        return ancpbids.validate_dataset(self.dataset)

    @property
    def files(self):
        return self.get_files()

    def get_files(self, scope='all'):
        """Get BIDSFiles for all layouts in the specified scope.

        Parameters
        ----------
        scope : str
            The scope of the search space. Indicates which
            BIDSLayouts' entities to extract.
            See :obj:`bids.layout.BIDSLayout.get` docstring for valid values.


        Returns:
            A dict, where keys are file paths and values
            are :obj:`bids.layout.BIDSFile` instances.

        """
        all_files = self.get(return_type="object", scope=scope)
        files = {file.get_absolute_path(): file for file in all_files}
        return files

    def get_file(self, filename, scope='all'):
        """Return the BIDSFile object with the specified path.

        Parameters
        ----------
        filename : str
            The path of the file to retrieve. Must be either an absolute path,
            or relative to the root of this BIDSLayout.
        scope : str or list, optional
            Scope of the search space. If passed, only BIDSLayouts that match
            the specified scope will be searched. See :obj:`BIDSLayout.get`
            docstring for valid values. Default is 'all'.

        Returns
        -------
        :obj:`bids.layout.BIDSFile` or None
            File found, or None if no match was found.
        """
        return self.dataset.get_file(filename)

    @property
    def description(self):
        return self.get_dataset_description()

    @property
    def root(self):
        return self.dataset.base_dir_

    def __repr__(self):
        """Provide a tidy summary of key properties."""
        ents = self.get_entities()
        n_subjects = len(set(ents['sub']))
        n_sessions = len(set(ents['ses']))
        n_runs = len(set(ents['run']))
        s = ("BIDS Layout: ...{} | Subjects: {} | Sessions: {} | "
             "Runs: {}".format(self.dataset.base_dir_, n_subjects, n_sessions, n_runs))
        return s
