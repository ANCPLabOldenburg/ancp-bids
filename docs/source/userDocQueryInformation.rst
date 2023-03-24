User Documentation
===================

Querying information about a BIDS dataset
-----------------------------------------------

.. autosummary::
   :toctree: generated

A core functionality of ancpBIDS is to query information in a BIDS compatible dataset.
Any file in a BIDS dataset that does not conform to the BIDS naming convention will be available as a File object instead of an Artifact.
This allows to also process ordinary files that are not (yet) part of the BIDS specification.

An online version can be found `here`_.

.. _here: https://bids-specification.readthedocs.io/en/stable/


Load an existing BIDS dataset
-----------------------------
To get started, we download a test dataset from https://github.com/ANCPLabOldenburg/ancp-bids-dataset.
These datasets are only meant to experiment with ancpBIDS and not expected to be used in research.

.. code-block:: python

    from ancpbids import utils
    dataset_path = utils.fetch_dataset('ds005')

If fetching the dataset succeeds, you will find a file ds005-testdata.zip in your home folder in '~/.ancp-bids/datasets'
and the contents of that zip file extracted to '~/.ancp-bids/datasets/ds005' as well.
If the dataset has already been downloaded within a previous call to `fetch_dataset()`, then it will not be downloaded again.

If you have your own BIDS dataset, then feel free to use those instead - and do not forget to adapt the following code to your specific dataset.

Now, after we have the path to our dataset folder, we read information about a BIDS dataset into a layout-object using BIDSLayout.
BIDSLayout takes as input the absolute or relative path to a BIDS-dataset and returns a layout in which most of the information about the dataset is held in-memory.

.. code-block:: python

    from ancpbids import BIDSLayout
    layout = BIDSLayout(dataset_path)

Note that in order optimize speed, BIDSLayout does not perform a deep search within data files.
It only reads and parses the files and directories necessary to gather information defined in the BIDS specification.

Perform some basic queries
--------------------------
We can now use several functions to query information about the dataset.
For example, we can ask which subjects are in the dataset:

.. code-block:: python

    subs=layout.get_subjects()
    print(subs)
    #Output:
    # ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16']

This will provide a list of all subject names in the dataset.

Next, let us see how many runs there are.

.. code:: python

    runs=layout.get_runs()
    print(runs)
    #Output:
    #['1', '2', '3']

Note that the returned runs are collected over all subjects,
i.e. it is not guaranteed that each participant has the same number of runs.

Now, the task

.. code-block:: python

    task=layout.get_task()
    print(task)
    #Output:
    #['mixedgamblestask']

These simple queries should support most of the `entities defined in BIDS`_. The queries are constructed as **layout.get_NameOfTheEntity()**.
The query will return '[]' (empty list) if the entity does not exist in the dataset or if a wrong string was provided as part of the 'get\_' call.

.. _entities defined in BIDS: https://bids-specification.readthedocs.io/en/stable/99-appendices/09-entities.html


Query available entities and metadata
---------------------------------------
The command layout.get_entities() returns a dictionary with all entities defined in the dataset and their values.

.. code-block:: python

    avail_entitities=layout.get_entities()
    print("Entities: ", list(avail_entitities.keys()))
    print("Value of task: ", avail_entitities['task']
    #Output:
    #Entities:  ['task', 'sub', 'run', 'ds', 'type']
    #Value of task:  {'mixedgamblestask'}

Note that BIDS allows the definition of `non standard labels and indexes in filenames`_.

.. _non standard labels and indexes in filenames: https://bids-specification.readthedocs.io/en/stable/02-common-principles.html#participant-names-and-other-labels

Metadata from json files can be queried using layout.get_metadata(entity='abc',suffix='xyz'). It will return a dictionary with keys and values

.. code-block:: python

    metadata = layout.get_metadata(task='mixedgamblestask', suffix='bold')
    print("metadata: ", list(metadata.keys()))
    print("Value of RepetitionTime: ", metadata['RepetitionTime'])
    #Output:
    #metadata:  ['RepetitionTime', 'TaskName', 'SliceTiming']
    #Value of RepetitionTime:  2.0


Retrieving matching filenames
-----------------------------
The layout.get() function allows for more complex queries and can return a list of files matching the query.

.. code-block:: python

    file_paths = layout.get(suffix='bold', subject='02', return_type='filename')
    print("BOLD files of subject 2:", *file_paths, sep='\n')
    #Output:
    #BOLD files of subject 2:
    #./tests/data/ds005/sub-02/func/sub-02_task-mixedgamblestask_run-01_bold.nii.gz
    #./tests/data/ds005/sub-02/func/sub-02_task-mixedgamblestask_run-02_bold.nii.gz
    #./tests/data/ds005/sub-02/func/sub-02_task-mixedgamblestask_run-03_bold.nii.gz

You can also specify lists of search items like ``subject=['02','03']`` in the above statement.
This will retrieve all the BOLD files of subjects 02 and 03.


Available search fields
-----------------------
The get() function can simultaneously search for matches in the following fields:

    1. **scope**: The BIDS subdirectory to be searched. Can be any of 'raw' | 'derivatives'
    2. **entities**: Key-value pairs in the filenames are entities defined in BIDS. Examples are 'sub' or 'run'. Use layout.get_entities() to get a list of entities available in the dataset.
    3. **suffix**: Suffixes define the imaging modality. Examples are 'bold' or 'meg'
    4. **extension**: Is the file extensions. Examples are '.nii' or 'nii.gz' for MRI and '.fif' for MEG
    5. **return_type**: Defines the what get() returns. This can be 'filename' or 'dict', where 'dict' is the default.

.. code-block:: python

    bold_files = layout.get(scope='raw',
                            return_type='filename',
                            suffix='bold',
                            extension='.nii.gz',
                            sub='03',
                            task='mixedgamblestask',
                            run=["01", "02"])
    print(*bold_files, sep='\n')
    #Output:
    #./tests/data/ds005/sub-03/func/sub-03_task-mixedgamblestask_run-01_bold.nii.gz
    #./tests/data/ds005/sub-03/func/sub-03_task-mixedgamblestask_run-02_bold.nii.gz


