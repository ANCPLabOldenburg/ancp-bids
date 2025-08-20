
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
    assert schema_latest.VERSION == '1.10.0'

    ds_old = load_dataset(DS005_SMALL_DIR, DatasetOptions(lazy_loading=lazy_loading))
    schema_old = ds_old.get_schema()
    assert schema_old == model_v1_8_0
    assert schema_old.VERSION == 'v1.8.0'

def test_load_schema():
    schema_latest = load_schema(DS005_DIR)
    assert schema_latest == model_latest
    assert schema_latest.VERSION == '1.10.0'

    schema_v180 = load_schema(DS005_SMALL_DIR)
    assert schema_v180 == model_v1_8_0
    assert schema_v180.VERSION == 'v1.8.0'

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
    assert "motion" in [e.name for e in model_v1_10_0.ModalityEnum]
