"""""""""""""""""""""""""""""""""""
ANCP-BIDS User Documentation - MEG
"""""""""""""""""""""""""""""""""""
.. contents:: Overview
   :depth: 3

Load an existing BIDS dataset
-----------------------------
Use the **load_dataset** function to load the data.
As an input parameter provide the load_dataset function with a path
to your root directory. The directory must be in BIDS compliant structure.

.. code-block:: python
    from ancpbids import load_dataset
    dataset_path = './ancp-bids/tests/data/ds003483'
    dataset = load_dataset(dataset_path)
    len(dataset.subjects)
    #Output:
    #21
Querying information about the dataset
--------------------------------------
First we read information about a BIDS dataset into a layout-object using
BIDSLayout. BIDSLayout takes as input the absolute or relative path to a
BIDS-dataset and returns a layout in which most of the information about
the dataset is held. Note that in order optimize speed BIDSLayout does not
perform a deep search within data files. It only parses the fields and
directories necessary to gather the information defined in the
Brain Imaging Data Structure (BIDS).

.. code-block:: python
    from ancpbids import BIDSLayout
    layout = BIDSLayout(dataset_path)
Basic queries
_____________
Now we can use the get functions to **retrieve information** about the dataset or
**access specific files**  in our directory. These simple queries should support most
of the `entities defined in BIDS`_. The queries are constructed as::

    layout.get_NameOfTheEntity()

The query will return '[]' if the entity does not exist in the dataset or if some wrong query
string was written after **'get\_'**. Note, that the entity that you are querying for can be written
in singular and plural, i.e. `layout.get_subjects()` and `layout.get_subject()` will yield
a list of all subject identifiers present in your dataset.

.. _entities defined in BIDS: https://bids-specification.readthedocs.io/en/stable/99-appendices/09-entities.html

.. code-block:: python
    subject_ids = layout.get_subjects()
    print(subject_ids)
    subject_ids = layout.get_subject()
    print(subject_ids)
    #Output:
    #['009', '012', '013', '014', '015', '016', '017', '018', '019', '020', '021', '022', '023', '024', '025', '026', '027', '028', '029', '030', '031']
    #['009', '012', '013', '014', '015', '016', '017', '018', '019', '020', '021', '022', '023', '024', '025', '026', '027', '028', '029', '030', '031']
Now lets see if we have different tasks defined in our dataset...

.. code-block:: python
    tasks = layout.get_tasks()
    print(tasks)
    #Output:
    #['deduction','induction']
To get an idea of the entities you can query for in your dataset you can use the
`layout.get_entities()` function to receive a dictionary with all entities defined in the
dataset and its respective values.

.. code-block:: python
    entities = layout.get_entities()
    print(entities)
    #Output:
    #OrderedDict([('sub', {'027', '026', '012', '019', '029', '014', '031', '021', '022', '016', '009', '017', '023', '030', '015', '028', '018', '013', '020', '025', '024'}),
    # ('ses', {'1'}), ('task', {'deduction', 'induction'}), ('run', {'1'}), ('desc', {'epochs'})])
In our case the dictionary consists of 5 entities ('sub', 'ses', 'task', 'run' and 'desc') with their respective values.

.. _Retrieving-matching-filenames:
Retrieving matching filenames
_____________________________
We can also use get function from the BIDSLayout to retrieve matching filenames,
i.e. if we want to filter our data for specific files like all MEG timeseries of one subject.
The **get()** function can simultaneously search your dataset for filenames matching the values specified by the following parameters:
    1. `scope`: The BIDS subdirectory to be searched. Can be any of 'raw' | 'derivatives'
    2. `entities`: Key-value pairs in the filenames as defined in BIDS. Examples are 'sub' or 'run'. Use `layout.get_entities()` to get a list of all entities available in your dataset.
    3. `suffix`: Suffixes define the data type. Examples are 'bold' or 'meg' for imaging data.
    4. `extension`: Extensions define the data format. Examples are '.nii' or 'nii.gz' for MRI and '.fif' for MEG
    5. `return_type`: Defines the what get() returns. This can be 'filename' or 'dict', where 'dict' is the default.

.. code-block:: python
    data_sub_009 = layout.get(suffix='meg',subject='009',extension='.fif',return_type='filename')
    print(data_sub_009)
    #Output
    #['./ancp-bids/tests/data/ds003483/sub-009/ses-1/meg/sub-009_ses-1_task-deduction_run-1_meg.fif',
    # './ancp-bids/tests/data/ds003483/sub-009/ses-1/meg/sub-009_ses-1_task-induction_run-1_meg.fif']
