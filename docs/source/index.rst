About
========
ancpBIDS is a lightweight Python library to read/query/validate/write BIDS datasets.
It can be used in workflows or analysis pipelines to handle IO specific aspects without bothering much about low level file system operations.
Its implementation is based on the BIDS schema and allows it to evolve with the BIDS specification in a generic way.
Using a plugin mechanism, contributors can extend its functionality in a controlled and clean manner.

!!! ANNOUNCEMENT !!! As of version 0.22.0 the BIDSLayout has moved over to PyBIDS where it will be developed and maintained in future.
ancpBIDS itself does not support this interface anymore but will act as a core package to PyBIDS and downstream projects needing a lightweight IO library to handle BIDS datasets.
This documentation has not yet been updated to reflect this change.

.. toctree::

   installation
   userDocCombined
   advancedQueries.rst
   validate
   api

