Validating a BIDS dataset
=============================

.. autosummary::
   :toctree: generated

Another core functionality ancpBIDS is to test whether a dataset adheres to `BIDS`_.
This process is called validation and ancpBIDS provides some basic functionality for it.
We are working on improving this further and making it more expressive.


.. _BIDS: https://bids-specification.readthedocs.io/en/stable/01-introduction.html


.. tab:: MRI

    .. code-block:: python

        from ancpbids import fetch_dataset, BIDSLayout, validate_dataset
        # fetch fMRI dataset
        dataset_path = fetch_dataset('ds005')
        layout = BIDSLayout(dataset_path)
        report = validate_dataset(layout.dataset)
        for message in report.messages:
            print(message)
        if report.has_errors():
            print("The dataset contains validation errors, cannot continue.")


.. tab:: MEG

    .. code-block:: python

        from ancpbids import fetch_dataset, BIDSLayout, validate_dataset
        # fetch MEG dataset
        dataset_path = fetch_dataset('ds003483')
        layout = BIDSLayout(dataset_path)
        report = validate_dataset(layout.dataset)
        for message in report.messages:
            print(message)
        if report.has_errors():
            print("The dataset contains validation errors, cannot continue.")


