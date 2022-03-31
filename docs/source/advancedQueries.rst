"""""""""""""""""""""""""""""""
Advanced Queries using ancpBIDS
"""""""""""""""""""""""""""""""

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