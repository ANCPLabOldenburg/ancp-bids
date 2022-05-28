import os.path
import warnings
from collections import OrderedDict
from functools import partial
from typing import List, Union, Dict

import ancpbids
from ancpbids import CustomOpExpr, EntityExpr, AllExpr, ValidationPlugin
from . import load_dataset, LOGGER
from .query import query, query_entities, FnMatchExpr, AnyExpr
from .utils import deepupdate, resolve_segments, convert_to_relative


warnings.warn('Development of the BIDSLayout interface will continue in the pybids project.')

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
        folder = self.dataset
        return query(folder, return_type, target, scope, extension, suffix, **entities)

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
        return query_entities(self.dataset, scope, sort)

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
        context = self.dataset
        filename = convert_to_relative(self.dataset, filename)
        if scope not in ['all', 'raw', 'self']:
            context, _ = resolve_segments(context, scope)
        return context.get_file(filename)

