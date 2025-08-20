
import ancpbids
from ..base_test_case import DS005_DIR

def test_get_all_files_from_pipeline():
    dataset = ancpbids.load_dataset(DS005_DIR)
    all_derivative_files = dataset.query(scope='derivatives/affine/matrix', return_type='file')
    assert len(all_derivative_files) == 16

def test_report_errors():
    dataset = ancpbids.load_dataset(DS005_DIR)
    report = ancpbids.validate_dataset(dataset)
    assert report.has_errors()

def test_get_entitites_no_scope():
    dataset = ancpbids.load_dataset(DS005_DIR)
    entities = dataset.query_entities(scope=None)
    assert ['ds', 'type', 'subject', 'task', 'run', 'description'] == list(entities.keys())
