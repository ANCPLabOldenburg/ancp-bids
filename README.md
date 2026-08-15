[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/ANCPLabOldenburg/ancp-bids)
[![Documentation Status](https://readthedocs.org/projects/ancpbids/badge/?version=latest)](http://ancpbids.readthedocs.io/en/latest/?badge=latest)
[![Latest Version](https://img.shields.io/pypi/v/ancpbids.svg)](https://pypi.python.org/pypi/ancpbids/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ancpbids.svg)](https://pypi.python.org/pypi/ancpbids/)
[![Test Status](https://github.com/ANCPLabOldenburg/ancp-bids/actions/workflows/testing.yml/badge.svg)](https://github.com/ANCPLabOldenburg/ancp-bids/actions/workflows/testing.yml)
[![Codecov](https://codecov.io/gh/ANCPLabOldenburg/ancp-bids/branch/main/graph/badge.svg)](https://codecov.io/gh/ANCPLabOldenburg/ancp-bids)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

**ancpBIDS** is a modular Python library for reading, querying, validating, and writing BIDS datasets. Its architecture is designed for extensibility and maintainability.

## Key Features

- **BIDS Dataset Loading**  
	Load BIDS datasets of any size or complexity, with support for multiple BIDS schema versions.

- **Flexible Query Engine**  
	Query files, folders, and metadata using a powerful, Pythonic API. Supports entity-based, scope-based, and custom queries.

- **Validation**  
	Validate datasets against the BIDS specification and custom rules using a plugin-based validation system.

- **Writing and Derivatives**  
	Write and update BIDS datasets, including support for creating and saving BIDS derivatives.

- **Lazy Loading**  
	Efficiently handle large datasets with optional lazy loading, reducing memory usage and speeding up initial access.

- **Plugin Architecture**  
	Extend or customize core functionality (validation, file handling, schema, etc.) via a robust plugin system.

- **PyBIDS Compatibility Layer**  
	Drop-in compatibility for many `pybids` API calls, easing migration from or integration with existing codebases.

- **Synthetic and Real Data Support**  
	Works with both synthetic test datasets and real-world BIDS datasets.

- **CI/CD Ready**  
	Includes a comprehensive suite of automated and manual tests, with synthetic datasets for reproducibility.

- **Extensible and Versioned Schema**  
	Supports multiple BIDS schema versions and allows for easy extension as the BIDS standard evolves.

## Architecture

- **Core Models:**  
	The in-memory graph is hand-maintained in `ancpbids/model_base.py`. Versioned enums are loaded at runtime from official BIDS `schema.json` files vendored in `ancpbids/schema/`.

- **Plugin System:**  
	The plugin mechanism (see `ancpbids/plugin.py`) allows for dynamic extension of core functionality. Plugins can hook into schema modification, dataset processing, file handling, writing, and validation. Graph methods (`query`, `get_schema`, …) live on the model classes; `SchemaPlugin` remains an extension point.

- **Query Engine:**  
	The query logic is implemented in `ancpbids/query.py`, providing flexible access to dataset contents and metadata.

- **Compatibility Layer:**  
	`ancpbids/pybids_compat.py` provides compatibility with the pybids API for easier migration and integration.

- **Utilities:**  
	Helper functions and utilities are in `ancpbids/utils.py`.

- **Testing:**  
	The `tests/` directory is organized into `auto` (CI-safe) and `manual` (non-deterministic or performance) tests, with synthetic datasets under `tests/data/`.

## Plugin and mixin system

Extensibility comes in two shapes:

- **Plugins** — hook into load / write / validate / schema / file I/O (`execute` methods).
- **Mixins** — add methods to a host class such as `BIDSLayout` via `@mixin(target=...)`.

Built-in plugins/mixins are registered the same way: decorated with
`@plugin(ranking=0, system=True)` / `@mixin(...)` and listed under
`ancpbids.plugins` / `ancpbids.mixins` in this project's `pyproject.toml`.
Third-party packages add their own entries to those groups.

### Registering an external plugin

1. Decorate a plugin subclass:

	```python
	from ancpbids.plugin import ValidationPlugin, plugin

	@plugin(ranking=1000)
	class SiteRulesPlugin(ValidationPlugin):
	    def execute(self, dataset, report: ValidationPlugin.ValidationReport):
	        pass
	```

2. In **your** package’s `pyproject.toml`:

	```toml
	[project.entry-points."ancpbids.plugins"]
	site_rules = "lab_bids_extensions.validation:SiteRulesPlugin"
	```

3. Install alongside ancpBIDS; importing `ancpbids` loads the plugin.

### Registering an external mixin

1. Decorate a mixin with a target (live class or `"module:Class"` string):

	```python
	from ancpbids import BIDSLayout
	from ancpbids.plugin import mixin

	@mixin(target=BIDSLayout, ranking=1000)
	class MyExportMixin:
	    def to_custom(self):
	        ...
	```

2. Advertise under `ancpbids.mixins`:

	```toml
	[project.entry-points."ancpbids.mixins"]
	my_export = "lab_bids_extensions.exports:MyExportMixin"
	```

Built-in `DataFrameMixin` lives in `ancpbids.mixins.mixin_dataframe`, uses `@mixin(target=BIDSLayout, ranking=0)`, and is listed as `to_df` under the `ancpbids.mixins` entry-point group in this project's `pyproject.toml`.

Full guide: [docs/source/plugins.rst](docs/source/plugins.rst).

## Versioning and Schema Evolution

- The codebase supports multiple BIDS schema versions via vendored `schema.json` files.
- The schema is loaded dynamically based on the dataset version, allowing for forward compatibility.

## Testing and CI

- **Unit Tests:**  
	Located in `tests/auto/`, these are run automatically in CI.
- **Manual/Performance Tests:**  
	Located in `tests/manual/`, these are for benchmarking or non-deterministic checks.
- **Synthetic Data:**  
	All tests use synthetic datasets in `tests/data/` to ensure reproducibility.

## Developer Guidelines

- **Extending the Model:**  
	Add a new `ancpbids/schema/schema_v<version>.json` (see Model Generation Utility). Type stubs and `model_latest` update from the vendored JSON files.
- **Adding Plugins:**  
	Follow the plugin system described above (including external entry points).
- **Testing:**  
	Add new tests to `tests/auto/` for CI-safe code, and to `tests/manual/` for performance or integration tests.
- **Documentation:**  
	Update `README.md` and docstrings for any new features or changes.

## Code Quality

- The codebase uses type hints and docstrings for clarity.
- Contributions should follow PEP8 and include tests and documentation.
## Model Generation Utility

The in-memory graph (`ancpbids/model_base.py`) is hand-maintained. `tools/generatemodel.py` fetches an official BIDS `schema.json` into `ancpbids/schema/` and writes version-specific type stubs (`v1_X_Y.pyi`) so IDEs can see enum literals such as `SuffixEnum.bold`. Enums are still built from JSON at runtime.

**Usage:**

```bash
uv run --with requests python tools/generatemodel.py [--schema-version <version>]
uv run python tools/generatemodel.py --stubs-only
```

- If `--schema-version` is omitted, the latest available schema version is used.
- `--stubs-only` regenerates stubs from JSON files already in `ancpbids/schema/`.
- Output: `ancpbids/schema/schema_v<version>.json`, `ancpbids/schema/v1_X_Y.pyi`, and `ancpbids/schema/aliases.pyi`.


## Further Reading

- [BIDS Specification](https://bids.neuroimaging.io/)
- [ancpBIDS Documentation](https://ancpbids.readthedocs.io)