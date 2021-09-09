
# About ancp-bids
A Python package which allows to:

- read/write
- query
- validate

BIDS datasets using the **BIDS Schema** as its foundation.

# Current state and further reading
We are in a proposal/experimental stage and design decisions may change frequently.
You can follow the progress of the proposal in the following slides:

https://docs.google.com/presentation/d/12x3cQGRD9-T1bkpK--t0e_OdgMb3UuO4jn5fGpj0a4w


# Installation

You can install the tool directly from PyPI:

`pip install ancpbids`

# Basic Usage, the PyBIDS way

    from ancpbids import BIDSLayout
    ds_path = "my-datasets/bids-001"
    layout = BIDSLayout(ds_path)
    first_run_bold_files = layout.get(run='1', suffix='bold', return_type='filename')
    ...

# Validation
`...`

# Complex Queries
`...`

# Creating new datasets
`...`