As you can see the query for all MEG timeseries files of **sub-009** returns two files which is due to the case that we have two different tasks defined
in our test dataset and every participant has a MEG timeseries for each of these tasks.
One can now arbitrarily combine the parameters of the **get()** function to narrow down or broaden the search
within the dataset at hand.

For example: We can add a value for the task parameter in the call above to **narrow down** our search
to the MEG timeseries data of **sub-009** for the **deduction task**.

.. code-block:: python
    data_sub_009_deduction = layout.get(suffix='meg',subject='009',extension='.fif',return_type='filename',task='deduction')
    print(data_sub_009_deduction)
    #Output:
    #['./ancp-bids/tests/data/ds003483/sub-009/ses-1/meg/sub-009_ses-1_task-deduction_run-1_meg.fif']
By not specifying certain parameters we can **broaden** our filter. If we want to compare the data of the
different task (induction and deduction) over all subjects we can drop the subject parameter from the query
above and will receive a list of paths to the MEG timeseries of all subjects for the deduction or induction
task, respectively.

.. code-block:: python
    data_all_sub_deduction = layout.get(suffix='meg',extension='.fif',return_type='filename',task='deduction')
    print(data_sub_009)
    #Output:
    #['./ancp-bids/tests/data/ds003483/sub-009/ses-1/meg/sub-009_ses-1_task-deduction_run-1_meg.fif',
    # './ancp-bids/tests/data/ds003483/sub-012/ses-1/meg/sub-012_ses-1_task-deduction_run-1_meg.fif',
    # './ancp-bids/tests/data/ds003483/sub-013/ses-1/meg/sub-013_ses-1_task-deduction_run-1_meg.fif',
    # './ancp-bids/tests/data/ds003483/sub-014/ses-1/meg/sub-014_ses-1_task-deduction_run-1_meg.fif',
    # './ancp-bids/tests/data/ds003483/sub-015/ses-1/meg/sub-015_ses-1_task-deduction_run-1_meg.fif',
    # './ancp-bids/tests/data/ds003483/sub-016/ses-1/meg/sub-016_ses-1_task-deduction_run-1_meg.fif',
    # './ancp-bids/tests/data/ds003483/sub-017/ses-1/meg/sub-017_ses-1_task-deduction_run-1_meg.fif',
    # './ancp-bids/tests/data/ds003483/sub-018/ses-1/meg/sub-018_ses-1_task-deduction_run-1_meg.fif',
    # './ancp-bids/tests/data/ds003483/sub-019/ses-1/meg/sub-019_ses-1_task-deduction_run-1_meg.fif',
    # './ancp-bids/tests/data/ds003483/sub-020/ses-1/meg/sub-020_ses-1_task-deduction_run-1_meg.fif',
    # './ancp-bids/tests/data/ds003483/sub-021/ses-1/meg/sub-021_ses-1_task-deduction_run-1_meg.fif',
    # './ancp-bids/tests/data/ds003483/sub-022/ses-1/meg/sub-022_ses-1_task-deduction_run-1_meg.fif',
    # './ancp-bids/tests/data/ds003483/sub-023/ses-1/meg/sub-023_ses-1_task-deduction_run-1_meg.fif',
    # './ancp-bids/tests/data/ds003483/sub-024/ses-1/meg/sub-024_ses-1_task-deduction_run-1_meg.fif',
    # './ancp-bids/tests/data/ds003483/sub-025/ses-1/meg/sub-025_ses-1_task-deduction_run-1_meg.fif',
    # './ancp-bids/tests/data/ds003483/sub-026/ses-1/meg/sub-026_ses-1_task-deduction_run-1_meg.fif',
    # './ancp-bids/tests/data/ds003483/sub-027/ses-1/meg/sub-027_ses-1_task-deduction_run-1_meg.fif',
    # './ancp-bids/tests/data/ds003483/sub-028/ses-1/meg/sub-028_ses-1_task-deduction_run-1_meg.fif',
    # './ancp-bids/tests/data/ds003483/sub-029/ses-1/meg/sub-029_ses-1_task-deduction_run-1_meg.fif',
    # './ancp-bids/tests/data/ds003483/sub-030/ses-1/meg/sub-030_ses-1_task-deduction_run-1_meg.fif',
    # './ancp-bids/tests/data/ds003483/sub-031/ses-1/meg/sub-031_ses-1_task-deduction_run-1_meg.fif']
