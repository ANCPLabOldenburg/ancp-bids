""""""""""""""""""""""""""""
ANCP-BIDS User Documentation
""""""""""""""""""""""""""""
.........................................
Querying information about a BIDS dataset
.........................................
.. contents:: Overview
   :depth: 3

One core functionality of the ancpbids tools is to query information about locally stored BIDS compatible data sets. Note that ancpbids will only include files in to the query that conform with the BIDS. An online version can be found `here`_.

.. _here: https://bids-specification.readthedocs.io/en/stable/

@Erdal: Is this a correct statement?

Load an existing BIDS dataset
-----------------------------
First we read information about a BIDS dataset in to a layout-object using BIDSLayout. BIDSLayout takes as input the absolute or relative path to a BIDS-dataset and returns a layout in which most of the information about the dataset is held.

.. code-block:: python
    from ancpbids import BIDSLayout
    dataset_path = './tests/data/ds005'
    layout = BIDSLayout(dataset_path)
Note that in order optimize speed BIDSLayout does not perform a deep search within data files. I  only parses the fiels and directories necessery to gather the information defined in the Brain Imaging Data Structure (BIDS).

Perform some basic queries
--------------------------
We can now use several methods to query information about the dataset. We can ask which subjects are in the dataset:

.. code:: python
    subs=layout.get_subjects()
    print(subs)
    #Output:
    #['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16']
This will provide a list of all subject names in the dataset.

Next lest us see how many runs there are.
@Erdal: what happens if participants have different numbers of runs?

.. code:: python
    runs=layout.get_runs()
    print(runs)
    #Output:
    #['1', '2', '3']
Now the task

.. code:: python
    task=layout.get_task()
    print(task)
    #Output:
    #['mixedgamblestask']
These simple queries should support most of the `entities defined in BIDS`_. The queries are constructed as **layout.get_NameOfTheEntity()**. The query will return '[]' if the entity does not exist in the dataset or if some wrong query string was written after 'get\_'.

.. _entities defined in BIDS: https://bids-specification.readthedocs.io/en/stable/99-appendices/09-entities.html


Query available entitities and metadata
---------------------------------------
The command layout.get_entities() returns a dictionary with all entities defined in the dataset and their values.

.. code:: python
    avail_entitities=layout.get_entities()
    print("Entities: ", list(avail_entitities.keys()))
    print("Value of task: ", avail_entitities['task']
    #Output:
    #Entities:  ['task', 'sub', 'run', 'ds', 'type']
    #Value of task:  {'mixedgamblestask'}

**@Erdal:** seems like layout.get_entities returns entitities that are not defined in https://bids-specification.readthedocs.io/en/stable/99-appendices/09-entities.html .Examples with ds005 are 'ds' and 'type'. Are they rather metadata?

Metadata from json files can be queried using layout.get_metadata(entity='abc',suffix='xyz'). It will return a dictionary with keys and values

.. code:: python
   metadata = layout.get_metadata(task='mixedgamblestask', suffix='bold')
    print("metadata: ", list(metadata.keys()))
    print("Value of RepetitionTime: ", metadata['RepetitionTime'])
    #Output:
    #metadata:  ['RepetitionTime', 'TaskName', 'SliceTiming']
    #Value of RepetitionTime:  2.0

**@Erdal:** The call layout.get_metadata() chrashes. In the tests I can see an example that works but ḿ no sure how to generalize to other calls. I guess it has something to do with the query module? Need help here.

Retrieving matching filenames
-----------------------------
The layout.get() function allows for more complex queries and can return a list of files matching the query.

.. code:: python
    file_paths = layout.get(suffix='bold', subject='02', return_type='filename')
    print("BOLD files of subject 2:", *file_paths, sep='\n')
    #Output:
    #BOLD files of subject 2:
    #./tests/data/ds005/sub-02/func/sub-02_task-mixedgamblestask_run-01_bold.nii.gz
    #./tests/data/ds005/sub-02/func/sub-02_task-mixedgamblestask_run-02_bold.nii.gz
    #./tests/data/ds005/sub-02/func/sub-02_task-mixedgamblestask_run-03_bold.nii.gz

You can also specify lists of search items like ``subject=['02','03']`` in the above statement. This will retrieve all the BOLD files of subjects 02 and 03.

Available search fields
-----------------------
The get() function can simulanteously search for matches in the following fields:

    1. **scope**: The BIDS subdirectory to be searched. Can be any of 'raw' | 'derivatives'
    2. **entities**: Key-value pairs in the filenames are entities defined in BIDS. Examples are 'sub' or 'run'. Use layout.get_entities() to get a list of entities available in the dataset.
    3. **suffix**: Suffixes define the imaging modality. Examples are 'bold' or 'meg'
    4. **extension**: Is the file extensions. Examples are '.nii' or 'nii.gz' for MRI and '.fif' for MEG
    5. **return_type**: Defines the what get() returns. This can be 'filename' or 'dict', where 'dict' is the default.

.. code:: python
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

@Erdal: I do not really understand what the function reports from the derivatives folder.

