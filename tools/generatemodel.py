#!/usr/bin/env python
"""Download official BIDS schema.json files and emit type-checker stubs.

The in-memory graph in ancpbids/model_base.py is hand-maintained.
Enums and rules are loaded from these JSON files at runtime. Stubs under
ancpbids/schema/stubs/ restore compile-time enum literals for IDEs.
"""
import argparse
import json
import keyword
from io import StringIO
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TOOLS_DIR.parent
SCHEMA_DIR = REPO_ROOT / "ancpbids" / "schema"
VERSIONS_DIR = SCHEMA_DIR / "versions"
STUBS_DIR = SCHEMA_DIR / "stubs"
JSON_PREFIX = "schema_v"
JSON_SUFFIX = ".json"


def fetch_schema_version(version_tag=None):
    import requests

    if version_tag:
        schema_url = (
            f"https://raw.githubusercontent.com/bids-standard/bids-schema/main/"
            f"versions/{version_tag}/schema.json"
        )
        return version_tag, schema_url

    url = "https://api.github.com/repos/bids-standard/bids-schema/contents/versions"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(
            f"Failed to fetch schema versions from GitHub. Status code: {response.status_code}"
        )

    version_dirs = [
        item["name"]
        for item in response.json()
        if item["type"] == "dir" and all(part.isdigit() for part in item["name"].split("."))
    ]
    if not version_dirs:
        raise Exception("No valid version directories found.")

    version_dirs.sort(key=lambda v: list(map(int, v.split("."))), reverse=True)
    latest_version = version_dirs[0]
    latest_schema_url = (
        f"https://raw.githubusercontent.com/bids-standard/bids-schema/main/"
        f"versions/{latest_version}/schema.json"
    )
    return latest_version, latest_schema_url


def download_schema(schema_url, save_path: Path):
    import requests

    response = requests.get(schema_url)
    if response.status_code != 200:
        raise Exception(f"Failed to download schema. Status code: {response.status_code}")
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_text(response.text)
    print(f"Schema downloaded and saved to {save_path}")


def nested(schema, path):
    context = schema
    for part in path.split("/"):
        context = context[part]
    return context


def _stub_module_name(version: str) -> str:
    return f"v{version.replace('.', '_')}"


def _enum_members(members: dict):
    return [
        key for key in members
        if key.isidentifier() and not keyword.iskeyword(key)
    ]


def _write_enum_stub(out: StringIO, class_name: str, members: dict):
    out.write(f"class {class_name}(Enum):\n")
    names = _enum_members(members)
    if not names:
        out.write("    ...\n\n")
        return
    for key in names:
        out.write(f"    {key} = ...\n")
    out.write("\n")


def render_version_stub(document: dict, version: str) -> str:
    unordered_entities = nested(document, "objects/entities")
    ordered_entities = {
        name: unordered_entities[name] for name in document["rules"]["entities"]
    }
    out = StringIO()
    out.write("# Generated from schema.json — do not edit by hand.\n")
    out.write(f"# BIDS version {version}\n")
    out.write("from enum import Enum\n")
    out.write("from .. import Schema as SchemaBase\n\n")
    _write_enum_stub(out, "DatatypeEnum", nested(document, "objects/datatypes"))
    _write_enum_stub(out, "ModalityEnum", nested(document, "objects/modalities"))
    _write_enum_stub(out, "SuffixEnum", nested(document, "objects/suffixes"))
    _write_enum_stub(out, "EntityEnum", ordered_entities)
    out.write("class Schema(SchemaBase):\n")
    out.write("    DatatypeEnum: type[DatatypeEnum]\n")
    out.write("    ModalityEnum: type[ModalityEnum]\n")
    out.write("    SuffixEnum: type[SuffixEnum]\n")
    out.write("    EntityEnum: type[EntityEnum]\n")
    return out.getvalue()


def render_aliases(versions: list) -> str:
    out = StringIO()
    out.write("# Generated from vendored schema.json files — do not edit by hand.\n")
    for version in versions:
        mod = _stub_module_name(version)
        alias = f"SchemaV{version.replace('.', '_')}"
        out.write(f"from .{mod} import Schema as {alias}\n")
    out.write("\n")
    for version in versions:
        alias = f"SchemaV{version.replace('.', '_')}"
        out.write(f"model_v{version.replace('.', '_')}: {alias}\n")
    latest_alias = f"SchemaV{versions[-1].replace('.', '_')}"
    out.write(f"model_latest: {latest_alias}\n")
    return out.getvalue()


def vendored_versions():
    versions = []
    for path in VERSIONS_DIR.glob(f"{JSON_PREFIX}*{JSON_SUFFIX}"):
        versions.append(path.name[len(JSON_PREFIX):-len(JSON_SUFFIX)])
    versions.sort(key=lambda v: tuple(int(part) for part in v.split(".")))
    return versions


def render_version_shim() -> str:
    return (
        "# Generated import shim; enum members are declared in the .pyi stub.\n"
        "from .. import Schema as Schema\n"
    )


def render_aliases_py(versions: list) -> str:
    out = StringIO()
    out.write("# Generated import shim; see aliases.pyi for types.\n")
    for version in versions:
        mod = _stub_module_name(version)
        alias = f"SchemaV{version.replace('.', '_')}"
        out.write(f"from .{mod} import Schema as {alias}\n")
    return out.getvalue()


def generate_all_stubs():
    versions = vendored_versions()
    if not versions:
        raise Exception(f"No schema JSON files found in {VERSIONS_DIR}")
    STUBS_DIR.mkdir(parents=True, exist_ok=True)
    shim = render_version_shim()
    for version in versions:
        json_path = VERSIONS_DIR / f"{JSON_PREFIX}{version}{JSON_SUFFIX}"
        document = json.loads(json_path.read_text())
        mod = _stub_module_name(version)
        stub_path = STUBS_DIR / f"{mod}.pyi"
        stub_path.write_text(render_version_stub(document, version))
        print(f"Wrote {stub_path}")
        shim_path = STUBS_DIR / f"{mod}.py"
        shim_path.write_text(shim)
        print(f"Wrote {shim_path}")
    aliases_pyi = STUBS_DIR / "aliases.pyi"
    aliases_pyi.write_text(render_aliases(versions))
    print(f"Wrote {aliases_pyi}")
    aliases_py = STUBS_DIR / "aliases.py"
    aliases_py.write_text(render_aliases_py(versions))
    print(f"Wrote {aliases_py}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download official BIDS schema.json and generate type stubs."
    )
    parser.add_argument(
        "--schema-version",
        type=str,
        help="Schema version to download (default is latest).",
    )
    parser.add_argument(
        "--stubs-only",
        action="store_true",
        help="Regenerate stubs from already vendored schema JSON files.",
    )
    args = parser.parse_args()

    if not args.stubs_only:
        version_tag = args.schema_version
        if version_tag:
            _, schema_url = fetch_schema_version(version_tag)
        else:
            version_tag, schema_url = fetch_schema_version()
        print(f"Using schema version: {version_tag}")
        VERSIONS_DIR.mkdir(parents=True, exist_ok=True)
        save_path = VERSIONS_DIR / f"{JSON_PREFIX}{version_tag}{JSON_SUFFIX}"
        download_schema(schema_url, save_path)

    generate_all_stubs()
