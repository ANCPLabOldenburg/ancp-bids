import importlib
import inspect
import pkgutil
import warnings
from importlib.metadata import entry_points
from typing import List, Optional, Union

# global plugins registry (list of plugin metadata/settings)
__PLUGINS__ = []
# applied mixin contributions (for idempotency / introspection)
__MIXINS__ = []

# Packaging entry-point group for third-party plugin contributions.
# If you ship a separate installable package, declare each plugin in *your*
# pyproject.toml (name on the left is an id you choose; right side is your class):
#   [project.entry-points."ancpbids.plugins"]
#   site_rules = "lab_bids_extensions.validation:SiteRulesPlugin"
PLUGIN_ENTRY_POINT_GROUP = "ancpbids.plugins"

# Packaging entry-point group for mixin contributions (classes decorated with @mixin).
#   [project.entry-points."ancpbids.mixins"]
#   to_df = "lab_bids_extensions.pandas_export:DataFrameMixin"
MIXIN_ENTRY_POINT_GROUP = "ancpbids.mixins"

_PLUGIN_META = "__ancpbids_plugin__"
_MIXIN_META = "__ancpbids_mixin__"

TargetRef = Union[type, str]


class Plugin:
    """Base class of all plugins.
    """

    def __init__(self, **props):
        self.props = props


class SchemaPlugin(Plugin):
    """A schema plugin may extend/modify a BIDS schema representation module.
    For example, to monkey-patch generated classes.
    """

    def execute(self, schema):
        raise NotImplementedError()


class DatasetPlugin(Plugin):
    """A dataset plugin may enhance an in-memory graph of a dataset.
    """

    def execute(self, dataset):
        raise NotImplementedError()


class FileHandlerPlugin(Plugin):
    """A file handler plugin may register a reader or writer function to allow handling unknown file extensions.
    """

    def execute(self, file_readers_registry, file_writers_registry):
        raise NotImplementedError()


class WritingPlugin(Plugin):
    """A writing plugin may write additional files/folders when a dataset is stored back to file system.
    This may be most interesting to write derivatives to a dataset."""

    def execute(self, dataset, target_dir: str, context_folder=None,
                src_dir: str = None):
        raise NotImplementedError()


class ValidationPlugin(Plugin):
    """A validation plugin may extend the rules to validate a dataset against."""

    class ValidationReport:
        """Contains validation messages (errors/warnings) after a dataset has been validated."""

        def __init__(self):
            self.messages = []

        def error(self, message, offender=None, code=None):
            """Adds a new error message to the report.

            Parameters
            ----------
            message:
                the error message to add to the report
            offender:
                the graph node that triggered the message
            code:
                optional schema issue code (for example ``NOT_INCLUDED``)

            """
            self.messages.append(_message('error', message, offender, code))

        def warn(self, message, offender=None, code=None):
            """Adds a new warning message to the report.

            Parameters
            ----------
            message:
                the warning message to add to the report
            offender:
                the graph node that triggered the message
            code:
                optional schema issue code

            """
            self.messages.append(_message('warn', message, offender, code))

        def has_errors(self):
            """
            Returns
            -------
            bool
                whether this report contains errors
            """
            return len(self.get_errors()) > 0

        def get_errors(self):
            return list(filter(lambda m: m['severity'] == 'error', self.messages))

    def execute(self, dataset, report: ValidationReport):
        raise NotImplementedError()


def _message(severity, message, offender, code):
    entry = {
        'severity': severity,
        'offender': offender,
        'message': message,
    }
    if code:
        entry['code'] = code
    return entry


def is_valid_plugin(plugin_class):
    """
    Parameters
    ----------
    plugin_class:
        the class to check if known to be a valid plugin class

    Returns
    -------
    bool
        whether the class is considered a valid plugin class
    """
    plugin_types = (SchemaPlugin, DatasetPlugin, WritingPlugin, ValidationPlugin, FileHandlerPlugin)
    return issubclass(plugin_class, plugin_types) and plugin_class not in plugin_types