Note, one can also pass a list of specific subject-id's to the **get()** function as value of the subject parameter.
This will search your data for matching filenames for all of the elements of the list. Lets assume that we want to
search our dataset for all MEG timeseries data of **sub-009**, **sub-013** and **sub-029** during the 'deduction' task

.. code-block:: python
    data_sub_009_013_029 = layout.get(suffix='meg',subject=['009','013','029'],extension='.fif',return_type='filename',task='deduction')
    print(data_sub_009_013_029)
    #Output:
    #['./ancp-bids/tests/data/ds003483/sub-009/ses-1/meg/sub-009_ses-1_task-deduction_run-1_meg.fif',
    #'./ancp-bids/tests/data/ds003483/sub-013/ses-1/meg/sub-013_ses-1_task-deduction_run-1_meg.fif',
    #'./ancp-bids/tests/data/ds003483/sub-029/ses-1/meg/sub-029_ses-1_task-deduction_run-1_meg.fif']
Be aware that you have to define the extension (set it to '.fif') in order to exclusively filter for
timeseries data and not include the json files of the acquisition and other files with the 'meg' suffix. Note,
if the data was not acquired on an ELEKTA/NEUROMAG/MEGIN MEG scanner (as is the case
for the ancp-testdata) the extension could be vary ,e.g. extension = '.ds' for CTF MEG systems. See here for a
complete list of `MEG data formats and their respective extensions`_ included in the BIDS standard.

The query below demonstrates what happens if you don't specify the extension parameter.

.. _MEG data formats and their respective extensions: https://bids-specification.readthedocs.io/en/stable/99-appendices/06-meg-file-formats.html

.. code-block:: python
    data_sub_009_meg_suffix = layout.get(suffix='meg',subject='009',return_type='filename')
    print(data_sub_009)
    #Output:
    #['./ancp-bids/tests/data/ds003483/sub-009/ses-1/meg/sub-009_ses-1_task-deduction_run-1_meg.json',
    #'./ancp-bids/tests/data/ds003483/sub-009/ses-1/meg/sub-009_ses-1_task-induction_run-1_meg.json',
    #'./ancp-bids/tests/data/ds003483/sub-009/ses-1/meg/sub-009_ses-1_task-deduction_run-1_meg.fif',
    #'./ancp-bids/tests/data/ds003483/sub-009/ses-1/meg/sub-009_ses-1_task-induction_run-1_meg.fif',
    #'./ancp-bids/tests/data/ds003483/derivatives/pipeline_preprocessing/sub-009/ses-1/meg/sub-009_ses-1_task-deduction_run-1_desc-epochs_meg.dat',
    #'./ancp-bids/tests/data/ds003483/derivatives/pipeline_preprocessing/sub-009/ses-1/meg/sub-009_ses-1_task-deduction_run-1_desc-epochs_meg.mat',
    #'./ancp-bids/tests/data/ds003483/derivatives/pipeline_preprocessing/sub-009/ses-1/meg/sub-009_ses-1_task-induction_run-1_desc-epochs_meg.dat',
    #'./ancp-bids/tests/data/ds003483/derivatives/pipeline_preprocessing/sub-009/ses-1/meg/sub-009_ses-1_task-induction_run-1_desc-epochs_meg.mat',
    #'./ancp-bids/tests/data/ds003483/derivatives/pipeline_preprocessing/sub-009/ses-1/meg/sub-009_ses-1_task-deduction_run-1_desc-epochs_meg.json',
    #'./ancp-bids/tests/data/ds003483/derivatives/pipeline_preprocessing/sub-009/ses-1/meg/sub-009_ses-1_task-induction_run-1_desc-epochs_meg.json']
For the testdata there are some files in the derivatives with the 'meg' suffix besides the metadata of the
acquisition defined in the json file.

Importantly, you could also use the extension parameter to explicitly search for available metadata or get the path
of specific metadata files: ::

    metadata_sub_009_meg = layout.get(suffix='meg',subject='009','extension'='.json',return_type='filename')
    print(data_sub_009)
    #Output:
    #

Querying metadata and other descriptive files
______________________________________________

As stated above the suffix parameter can be set to 'meg' for the timeseries data but luckily we can query our data for all of the files included in the BIDS standard by using their specific suffixes.

In the domain of MEG these suffixes are:
    1. `events`: search for event files
    2. `ccordsystem`: search for the file specifying the coordinate system
    3. `channels`: search for the file which specifies channel names and types
    4. `scans`: search for the files documenting the different scan sequences that were run

Here are some examples of how to query for these BIDS specific files.

Retrieve a list of all event files available in your data:

