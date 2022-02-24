.........................................
Validating a BIDS dataset
.........................................
.. contents:: Overview
   :depth: 3

Another core functionality ancpbids is to test whether a dataset adheres to `BIDS`_. This process is called validation and ancpbids provides some basic functionality for it. We are working on improving this further and making it more expressive. Her we introduce this function.

.. _BIDS: https://bids-specification.readthedocs.io/en/stable/01-introduction.html


.. tab:: MRI

    .. code::

        from ancpbids import BIDSLayout, validate_dataset
        dataset_path = './tests/data/ds005'
        layout = BIDSLayout(dataset_path)
        report = validate_dataset(layout.dataset)
        for message in report.messages:
            print(message)
        if report.has_errors():
            print("The dataset contains validation errors, cannot continue.")