def plugin(ranking: int = 1000, *, register: bool = True, **props):
    """Class decorator that attaches plugin metadata and optionally registers the class.

    Parameters
    ----------
    ranking:
        lower values run earlier (system plugins use ``0``)
    register:
        if True (default), call ``register_plugin`` immediately
    props:
        extra static properties stored on the registry entry

    Example
    -------
    .. code-block:: python

        @plugin(ranking=1000)
        class SiteRulesPlugin(ValidationPlugin):
            def execute(self, dataset, report):
                ...
    """

    def decorator(cls):
        if not is_valid_plugin(cls):
            raise ValueError('Invalid plugin class: %s' % cls.__name__)
        setattr(cls, _PLUGIN_META, {'ranking': ranking, 'props': props})
        if register:
            register_plugin(cls, ranking=ranking, **props)
        return cls

    return decorator


def mixin(*, target: TargetRef, ranking: int = 1000, apply: bool = True, **props):
    """Class decorator that marks a mixin and optionally patches its target class.

    Parameters
    ----------
    target:
        the class to extend, or a resolvable string (``"module.path:ClassName"``
        or ``"module.path.ClassName"``)
    ranking:
        lower values are applied earlier when several mixins are batch-loaded
    apply:
        if True (default), patch the target immediately via ``register_mixin``
    props:
        extra metadata retained on the mixin class

    Example
    -------
    .. code-block:: python

        @mixin(target=BIDSLayout)
        class DataFrameMixin:
            def to_df(self, ...):
                ...
    """

    def decorator(cls):
        setattr(cls, _MIXIN_META, {
            'target': target,
            'ranking': ranking,
            'props': props,
        })
        if apply:
            register_mixin(cls)
        return cls

    return decorator


def get_plugin_meta(plugin_class) -> Optional[dict]:
    return getattr(plugin_class, _PLUGIN_META, None)


def get_mixin_meta(mixin_class) -> Optional[dict]:
    return getattr(mixin_class, _MIXIN_META, None)


def _resolve_target(target: TargetRef) -> type:
    if isinstance(target, type):
        return target
    if not isinstance(target, str):
        raise TypeError('mixin target must be a class or string, got %r' % (target,))
    if ':' in target:
        module_name, _, attr = target.partition(':')
    else:
        module_name, _, attr = target.rpartition('.')
        if not module_name or not attr:
            raise ValueError('Invalid mixin target %r; use "module:Class" or "module.Class"' % target)
    module = importlib.import_module(module_name)
    resolved = getattr(module, attr)
    if not isinstance(resolved, type):
        raise TypeError('mixin target %r did not resolve to a class' % target)
    return resolved


def _prepend_base(target: type, mixin_cls: type) -> None:
    if mixin_cls in target.__mro__:
        return
    bases = tuple(target.__bases__)
    if bases == (object,):
        raise TypeError(
            'Cannot patch %s with mixins because it inherits directly from object; '
            'give it a non-object base class first' % target.__name__)
    target.__bases__ = (mixin_cls,) + bases


def register_mixin(mixin_class, ranking: int = None, **props):
    """Apply a ``@mixin``-decorated class to its target.

    Parameters
    ----------
    mixin_class:
        class decorated with ``@mixin``
    ranking:
        optional override of the decorator ranking (stored for introspection)
    props:
        optional extra props merged into stored metadata
    """
    meta = get_mixin_meta(mixin_class)
    if meta is None:
        raise ValueError('%s is not decorated with @mixin' % mixin_class.__name__)

    if any(entry['mixin_class'] is mixin_class for entry in __MIXINS__):
        return

    resolved_ranking = meta['ranking'] if ranking is None else ranking
    merged_props = {**meta.get('props', {}), **props}
    target = _resolve_target(meta['target'])
    _prepend_base(target, mixin_class)
    __MIXINS__.append({
        'ranking': resolved_ranking,
        'mixin_class': mixin_class,
        'target': target,
        'props': merged_props,
    })


def load_mixins_from_entrypoints(group: str = MIXIN_ENTRY_POINT_GROUP):
    """Load ``@mixin`` classes from packaging entry points and apply them by ranking."""
    loaded = []
    for ep in _iter_entry_points(group):
        cls = ep.load()
        meta = get_mixin_meta(cls)
        if meta is None:
            raise ValueError(
                'Entry point %s did not load an @mixin-decorated class: %s' % (ep.name, cls))
        loaded.append(cls)
    for cls in sorted(loaded, key=lambda c: get_mixin_meta(c)['ranking']):
        register_mixin(cls)


