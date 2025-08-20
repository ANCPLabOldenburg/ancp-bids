
from ancpbids import load_dataset
from ..base_test_case import SYNTHETIC_DIR, DS005_SMALL2_DIR

def test_derivative_generated_by():
    test_ds = load_dataset(SYNTHETIC_DIR)
    schema = test_ds.get_schema()
    fmriprep_folder = test_ds.derivatives.get_folder('fmriprep')
    assert isinstance(fmriprep_folder, schema.DerivativeFolder)
    assert isinstance(fmriprep_folder.dataset_description, schema.DerivativeDatasetDescriptionFile)
    dddf = fmriprep_folder.dataset_description
    assert len(dddf.GeneratedBy) == 1
    generated_by = dddf.GeneratedBy[0]
    assert generated_by.Name == "fmriprep"
    assert generated_by.Version == "1.1.0"
    assert generated_by.Container
    container = generated_by.Container
    assert container.Type == "abc"
    assert container.Tag == "xyz"
    assert container.URI == "test:abc/xyz"

def test_derivative_dataset_description():
    test_ds = load_dataset(DS005_SMALL2_DIR)
    schema = test_ds.get_schema()
    dd_files = test_ds.select(schema.DatasetDescriptionFile).objects(as_list=True)
    assert len(dd_files) == 2
    names = {'Mixed-gambles task', 'Mixed-gambles task -- dummy derivative'}
    dd_names = [d['Name'] for d in dd_files]
    assert set(dd_names) == names
    dd = dd_files[1]
    # PipelineDescription is not part of BIDS spec but available in the generic contents object
    assert dd.contents['PipelineDescription']['Name'] == 'events'

def test_create_artifact_with_raw():
    test_ds = load_dataset(DS005_SMALL2_DIR)
    sub01_json = test_ds.query(sub='01', suffix='bold', extension='.json')[0]
    derivative_folder = test_ds.create_derivative(name="unit-test")
    deriv_artifact = derivative_folder.create_artifact(raw=sub01_json)
    deriv_artifact.add_entities(desc='unittest')
    assert deriv_artifact.get_entity("sub") == "01"
    assert deriv_artifact.get_entity("task") == "mixedgamblestask"
    assert deriv_artifact.get_entity("run") == 1
    assert deriv_artifact.get_entity("desc") == "unittest"
