"""""""""""""""""""""""""""""""
Advanced Queries
"""""""""""""""""""""""""""""""

In the *link to userDocCombined* you have learnt how to access your imaging data using the
*get()* function. However, a BIDS dataset contains a lot of other valuable data and metadata
apart from our primary data (e.g. MRI or MEG timeseries). This documentation should show you how to use ancpBIDS
to query for the most common files usually contained in a BIDS dataset.

Just to recall, these are the parameters of the *get()* function:

    1. **scope**: The BIDS subdirectory to be searched. Can be any of 'raw' | 'derivatives'
    2. **entities**: Key-value pairs in the filenames are entities defined in BIDS. Examples are 'sub' or 'run'. Use layout.get_entities() to get a list of entities available in the dataset.
    3. **suffix**: Suffixes define the imaging modality or data type. Examples are 'bold' or 'meg' but also 'events' or 'participants'
    4. **extension**: Is the file extensions. Examples are '.nii' or 'nii.gz' for MRI, '.fif' for MEG and .tsv for tabular files
    5. **return_type**: Defines the what get() returns. This can be 'filename' or 'dict', where 'dict' is the default.

We can now systematically manipulate these parameters to **narrow down** or **broaden**
our queries.

For example, if we want to query for the json metadata files, which contain information about the
rawdata we can use the same query that was used for the rawdata...

.. tab:: MRI

    .. code-block:: python

        bold_files = layout.get(scope='raw',
                            return_type='filename',
                            suffix='bold',
                            extension='.nii.gz',
                            sub='03',
                            task='mixedgamblestask',
                            run=["01", "02"])
        print(*bold_files, sep='\n')


.. tab:: MEG

    .. code-block:: python

        meg_timeseries_files = layout.get(scope='raw',
                            return_type='filename',
                            suffix='meg',
                            extension='.fif',
                            sub='009',
                            task=['induction','deduction'])
        print(*meg_timeseries, sep='\n')


... but set the extension parameter to '.json' instead of '.fif' or '.nii.gz'. In general, it is important that you specify the extension since
it is BIDS convention that metadata files should have the same name as the file they describe but with the '.json' extension
See the example below:

.. tab:: MRI

    .. code-block:: python

        bold_files = layout.get(scope='raw',
                            return_type='filename',
                            suffix='bold',
                            extension='.json',
                            sub='03',
                            task='mixedgamblestask',
                            run=["01", "02"])
        print(*bold_files, sep='\n')

.. tab:: MEG

    .. code-block:: python

        meg_timeseries_files = layout.get(scope='raw',
                            return_type='filename',
                            suffix='meg',
                            extension='.json',
                            sub='009',
                            task=['induction','deduction'])
        print(*meg_timeseries, sep='\n')
        #Output:
        #./
        #/Users/*yourUserName*/.ancp-bids/datasets/ds003483/sub-009/ses-1/meg/sub-009_ses-1_task-deduction_run-1_meg.json
        #/Users/*yourUserName*/.ancp-bids/datasets/ds003483/sub-009/ses-1/meg/sub-009_ses-1_task-induction_run-1_meg.json

Note, the parameters that you can manipulate strongly depend on the dataset since every entity defined in your data
is an parameter of the *get()* function. Hence the more complex the data the more complex a query could be.

Now we can also **not** specify certain parameters in our query to **broaden** our search
within the dataset at hand. For example, if we don't specify the *sub* parameter in the query above we will
receive a list containing the paths of every .json file of every subject and not only subject 009.


.. tab:: MRI

    .. code-block:: python

        bold_json_files = layout.get(scope='raw',
                            return_type='filename',
                            suffix='bold',
                            extension='.nii.gz',
                            task='mixedgamblestask',
                            run=["01", "02"])
        print(*bold_files, sep='\n')

.. tab:: MEG

    .. code-block:: python

        meg_timeseries_json_files = layout.get(scope='raw',
                            return_type='filename',
                            suffix='meg',
                            extension='.fif',
                            task=['induction','deduction'])
        print(*meg_timeseries, sep='\n')
        #Output:






Querying metadata and other descriptive files
______________________________________________

As stated above the suffix parameter can be set to 'meg' or 'bold' for the timeseries data but luckily we can query our data for all of the
other files included in the BIDS standard by using their specific suffixes.

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
    #...
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

Moreover, the ancpbids library offers convenience functions to query for (or access?)
the dataset_description.json (and the participants.tsv which are the most common metadata
from the first level of hierarchy within the dataset, i.e.metadata that describes the whole dataset.)

.. code-block:: python

    dataset_desc = layout.get_dataset_description()




