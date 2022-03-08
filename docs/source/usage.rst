Usage
=====

.. autosummary::
   :toctree: generated

Load an existing BIDS dataset
-----------------------------

    >>> from ancpbids import load_dataset
    >>> dataset_path = 'path/to/your/dataset'
    >>> dataset = load_dataset(dataset_path)

When loading a dataset, ancpBIDS will create an in-memory representation of it.
This reduces the number of file system operations to a minimum
as subsequent dataset operations can be executed on the in-memory structure.
Keep in mind that any file system structural changes are not observed,
i.e. if you added new files to your dataset after loading it, you have to reload it or start over your script.

Validate a BIDS dataset
-----------------------------
Before processing a BIDS dataset, it is recommended to make sure it has no parts that do not conform to the BIDS specification.

    >>> from ancpbids import load_dataset, validate_dataset
    >>> dataset_path = 'path/to/your/dataset'
    >>> dataset = load_dataset(dataset_path)
    >>> report = validate_dataset(dataset)
    >>> for message in report.messages:
    >>>     print(message)
    >>> if report.has_errors():
    >>>     raise "The dataset contains validation errors, cannot continue".

Note: ancpBIDS' validation rules are very limited at the moment.

Query a BIDS dataset
-----------------------------

Query using the fluent API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Once a dataset is loaded, it is possible to query the in-memory representation using a `fluent API <https://en.wikipedia.org/wiki/Fluent_interface>`_.

    >>> from ancpbids import load_dataset, validate_dataset
    >>> dataset_path = 'path/to/your/dataset'
    >>> dataset = load_dataset(dataset_path)
    >>> file_paths = ds.select(model.Artifact) \
    >>>    .where(all_of(eq(model.Artifact.suffix, model.SuffixEnum.bold.name),
    >>>                 entity(model.EntityEnum.subject, '02'))) \
    >>>    .get_file_paths()
    >>> file_paths = list(file_paths)

In this example, all `Artifacts` (i.e. BIDS files) are selected which have the suffix `bold` and belong to subject `02`.

Query using the PyBIDS API
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ancpBIDS supports a subset of PyBIDS' `BIDSLayout` API. If you are familiar with PyBIDS, you can also extract information from the dataset using its `BIDSLayout.get_...()` interface.
The previous example can be re-written to (more convenient):

    >>> from ancpbids import BIDSLayout
    >>> dataset_path = 'path/to/your/dataset'
    >>> layout = BIDSLayout(dataset_path)
    >>> file_paths = layout.get(suffix='bold', subject='02', return_type='filename')

Technical note: the `BIDSLayout` implementation uses the fluent API.

.. tab:: fmri

    .. code::

        fMRI specific instructions

.. tab:: EEG

    .. code::

        EEG specific instructions

.. tab:: MEG

    .. code::

        MEG specific instructions
        sdfsd fsdf
        sdfsd fsdf sdf

asd asd asd