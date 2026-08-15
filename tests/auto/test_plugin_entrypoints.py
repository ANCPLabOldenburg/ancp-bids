from types import SimpleNamespace
from unittest.mock import patch
import warnings

from ancpbids.plugin import (
    ValidationPlugin,
    __MIXINS__,
    __PLUGINS__,
    get_mixin_meta,
    get_hook_meta,
    load_mixins_from_entrypoints,
    load_plugins_from_entrypoints,
    mixin,
    hook,
    register_plugin,
)
from ancpbids.plugins.plugin_dsloader import DatasetPopulationPlugin
from ancpbids.mixins.mixin_dataframe import DataFrameMixin
from ancpbids.pybids_compat import BIDSLayout


def test_load_plugins_by_package_is_deprecated():
    import ancpbids.plugins as plugins_pkg
    from ancpbids.plugin import load_plugins_by_package

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        load_plugins_by_package(plugins_pkg, ranking=0, system=True)

    assert any(issubclass(w.category, DeprecationWarning) for w in caught)
    assert any("load_plugins_by_package is deprecated" in str(w.message) for w in caught)


def test_builtin_plugins_registered_via_entrypoints():
    dataset_entries = [
        e for e in __PLUGINS__ if e["plugin_class"] is DatasetPopulationPlugin
    ]
    assert len(dataset_entries) == 1
    assert dataset_entries[0]["ranking"] == 0
    assert dataset_entries[0]["props"].get("system") is True
    assert get_hook_meta(DatasetPopulationPlugin)["ranking"] == 0


def test_hook_decorator_registers_with_ranking():
    snapshot = list(__PLUGINS__)

    try:
        @hook(ranking=42, register=True)
        class RankedPlugin(ValidationPlugin):
            def execute(self, dataset, report):
                pass

        meta = get_hook_meta(RankedPlugin)
        assert meta["ranking"] == 42
        entry = next(e for e in __PLUGINS__ if e["plugin_class"] is RankedPlugin)
        assert entry["ranking"] == 42
        # idempotent
        register_plugin(RankedPlugin, ranking=99)
        assert sum(1 for e in __PLUGINS__ if e["plugin_class"] is RankedPlugin) == 1
    finally:
        __PLUGINS__[:] = snapshot


def test_load_plugins_from_entrypoints_uses_decorator_ranking():
    snapshot = list(__PLUGINS__)

    try:
        @hook(ranking=7, register=False)
        class DecoratedEntrypointPlugin(ValidationPlugin):
            def execute(self, dataset, report):
                pass

        ep = SimpleNamespace(load=lambda: DecoratedEntrypointPlugin)
        with patch("ancpbids.plugin._iter_entry_points", return_value=[ep]):
            load_plugins_from_entrypoints()

        entry = next(e for e in __PLUGINS__ if e["plugin_class"] is DecoratedEntrypointPlugin)
        assert entry["ranking"] == 7
    finally:
        __PLUGINS__[:] = snapshot


def test_register_plugin_rejects_invalid_entrypoint_target():
    try:
        register_plugin(object)
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_dataframe_mixin_applied_via_decorator():
    assert issubclass(BIDSLayout, DataFrameMixin)
    assert get_mixin_meta(DataFrameMixin)["target"] == "ancpbids.pybids_compat:BIDSLayout"
    assert any(entry["mixin_class"] is DataFrameMixin for entry in __MIXINS__)
    assert any(entry["target"] is BIDSLayout for entry in __MIXINS__
               if entry["mixin_class"] is DataFrameMixin)


def test_mixin_decorator_patches_target():
    class HostBase:
        pass

    class Host(HostBase):
        pass

    snapshot = list(__MIXINS__)
    try:
        @mixin(target=Host, ranking=5)
        class Extra:
            def ping(self):
                return "pong"

        assert issubclass(Host, Extra)
        assert Host().ping() == "pong"
        assert get_mixin_meta(Extra)["ranking"] == 5
    finally:
        __MIXINS__[:] = snapshot
        Host.__bases__ = (HostBase,)


def test_load_mixins_from_entrypoints_applies_by_ranking():
    class HostBase:
        pass

    class Host(HostBase):
        pass

    snapshot = list(__MIXINS__)
    try:
        @mixin(target=Host, ranking=20, apply=False)
        class Late:
            def tag(self):
                return "late"

        @mixin(target=Host, ranking=10, apply=False)
        class Early:
            def tag(self):
                return "early"

        eps = [
            SimpleNamespace(name="late", load=lambda: Late),
            SimpleNamespace(name="early", load=lambda: Early),
        ]
        with patch("ancpbids.plugin._iter_entry_points", return_value=eps):
            load_mixins_from_entrypoints()

        assert Host.__mro__[1] is Late
        assert Host().tag() == "late"
    finally:
        __MIXINS__[:] = snapshot
        Host.__bases__ = (HostBase,)
