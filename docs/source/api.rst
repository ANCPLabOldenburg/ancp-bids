API
===

.. autosummary::
   :toctree: generated


.. autoclass:: ancpbids.BIDSLayout
    :members:

    .. attribute:: get_<entity>()

        It is possible to get a unique set of values for each of the available BIDS entities.

        Examples:
    .. code-block::

        all_task_labels = layout.get_tasks()
        all_subject_labels = layout.get_subjects(task='lang')
        all_bold_session_labels = layout.get_sessions(suffix='bold')

    See :class:`EntityEnum <ancpbids.model_v1_7_0.EntityEnum>` for supported entities.

.. automodule:: ancpbids
    :members:


.. automodule:: ancpbids.utils
    :members:
