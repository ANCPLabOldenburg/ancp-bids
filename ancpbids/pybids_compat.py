import os.path
from collections import OrderedDict
from functools import partial
from typing import List, Union

import ancpbids
from ancpbids import CustomOpExpr, EntityExpr, AllExpr, ValidationPlugin
from . import load_dataset, model, LOGGER
from .plugins.plugin_query import FnMatchExpr, AnyExpr
from .utils import deepupdate


class BIDSLayout:
    """A convenience class to provide access to an in-memory representation of a BIDS dataset.

    :param ds_dir: the (absolute) path to the dataset to load
    :type ds_dir: str

    .. code-block::

        dataset_path = 'path/to/your/dataset'
        layout = BIDSLayout(dataset_path)
    """

    def __init__(self, ds_dir: str, **kwargs):
        self.dataset = load_dataset(ds_dir)

    def _to_any_expr(self, value, ctor):
        # if the value is a list, then wrap it in an AnyExpr
        if isinstance(value, list):
            ops = []
            for v in value:
                ops.append(ctor(v))
            return AnyExpr(*ops)
        # else just return using the constructor function
        return ctor(value)

    def __getattr__(self, key, **kwargs):
        k = key if not key.startswith("get_") else key[4:]
        return partial(self.get, return_type='id', target=k, **kwargs)

    def get_metadata(self, *args, **kwargs):
        """
        Returns a dictionary of metadata matching the provided criteria (see :meth:`ancpbids.BIDSLayout.get`).
        Also takes the BIDS inheritance principle into account, i.e. any metadata defined at dataset level
        may be overridden by a more specific metadata entry at a lower level such as the subject level.

        As of the BIDS specification, metadata is kept in JSON files.

        """
        qry_result = filter(lambda a: isinstance(a, model.MetadataFile), self.get(*args, **kwargs))
        # build lists of ancestors + the leaf (metadata file)
        ancestors = list(map(lambda e: (list(reversed(list(e.iterancestors()))), e), qry_result))
        # sort by number of ancestors
        # TODO must sort by the items within the list not just by length of list
        # example: [xyz,abc] would be treated the same when it should be [abc, xyz]
        ancestors.sort(key=lambda e: len(e[0]))

        metadata = {}
        if ancestors:
            # start with first metadata file
            deepupdate(metadata, ancestors[0][1].contents)
            if len(ancestors) > 1:
                for i in range(1, len(ancestors)):
                    a0 = ancestors[i - 1][0]
                    a1 = ancestors[i][0]
                    # remove the ancestors from a0 and make sure it is empty
                    remaining_ancestors = set(*a0).difference(*a1)
                    if remaining_ancestors:
                        # if remaining ancestors list is not empty,
                        # this is interpreted as having the leaves from different branches
                        # for example, metadata from func/sub-01/...json must not be mixed with func/sub-02/...json
                        LOGGER.warn("Query returned metadata files from incompatible sources.")
                    deepupdate(metadata, ancestors[i][1].contents)

        return metadata

    def _require_artifact(self, expr):
        """
        :param expr: the expression to wrap
        :return: a wrapping expression to make sure that the provided object is an instance of model.Artifact
        """
        return AllExpr(CustomOpExpr(lambda m: isinstance(m, model.Artifact)), expr)

    def get(self, return_type: str = 'object', target: str = None, scope: str = 'all',
            extension: Union[str, List[str]] = None, suffix: Union[str, List[str]] = None,
            **entities):
        """
        Depending on the return_type value returns either paths to files that matched the filtering criteria
        or :class:`Artifact <ancpbids.model_v1_7_0.Artifact>` objects for further processing by the caller.

        Note that all provided filter criteria are AND combined, i.e. subj='02',task='lang' will match files containing
        '02' as a subject AND 'lang' as a task. If you provide a list of values for a criteria, they will be OR combined.

        .. code-block::

            file_paths = layout.get(subj='02', task='lang', suffix='bold', return_type='files')

            file_paths = layout.get(subj=['02', '03'], task='lang', return_type='files')


        :param return_type: Either 'files' to return paths of matched files
            or 'object' to return :class:`Artifact <ancpbids.model_v1_7_0.Artifact>` object, defaults to 'object'

        :param target: Either `suffixes`, `extensions` or one of any valid BIDS entities key
            (see :class:`EntityEnum <ancpbids.model_v1_7_0.EntityEnum>`, defaults to `None`

        :param scope: a hint where to search for files
            If passed, only nodes/directories that match the specified scope will be
            searched. Possible values include:
            'all' (default): search all available directories.
            'derivatives': search all derivatives directories.
            'raw': search only BIDS-Raw directories.
            'self': search only the directly called BIDSLayout.
            <PipelineName>: the name of a BIDS-Derivatives pipeline.

        :param extension: criterion to match any files containing the provided extension only

        :param suffix: criterion to match any files containing the provided suffix only

        :param entities: a list of key-values to match the entities of interest, example: subj='02',task='lang'

        :return: depending on the return_type value either paths to files that matched the filtering criteria
            or Artifact objects for further processing by the caller
        """
        if return_type == 'id':
            if not target:
                raise ValueError("return_type=id requires the target parameter to be set")

        context = self.dataset
        ops = []
        target_type = model.File
        if scope.startswith("derivatives"):
            context = self.dataset.derivatives
            # we already consumed the first path segment
            segments = os.path.normpath(scope).split(os.sep)[1:]
            for segment in segments:
                context = context.get_folder(segment)
            # derivatives may contain non-artifacts which should also be considered
            target_type = model.File

        select = context.select(target_type)

        if scope == 'raw':
            # the raw scope does not consider derivatives folder but everything else
            select.subtree(CustomOpExpr(lambda m: not isinstance(m, model.DerivativeFolder)))

        result_extractor = None
        if target:
            if target in 'suffixes':
                suffix = '*'
                result_extractor = lambda artifacts: [a.suffix for a in artifacts]
            elif target in 'extensions':
                extension = '*'
                result_extractor = lambda artifacts: [a.extension for a in artifacts]
            else:
                target = model.fuzzy_match_entity_key(target)
                entities = {**entities, target: '*'}
                result_extractor = lambda artifacts: [entity.value for a in artifacts for entity in
                                                      filter(lambda e: e.key == target, a.entities)]

        for k, v in entities.items():
            entity_key = model.fuzzy_match_entity(k)
            v = model.process_entity_value(k, v)
            ops.append(self._require_artifact(self._to_any_expr(v, lambda val: EntityExpr(entity_key, val))))

        if extension:
            ops.append(self._require_artifact(
                self._to_any_expr(extension, lambda ext: FnMatchExpr(model.Artifact.extension, ext))))

        if suffix:
            ops.append(
                self._require_artifact(self._to_any_expr(suffix, lambda suf: FnMatchExpr(model.Artifact.suffix, suf))))

        select.where(AllExpr(*ops))

        if return_type and return_type.startswith("file"):
            return list(select.get_file_paths_absolute())
        else:
            artifacts = select.objects()
            if result_extractor:
                return sorted(set(result_extractor(artifacts)))
            return list(artifacts)

    def get_entities(self, scope=None, sort=False):
        artifacts = filter(lambda m: isinstance(m, model.Artifact), self.get(scope=scope))
        result = OrderedDict()
        for e in [e for a in artifacts for e in a.entities]:
            if e.key not in result:
                result[e.key] = set()
            result[e.key].add(e.value)
        if sort:
            result = {k: sorted(v) for k, v in sorted(result.items())}
        return result

    def get_dataset_description(self) -> dict:
        """
        :return: the dataset's dataset_description.json as a dictionary or None if not provided
        """
        return self.dataset.dataset_description

    def get_dataset(self) -> model.Dataset:
        """
        :return: the in-memory representation of this layout/dataset
        """
        return self.dataset

    def write_derivative(self, derivative: model.DerivativeFolder):
        """
        Writes the provided derivative folder to the dataset.
        Note that a 'derivatives' folder will be created if not present.

        :param derivative: the derivative folder to write
        """
        ancpbids.write_derivative(self.dataset, derivative)

    def validate(self) -> ValidationPlugin.ValidationReport:
        """
        Validates a dataset and returns a report object containing any detected validation errors.

        Example:

        .. code-block::

            report = layout.validate()
            for message in report.messages:
                print(message)
            if report.has_errors():
                raise "The dataset contains validation errors, cannot continue".


        :return: a report object containing any detected validation errors or warning
        """
        return ancpbids.validate_dataset(self.dataset)
