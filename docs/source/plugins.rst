Plugins and mixins
==================

ancpBIDS's plugin mechanism has two contribution kinds: **hooks** (lifecycle
plugins with an ``execute`` method, registered via ``@hook``) and **mixins**
(extra methods on host classes such as ``BIDSLayout``, via ``@mixin``).

Plugin types
------------

* ``SchemaPlugin`` — modify or extend a loaded BIDS schema
* ``DatasetPlugin`` — operate on the in-memory dataset graph after load
* ``FileHandlerPlugin`` — register custom file readers/writers
* ``WritingPlugin`` — add files or folders when writing a dataset
* ``ValidationPlugin`` — add custom validation rules

Built-in plugins are declared in ancpBIDS' own ``pyproject.toml`` under
``ancpbids.plugins`` (with ``@hook(ranking=0, system=True)``) and loaded the
same way as third-party plugins. Additional plugins use the same entry-point
group or ``register_plugin``.

Registering an external plugin
------------------------------

Use this path when you publish a **separate** installable package that depends
on ``ancpbids``. You declare contributions in **your** package's
``pyproject.toml``; you do not change ancpBIDS itself.

1. Subclass a plugin base class and decorate it with ``@hook`` (ranking is
   metadata on the class):

   .. code-block:: python

      # lab_bids_extensions/validation.py
      from ancpbids.plugin import ValidationPlugin, hook

      @hook(ranking=1000)
      class SiteRulesPlugin(ValidationPlugin):
          def execute(self, dataset, report: ValidationPlugin.ValidationReport):
              # add errors/warnings via report.error(...) / report.warn(...)
              pass

2. Declare an entry point under the ``ancpbids.plugins`` group in **your**
   ``pyproject.toml``:

   .. code-block:: toml

      [project.entry-points."ancpbids.plugins"]
      site_rules = "lab_bids_extensions.validation:SiteRulesPlugin"

   How to read that line:

   * ``site_rules`` — a contribution id **you** choose (for humans and tools)
   * ``lab_bids_extensions.validation`` — **your** Python module
   * ``SiteRulesPlugin`` — **your** class in that module

   The quotes around ``ancpbids.plugins`` are required in TOML because the
   group name contains a dot.

3. Install your package into the same environment as ancpBIDS.

4. Importing ``ancpbids`` loads entry-point plugins via
   ``load_plugins_from_entrypoints()``. Ranking from ``@hook`` is respected.

Registering an external mixin
-----------------------------

Mixins add methods to an existing host class (for example ``BIDSLayout``).
Declare intent with ``@mixin``; ancpBIDS patches the target from metadata.

1. Define the mixin in your package:

   .. code-block:: python

      from ancpbids import BIDSLayout
      from ancpbids.plugin import mixin

      @mixin(target=BIDSLayout, ranking=1000)
      class MyExportMixin:
          def to_custom(self):
              ...

   ``target`` may also be a string (``"ancpbids.pybids_compat:BIDSLayout"``)
   when a live class reference would create import cycles (built-in mixins use this).

2. Advertise it under ``ancpbids.mixins``:

   .. code-block:: toml

      [project.entry-points."ancpbids.mixins"]
      my_export = "lab_bids_extensions.exports:MyExportMixin"

3. After install, ``load_mixins_from_entrypoints()`` (called when ``ancpbids``
   is imported) applies mixins by ascending ``ranking``.

The target class must not inherit *directly* from ``object`` (Python cannot
reassign ``__bases__`` in that case). ``BIDSLayout`` uses an intermediate
``_BIDSLayoutBase`` for this reason.

Built-in example: ``DataFrameMixin`` lives in ``ancpbids.mixins.mixin_dataframe``,
is declared as ``@mixin(target=..., ranking=0)``, and is listed under the
``ancpbids.mixins`` entry-point group in ancpBIDS' ``pyproject.toml``
(same mechanism external packages use).

Alternative registration (same process)
---------------------------------------

.. code-block:: python

   from ancpbids.plugin import register_plugin, register_mixin

   register_plugin(SiteRulesPlugin, ranking=1000)
   register_mixin(MyExportMixin)

Ranking
-------

Lower ``ranking`` runs / applies earlier. Built-ins use ``0``. External
contributions typically use ``1000`` (the decorator default).

See also
--------

* API: :mod:`ancpbids.plugin`
* ``PLUGIN_ENTRY_POINT_GROUP`` (``"ancpbids.plugins"``)
* ``MIXIN_ENTRY_POINT_GROUP`` (``"ancpbids.mixins"``)