.. code-block:: python
    all_events = layout.get(suffix='events', return_type='filename')
    print(all_events)
    #Output
    #['./ancp-bids/tests/data/ds003483/sub-009/ses-1/meg/sub-009_ses-1_task-deduction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-009/ses-1/meg/sub-009_ses-1_task-induction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-012/ses-1/meg/sub-012_ses-1_task-deduction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-012/ses-1/meg/sub-012_ses-1_task-induction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-013/ses-1/meg/sub-013_ses-1_task-deduction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-013/ses-1/meg/sub-013_ses-1_task-induction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-014/ses-1/meg/sub-014_ses-1_task-deduction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-014/ses-1/meg/sub-014_ses-1_task-induction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-015/ses-1/meg/sub-015_ses-1_task-deduction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-015/ses-1/meg/sub-015_ses-1_task-induction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-016/ses-1/meg/sub-016_ses-1_task-deduction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-016/ses-1/meg/sub-016_ses-1_task-induction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-017/ses-1/meg/sub-017_ses-1_task-deduction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-017/ses-1/meg/sub-017_ses-1_task-induction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-018/ses-1/meg/sub-018_ses-1_task-deduction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-018/ses-1/meg/sub-018_ses-1_task-induction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-019/ses-1/meg/sub-019_ses-1_task-deduction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-019/ses-1/meg/sub-019_ses-1_task-induction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-020/ses-1/meg/sub-020_ses-1_task-deduction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-020/ses-1/meg/sub-020_ses-1_task-induction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-021/ses-1/meg/sub-021_ses-1_task-deduction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-021/ses-1/meg/sub-021_ses-1_task-induction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-022/ses-1/meg/sub-022_ses-1_task-deduction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-022/ses-1/meg/sub-022_ses-1_task-induction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-023/ses-1/meg/sub-023_ses-1_task-deduction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-023/ses-1/meg/sub-023_ses-1_task-induction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-024/ses-1/meg/sub-024_ses-1_task-deduction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-024/ses-1/meg/sub-024_ses-1_task-induction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-025/ses-1/meg/sub-025_ses-1_task-deduction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-025/ses-1/meg/sub-025_ses-1_task-induction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-026/ses-1/meg/sub-026_ses-1_task-deduction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-026/ses-1/meg/sub-026_ses-1_task-induction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-027/ses-1/meg/sub-027_ses-1_task-deduction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-027/ses-1/meg/sub-027_ses-1_task-induction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-028/ses-1/meg/sub-028_ses-1_task-deduction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-028/ses-1/meg/sub-028_ses-1_task-induction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-029/ses-1/meg/sub-029_ses-1_task-deduction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-030/ses-1/meg/sub-030_ses-1_task-deduction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-030/ses-1/meg/sub-030_ses-1_task-induction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-031/ses-1/meg/sub-031_ses-1_task-deduction_run-1_events.tsv',
    #'./ancp-bids/tests/data/ds003483/sub-031/ses-1/meg/sub-031_ses-1_task-induction_run-1_events.tsv']
Again we can use any combination of the parameters of the **get()** function to narrow down the search according
to our needs.

Following the example from the section above we could limit our search to all event files of a specific subject,
task or other entity defined in our data. See, *reference to section* to once again check how to find all available entities in your data.

Let's search our data for the event file of **sub-009** for the **deduction** task:

.. code-block:: python
    events_sub009_deduc = layout.get(suffix='events', subject='009', task='deduction', return_type='filename')
    print(events_sub009_deduc)
    #Output
    #['./ancp-bids/tests/data/ds003483/sub-009/ses-1/meg/sub-009_ses-1_task-deduction_run-1_events.tsv']
Note, if your BIDS dataset contains metadata for your event files you can specify if you want to search
for the metadata or the actual event files by setting the extension parameter to '.json' or '.tsv', respectively.

We can search our data for the other files described above by setting the extension value to one
of the values defined above.

Access file contents
--------------------
Now we know how to query our data to gather information about the dataset and to locate specific files which we
will need for our analysis. In order to work with these files in our workflows we have to **access** them.

For accessing the contents of our files we can use the **load_contents()** function. Keep in mind that in order to
successfully load the contents of the file the **return_type** parameter of the **get()** function should not be
specified sticking to its default value 'dict'.

We can then load the contents of the first element of our dictionary to access the file, see the example below:

.. code-block:: python
    events = layout.get(suffix='events',subject='009',task='deduction')
    df_events = events[0].load_contents()
This way you will be able to load the contents of the metadata and descriptive tabular files.
@Erdal: für imaging data brauchen wir aber noch bibleotheken die die daten interpretieren können richtig?


