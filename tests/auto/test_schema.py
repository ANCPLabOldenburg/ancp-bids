
import pytest
from ancpbids import model_v1_8_0, model_latest, load_dataset, load_schema, DatasetOptions
from ..base_test_case import DS005_DIR, DS005_SMALL_DIR

def test_entity_matching():
    assert model_latest.fuzzy_match_entity_key('sub') == 'sub'
    assert model_latest.fuzzy_match_entity_key('subject') == 'sub'
    assert model_latest.fuzzy_match_entity_key('subjects') == 'sub'
    assert model_latest.fuzzy_match_entity_key('subjs') == 'sub'
    assert model_latest.fuzzy_match_entity_key('des') == 'desc'
    assert model_latest.fuzzy_match_entity_key('dscr') == 'desc'
    assert model_latest.fuzzy_match_entity_key('descriptions') == 'desc'


@pytest.mark.parametrize("lazy_loading", [True, False])
def test_schema_versions(lazy_loading):
    ds_latest = load_dataset(DS005_DIR, DatasetOptions(lazy_loading=lazy_loading))
    schema_latest = ds_latest.get_schema()
    assert schema_latest == model_latest
    assert schema_latest.VERSION == '1.11.1'

    ds_old = load_dataset(DS005_SMALL_DIR, DatasetOptions(lazy_loading=lazy_loading))
    schema_old = ds_old.get_schema()
    assert schema_old == model_v1_8_0
    assert schema_old.VERSION == '1.8.0'

def test_load_schema():
    schema_latest = load_schema(DS005_DIR)
    assert schema_latest == model_latest
    assert schema_latest.VERSION == '1.11.1'

    schema_v180 = load_schema(DS005_SMALL_DIR)
    assert schema_v180 == model_v1_8_0
    assert schema_v180.VERSION == '1.8.0'

    # The classes of each schema are separate identities
    # assert on arbitrary class
    assert not (schema_latest.DatatypeEnum == schema_v180.DatatypeEnum)

def test_v190_motion_modality_exists():
    from ancpbids import model_v1_9_0
    # in 1.9.0 the motion modality was added
    assert "motion" in [e.name for e in model_v1_9_0.ModalityEnum]

def test_v110_mrs_modality_exists():
    from ancpbids import model_v1_10_0
    # in 1.10.0 the mrs modality was added
    assert "mrs" in [e.name for e in model_v1_10_0.ModalityEnum]


def test_v1101_phenotype_datatype_exists():
    from ancpbids import model_v1_10_1
    assert "phenotype" in [e.name for e in model_v1_10_1.DatatypeEnum]


def test_v111_emg_exists():
    from ancpbids import model_v1_11_0, model_v1_11_1
    assert "emg" in [e.name for e in model_v1_11_0.ModalityEnum]
    assert "emg" in [e.name for e in model_v1_11_0.DatatypeEnum]
    assert "emg" in [e.name for e in model_v1_11_1.ModalityEnum]


def test_vendored_schema_json():
    from ancpbids.schema import available_versions, load, load_json

    versions = available_versions()
    assert versions[0] == "1.8.0"
    assert versions[-1] == "1.11.1"
    document = load_json("1.11.1")
    assert document["bids_version"] == "1.11.1"
    assert "rules" in document
    assert "objects" in document
    assert load_json("v1.8.0")["bids_version"] == "1.8.0"
    assert load("1.11.1") is model_latest
    assert load("v1.8.0") is model_v1_8_0


def test_schema_stubs():
    from pathlib import Path
    from ancpbids import schema as schema_pkg

    stub_dir = Path(schema_pkg.__file__).parent / "stubs"
    stub_180 = (stub_dir / "v1_8_0.pyi").read_text()
    stub_111 = (stub_dir / "v1_11_1.pyi").read_text()
    aliases = (stub_dir / "aliases.pyi").read_text()
    assert "class SuffixEnum(Enum):" in stub_180
    assert "    bold = ..." in stub_180
    assert "    emg = ..." not in stub_180
    assert "    emg = ..." in stub_111
    assert "model_v1_8_0:" in aliases
    assert "model_latest:" in aliases
    assert (stub_dir / "v1_8_0.py").exists()
    from ancpbids.schema.stubs.v1_8_0 import Schema as StubSchema
    assert StubSchema is schema_pkg.Schema


def test_members_from_properties():
    schema = model_latest
    by_name = {m['name']: m for m in schema.get_members(schema.Dataset)}
    assert not hasattr(schema.Dataset, 'MEMBERS')
    assert by_name['subjects']['type'] is schema.Subject
    assert by_name['subjects']['max'] > 1
    assert by_name['subjects']['meta']['name_pattern'] == 'sub-.*'
    assert by_name['dataset_description']['type'] is schema.DatasetDescriptionFile
    assert by_name['participants_tsv']['meta']['name_pattern'] == 'participants.tsv'
    assert by_name['files']['type'] is schema.File

    json_members = {m['name']: m for m in schema.get_members(schema.JsonFile)}
    assert json_members['contents']['type'] is dict

    subject = {m['name']: m for m in schema.get_members(schema.Subject)}
    assert subject['sessions']['meta']['name_pattern'] == 'ses-.*'
    assert subject['datatypes']['meta']['name_pattern'] == '.*'
    assert schema.get_members(schema.DatatypeFolder, include_superclass=False) == []
