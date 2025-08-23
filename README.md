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
	The core BIDS data model is implemented in `ancpbids/model_base.py` and versioned model files (e.g., `model_v1_8_0.py`). These define the schema and object graph for BIDS datasets.

- **Plugin System:**  
	The plugin mechanism (see `ancpbids/plugin.py`) allows for dynamic extension of core functionality. Plugins can hook into schema modification, dataset processing, file handling, writing, and validation.

- **Query Engine:**  
	The query logic is implemented in `ancpbids/query.py`, providing flexible access to dataset contents and metadata.

- **Compatibility Layer:**  
	`ancpbids/pybids_compat.py` provides compatibility with the pybids API for easier migration and integration.

- **Utilities:**  
	Helper functions and utilities are in `ancpbids/utils.py`.

- **Testing:**  
	The `tests/` directory is organized into `auto` (CI-safe) and `manual` (non-deterministic or performance) tests, with synthetic datasets under `tests/data/`.

## Plugin System

The plugin system is a core feature for extensibility:

- **Plugin Types:**  
	- `SchemaPlugin`: Modify or extend the BIDS schema.
	- `DatasetPlugin`: Operate on in-memory dataset graphs.
	- `FileHandlerPlugin`: Register custom file readers/writers.
	- `WritingPlugin`: Add files/folders during dataset writing.
	- `ValidationPlugin`: Add custom validation rules.

- **Registration and Discovery:**  
	Plugins are registered via `register_plugin` or discovered with `load_plugins_by_package`. They are prioritized by a `ranking` value.

- **Execution:**  
	At key points (e.g., dataset load, write, validate), the system retrieves and executes all relevant plugins using `get_plugins`.

- **How to Add a Plugin:**  
	1. Subclass the appropriate plugin base class from `plugin.py`.
	2. Implement the required `execute` method.
	3. Register your plugin using `register_plugin` or by placing it in a discoverable package.

## Versioning and Schema Evolution

- The codebase supports multiple BIDS schema versions, with separate model files for each version.
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
	Add new schema versions as new files in `ancpbids/`, following the pattern of existing model files.
- **Adding Plugins:**  
	Follow the plugin system described above.
- **Testing:**  
	Add new tests to `tests/auto/` for CI-safe code, and to `tests/manual/` for performance or integration tests.
- **Documentation:**  
	Update `README.md` and docstrings for any new features or changes.

## Code Quality

- The codebase uses type hints and docstrings for clarity.
- Contributions should follow PEP8 and include tests and documentation.
## Model Generation Utility

The script `tools/generatemodel.py` is provided to automate the generation of Python model classes from BIDS schema files. This utility ensures that the codebase can easily stay up-to-date with the latest BIDS schema versions.

**Features:**
- Fetches the latest or a specified BIDS schema version directly from the official BIDS GitHub repository.
- Downloads the schema and generates Python model files in the `ancpbids/` directory (e.g., `model_base.py`, `model_v<version>.py`).
- Supports custom ordering and enum generation for BIDS datatypes, modalities, suffixes, and entities.

**Usage:**

```bash
cd tools
python generatemodel.py [--schema-version <version>]
```

- If `--schema-version` is omitted, the latest available schema version will be used.
- The generated files will be saved in the `ancpbids/` directory and the corresponding schema in the `schema/` directory.

**When to use:**
- When a new BIDS schema version is released and you want to update the models.
- When making changes to the schema or model structure for development or testing.


## Further Reading

- [BIDS Specification](https://bids.neuroimaging.io/)
- [ancpBIDS Documentation](https://ancpbids.readthedocs.io)