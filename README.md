[![Documentation Status](https://readthedocs.org/projects/ancpbids/badge/?version=latest)](http://ancpbids.readthedocs.io/en/latest/?badge=latest)
[![Latest Version](https://img.shields.io/pypi/v/ancpbids.svg)](https://pypi.python.org/pypi/ancpbids/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ancpbids.svg)](https://pypi.python.org/pypi/ancpbids/)
[![Test Status](https://github.com/ANCPLabOldenburg/ancp-bids/actions/workflows/testing.yml/badge.svg)](https://github.com/ANCPLabOldenburg/ancp-bids/actions/workflows/testing.yml)
[![Codecov](https://codecov.io/gh/ANCPLabOldenburg/ancp-bids/branch/main/graph/badge.svg)](https://codecov.io/gh/ANCPLabOldenburg/ancp-bids)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
# About
ancpBIDS is a lightweight Python library to read/query/validate/write BIDS datasets.
It can be used in workflows or analysis pipelines to handle IO specific aspects without bothering much about low level file system operations.
Its implementation is based on the BIDS schema and allows it to evolve with the BIDS specification in a generic way.
Using a plugin mechanism, contributors can extend its functionality in a controlled and clean manner.

!!! ANNOUNCEMENT !!! As of version 0.22.0 the BIDSLayout has moved over to [PyBIDS](https://github.com/bids-standard/pybids) where it will be developed and maintained in future.
ancpBIDS itself does not support this interface anymore but will act as a core package to PyBIDS and downstream projects needing a lightweight IO library to handle BIDS datasets.
This documentation has not yet been updated to reflect this change.

Read more on [readthedocs.io](https://ancpbids.readthedocs.io)