# Schema-driven validation

ancpbids runs official BIDS `schema.document` rules against the in-memory
dataset graph (no Deno shell-out). Entry points:

| Module / folder | Role |
|-----------------|------|
| `expr.py` | Schema expression language (`meta.expression_tests` oracle) |
| `validate.py` | Thin public API (`files` / `entities` / …) |
| `session.py` | Shared `ValidationSession`, rule indexing, selectors |
| `context.py` | Rich file context (sidecar, columns, associations, headers) |
| `values.py` | Value constraints and issue helpers |
| `rules/` | One module per schema rule family |
| `headers.py` | NIfTI/GZIP/TIFF/OME header readers (nibabel preferred for NIfTI) |
| `versions/` | Vendored official `schema_v*.json` (runtime source of truth) |
| `stubs/` | Generated `.py` / `.pyi` shims for IDE enum literals |
| `../plugins/plugin_schema_validator.py` | Thin `ValidationPlugin` wrappers per rule family |

Public API: `validate_dataset()` → `ValidationReport` (optional `code` / `sub_code`).

Reference implementation: [bids-validator](https://github.com/bids-standard/bids-validator)
(Deno/TS). Context shapes follow `meta.context` in the BIDS schema.

Regenerate stubs after adding JSON under `versions/`:

```bash
uv run python tools/generatemodel.py --stubs-only
```

## Covered today

**Rule families** — `rules.files`, `entities`, `directories`, `sidecars`, `json`,
`dataset_metadata`, `tabular_data`, `checks`.

**Context (major fields)** — `path`, `entities`, `datatype`, `suffix`, `extension`,
`modality`, `sidecar` (inheritance), `json`, `columns` (`.tsv` / `.tsv.gz` /
headerless motion), `nifti_header`, `gzip`, `ome`, `tiff`, `subject.sessions`,
`dataset.*`, `associations` (events, aslcontext, bval/bvec, channels, coordsystem,
coordsystems, physio+sidecar, electrodes, magnitude/m0scan, atlas_description).

**Parity highlights already landed**

- Filename identify-then-validate (`MISSING_REQUIRED_ENTITY`, `EXTENSION_MISMATCH`, …)
  instead of collapsing mismatches to `NOT_INCLUDED` only
- Derivative sidecar optionality (skip missing keys unless the rule selects
  `DatasetType == "derivative"`)
- `coordsystems` multi-file association; `physio.sidecar`
- TSV structure basics (`TSV_EQUAL_ROWS`, `TSV_EMPTY_LINE`, …)
- `AMBIGUOUS_AFFINE` when `axis_codes` is null
- Selector truthiness treats non-empty `intersects()` lists as matching

Vendored schemas: BIDS **1.8.0–1.11.1**. Deno’s default schema package may be newer.

## Known gaps vs Deno validator

Prioritized for later work. “P1” blocks close schema-check parity on real datasets;
“P2” is same-pipeline product behavior; “P3” is infra / out of library scope.

### P1 — schema-check / context parity

1. **`SIDECAR_FIELD_OVERRIDE`**  
   Deno tracks sidecar key origins and errors when inheritance merges conflicting
   values. We `deepupdate` silently in `Artifact.get_metadata()`.

2. **Sidecar-refined TSV column typing**  
   Deno applies sidecar `Format` / `Levels` / `Units` / min-max to column values and
   can emit `TSV_COLUMN_TYPE_REDEFINED`. We only use schema column object defs.

3. **Deeper JSON / metadata validation**  
   Deno uses AJV over metadata defs (`JSON_SCHEMA_VALIDATION_ERROR` with full
   keyword coverage). Our `_value_matches` covers type/enum/anyOf/minmax/items/
   pattern/format but is weaker on nested `additionalProperties` and complex
   objects (`StimulusPresentation`, coordinate maps, etc.).

4. **Association / inheritance polish**  
   - Mark associated files as `viewed` during walk-back  
   - Stronger multi-candidate handling beyond current
     `MULTIPLE_INHERITABLE_FILES` / first-match for non-multi targets  
   Unlocks orphan checks below.

5. **Dataset orphans (needs `viewed` tracking)**  
   - `SIDECAR_WITHOUT_DATAFILE`  
   - `UNUSED_STIMULUS`

6. **`RepetitionTime` float rounding**  
   Deno rounds TR in sidecar context for float-safe schema compares.

### P2 — pipeline extras Deno runs alongside schema rules

7. **HED** — `@hed/validator` integration; we only model `HEDVersion`.  
8. **`CITATION.cff`** — AJV validate citation file.  
9. **Misc file issues** — `EMPTY_FILE`, `CASE_COLLISION`, `ENTITY_WITH_NO_LABEL`.  
10. **Encoding** — reject JSON BOM / UTF-16 (`INVALID_JSON_ENCODING`); our
    `json.load` is permissive / silent on some failures.  
11. **Symlinks** — broken / cycle / out-of-tree / submodule reporting. Loader uses
    `follow_symlinks=False` for dirs but does not emit symlink issues.  
12. **Validator config** — severity overrides (`ignore` / `warning` / `error`
    patterns), `--ignoreNiftiHeaders`, `--ignoreWarnings`, modality blacklist,
    `--datasetTypes`, `--recursive`, `--maxRows`, `--prune`, `--filenameMode`.  
13. **Recursive derivatives** — Deno strips `derivatives/` then optionally
    re-validates as nested results. We keep derivatives in-graph with local
    `dataset_description` (intentional product difference; document policy if
    changing).  
14. **Directory-node contexts** — Deno can apply rules to directory entries
    (`directory: true`, size aggregation). We skip opaque children but do not
    treat dirs as full validation contexts.

### P3 — infra / reporting

15. Git / annex tree loading, browser `FileTree`.  
16. Summary report object and verbose “passing rules” output.  
17. Issue message templates with context interpolation (Deno formatter).  
18. Sidecar-key validation caching (`sidecarKeyValidated`) — mostly performance.

## Suggested implementation order

1. `SIDECAR_FIELD_OVERRIDE` + sidecar origin map  
2. Sidecar-refined TSV typing  
3. `viewed` tracking → orphan issues  
4. Deeper JSON validation (or optional AJV/`jsonschema` extra)  
5. Config / severity overrides if exposing a CLI-like API  
6. HED / CITATION.cff if full product parity is required  

## Notes

- **Derivatives:** in-graph vs Deno’s opt-in `--recursive` is a product choice, not
  only a missing check.  
- **Header parsing attribution:** see module docstring in `headers.py` (patterns
  adapted from bids-validator `src/files/nifti.ts`, `gzip.ts`, `tiff.ts`).  
- **Schema drift:** re-vendor when targeting newer `@bids/schema` than 1.11.1.