def load_plugins_by_package(ns_pkg, ranking: int = 1000, **props):
    """Loads all valid plugin classes by the provided package.

    .. deprecated::
        Prefer ``@plugin`` plus the ``ancpbids.plugins`` entry-point group
        (see ``load_plugins_from_entrypoints``). Package scanning remains for
        transitional use and will be removed in a future release.

    Parameters
    ----------
    ns_pkg:
        the package to scan for plugin classes
    ranking:
        the ranking to use for any detected plugin class
    props
        the properties to assign to the detected plugin classes
    Returns
    -------
    list
        a list of plugin classes or empty if no valid plugin classes found
    """
    warnings.warn(
        'load_plugins_by_package is deprecated; use @plugin and the '
        'ancpbids.plugins entry-point group (load_plugins_from_entrypoints) instead',
        DeprecationWarning,
        stacklevel=2,
    )
    mods = [importlib.import_module(name) for finder, name, ispkg in
            pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")]
    for mod in mods:
        for mem in inspect.getmembers(mod, inspect.isclass):
            plugin_class = mem[1]
            if is_valid_plugin(plugin_class):
                register_plugin(plugin_class, ranking, **props)


def _iter_entry_points(group: str):
    eps = entry_points()
    if hasattr(eps, "select"):
        return eps.select(group=group)
    return eps.get(group, ())


def load_plugins_from_entrypoints(group: str = PLUGIN_ENTRY_POINT_GROUP, ranking: int = 1000, **props):
    """Loads plugin classes advertised via packaging entry points.

    If you maintain a separate installable package, declare each plugin in
    *your* ``pyproject.toml`` under the ``ancpbids.plugins`` group::

        [project.entry-points."ancpbids.plugins"]
        site_rules = "lab_bids_extensions.validation:SiteRulesPlugin"

    Prefer decorating the class with ``@plugin(ranking=...)`` so ranking/props
    travel with the class. Undecorated entry points use the ``ranking``/``props``
    arguments of this loader.

    Parameters
    ----------
    group:
        the entry-point group to scan (default: ``ancpbids.plugins``)
    ranking:
        fallback ranking when the class has no ``@plugin`` metadata
    props
        fallback properties merged under any ``@plugin`` props
    """
    for ep in _iter_entry_points(group):
        cls = ep.load()
        meta = get_plugin_meta(cls)
        if meta:
            register_plugin(cls, ranking=meta['ranking'], **{**props, **meta.get('props', {})})
        else:
            register_plugin(cls, ranking, **props)


def register_plugin(plugin_class, ranking: int = 1000, **props):
    """Registers the provided plugin class. If the class is not considered a valid plugin class a ValueError is raised.

    Parameters
    ----------
    plugin_class:
        The plugin class to register.
    ranking:
        The rank to use for the plugin to help prioritize plugins of same type.
        Note that the lower the ranking the higher its prioritization in the processing.
        System level plugins are registered with `ranking = 0`, i.e.
        if you need your plugin to be prioritized over system plugins, use a ranking below 0.
    props
        Additional (static) properties to attach to the provided plugin class.

    """
    if not is_valid_plugin(plugin_class):
        raise ValueError('Invalid plugin class: %s' % plugin_class.__name__)

    if any(entry['plugin_class'] is plugin_class for entry in __PLUGINS__):
        return

    meta = get_plugin_meta(plugin_class)
    if meta:
        ranking = meta['ranking']
        props = {**meta.get('props', {}), **props}

    __PLUGINS__.append({
        'ranking': ranking,
        'plugin_class': plugin_class,
        'props': props
    })


def get_plugins(plugin_class, **props) -> List[Plugin]:
    """Returns a list of plugin instances matching the provided plugin class and properties.

    Parameters
    ----------
    plugin_class:
        the plugin class to filter by
    props:
        additional filters found in any attached plugin properties

    Returns
    -------
        a list of plugin instances matching the provided plugin class and properties
    """
    plugins = filter(lambda entry: issubclass(entry['plugin_class'], plugin_class), __PLUGINS__)
    plugins = sorted(plugins, key=lambda entry: entry['ranking'])
    # note that a concrete instance of the plugin classes is returned
    return list(map(lambda entry: entry['plugin_class'](**entry['props']), plugins))
