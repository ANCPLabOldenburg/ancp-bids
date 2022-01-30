import importlib
import inspect
import pkgutil
from typing import List

# global plugins registry (list of plugin metadata/settings)
__PLUGINS__ = []

from ancpbids import model


class Plugin:
    def __init__(self, **props):
        self.props = props


class DatasetPlugin(Plugin):
    def execute(self, dataset: model.Dataset):
        raise NotImplementedError()


class WritingPlugin(Plugin):
    def execute(self, dataset: model.Dataset, target_dir: str, context_folder: model.Folder = None,
                src_dir: str = None):
        raise NotImplementedError()


class ValidationPlugin(Plugin):
    class ValidationReport:
        def __init__(self):
            self.messages = []

        def error(self, message):
            self.messages.append({
                'severity': 'error',
                'message': message
            })

        def warn(self, message):
            self.messages.append({
                'severity': 'warn',
                'message': message
            })

    class ValidationRule:
        def validate(self, **kwargs):
            raise NotImplementedError()

    def execute(self, dataset: model.Dataset, report: ValidationReport):
        raise NotImplementedError()


def is_valid_plugin(plugin_class):
    plugin_types = (DatasetPlugin, WritingPlugin, ValidationPlugin)
    return issubclass(plugin_class, plugin_types) and plugin_class not in plugin_types


def load_plugins_by_package(ns_pkg, ranking: int = 1000, **props):
    mods = [importlib.import_module(name) for finder, name, ispkg in
            pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")]
    for mod in mods:
        for mem in inspect.getmembers(mod, inspect.isclass):
            plugin_class = mem[1]
            if is_valid_plugin(plugin_class):
                register_plugin(plugin_class, ranking, **props)


def register_plugin(plugin_class, ranking: int = 1000, **props):
    if not is_valid_plugin(plugin_class):
        raise ValueError('Invalid plugin class: %s' % plugin_class.__name__)

    __PLUGINS__.append({
        'ranking': ranking,
        'plugin_class': plugin_class,
        'props': props
    })


def get_plugins(plugin_class, **props) -> List[Plugin]:
    plugins = filter(lambda entry: issubclass(entry['plugin_class'], plugin_class), __PLUGINS__)
    plugins = sorted(plugins, key=lambda entry: entry['ranking'])
    # note that a concrete instance of the plugin classes is returned
    return list(map(lambda entry: entry['plugin_class'](**entry['props']), plugins))
