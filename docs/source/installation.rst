Installation
============

.. autosummary::
   :toctree: generated


Install using `pip`
-------------------
ancpBIDS is available via `PyPi.org <https://pypi.org/project/ancpbids/>`_

.. code-block::
   :caption: Initial installation

       pip install ancpbids

.. code-block::
   :caption: Upgrade existing

       pip install --upgrade ancpbids

Optional extras:

.. code-block::

       pip install "ancpbids[pandas]"
       pip install "ancpbids[torch]"

Install using `conda`
---------------------

Not yet available.

Development
-----------
The project is managed with `uv <https://docs.astral.sh/uv/>`_. From a clone:

.. code-block::

       uv sync
       uv run pytest tests/auto
