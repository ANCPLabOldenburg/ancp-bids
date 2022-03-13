import importlib
import inspect
import pkgutil
from typing import List

# global plugins registry (list of plugin metadata/settings)
__PLUGINS__ = []


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

        def error(self, message):
            """Adds a new error message to the report.

            Parameters
            ----------
            message:
                the error message to add to the report

            """
            self.messages.append({
                'severity': 'error',
                'message': message
            })

        def warn(self, message):
            """Adds a new warning message to the report.

            Parameters
            ----------
            message:
                the warning message to add to the report

            """
            self.messages.append({
                'severity': 'warn',
                'message': message
            })

        def has_errors(self):
            """
            Returns
            -------
            bool
                whether this report contains errors
            """
            for m in self.messages:
                if m['severity'] == 'error':
                    return True
            return False

    def execute(self, dataset, report: ValidationReport):
        raise NotImplementedError()


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


def load_plugins_by_package(ns_pkg, ranking: int = 1000, **props):
    """Loads all valid plugin classes by the provided package.

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
    mods = [importlib.import_module(name) for finder, name, ispkg in
            pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")]
    for mod in mods:
        for mem in inspect.getmembers(mod, inspect.isclass):
            plugin_class = mem[1]
            if is_valid_plugin(plugin_class):
                register_plugin(plugin_class, ranking, **props)


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
