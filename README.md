
# ancpBIDS Technical Overview

## Architecture

**ancpBIDS** is a modular Python library for reading, querying, validating, and writing BIDS datasets. Its architecture is designed for extensibility and maintainability, with the following key components:

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

## Further Reading

- [BIDS Specification](https://bids.neuroimaging.io/)
- [ancpBIDS Documentation](https://ancpbids.readthedocs.io)