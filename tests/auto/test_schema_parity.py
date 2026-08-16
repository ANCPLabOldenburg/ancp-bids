import gzip
import json

from ancpbids import load_dataset, validate_dataset, DatasetOptions
from ancpbids.plugins.plugin_schema_validator import (
    SchemaFilesPlugin,
    SchemaSidecarsPlugin,
)
from ancpbids import _internal_validate_dataset


def _write_ds(root, description=None):
    root.mkdir(parents=True, exist_ok=True)
    (root / 'dataset_description.json').write_text(json.dumps(description or {
        'Name': 'Parity',
        'BIDSVersion': '1.11.1',
        'DatasetType': 'raw',
    }))


def test_physio_association_includes_sidecar(tmp_path):
    root = tmp_path / 'ds'
    _write_ds(root)
    func = root / 'sub-01' / 'func'
    func.mkdir(parents=True)
    (func / 'sub-01_task-rest_bold.nii.gz').write_bytes(b'\0')
    (func / 'sub-01_task-rest_bold.json').write_text(json.dumps({
        'RepetitionTime': 2.0,
        'TaskName': 'rest',
    }))
    (func / 'sub-01_task-rest_physio.json').write_text(json.dumps({
        'SamplingFrequency': 100,
        'StartTime': 0,
        'Columns': ['cardiac', 'respiratory'],
    }))
    with gzip.open(func / 'sub-01_task-rest_physio.tsv.gz', 'wb') as handle:
        handle.write(b'1\t2\n3\t4\n')

    ds = load_dataset(str(root), DatasetOptions(lazy_loading=True, ignore_pickle_file=True))
    report = validate_dataset(ds)
    session = report._schema_session
    bold = next(
        file for file in session.iter_files()
        if getattr(file, 'suffix', None) == 'bold'
    )
    ctx = session.context(bold, rich=True)
    physio = ctx['associations']['physio']
    assert physio is not None
    assert physio['sidecar']['SamplingFrequency'] == 100
    assert physio['sidecar']['Columns'] == ['cardiac', 'respiratory']

    physio_file = next(
        file for file in session.iter_files()
        if getattr(file, 'suffix', None) == 'physio'
    )
    physio_ctx = session.context(physio_file, rich=True)
    assert physio_ctx['columns']['cardiac'] == ['1', '3']
    assert physio_ctx['columns']['respiratory'] == ['2', '4']


def test_coordsystems_multi_association(tmp_path):
    root = tmp_path / 'ds'
    _write_ds(root)
    emg = root / 'sub-01' / 'emg'
    emg.mkdir(parents=True)
    (emg / 'sub-01_emg.edf').write_bytes(b'\0')
    (emg / 'sub-01_space-Cap_coordsystem.json').write_text(json.dumps({
        'ECGCoordinateSystem': 'Other',
        'ECGCoordinateUnits': 'mm',
        'ParentCoordinateSystem': 'Cap',
    }))
    (emg / 'sub-01_space-Other_coordsystem.json').write_text(json.dumps({
        'ECGCoordinateSystem': 'Other',
        'ECGCoordinateUnits': 'mm',
    }))

    ds = load_dataset(str(root), DatasetOptions(lazy_loading=True, ignore_pickle_file=True))
    report = validate_dataset(ds)
    session = report._schema_session
    data = next(
        file for file in session.iter_files()
        if getattr(file, 'suffix', None) == 'emg'
    )
    ctx = session.context(data, rich=True)
    coords = ctx['associations']['coordsystems']
    assert coords is not None
    assert len(coords['paths']) == 2
    assert set(coords['spaces']) == {'Cap', 'Other'}
    assert coords['ParentCoordinateSystems'] == ['Cap']


def test_filename_missing_required_entity_not_not_included(tmp_path):
    root = tmp_path / 'ds'
    _write_ds(root)
    func = root / 'sub-01' / 'func'
    func.mkdir(parents=True)
    (func / 'sub-01_bold.nii.gz').write_bytes(b'\0')

    ds = load_dataset(str(root), DatasetOptions(lazy_loading=True, ignore_pickle_file=True))
    report = _internal_validate_dataset(
        ds, lambda plugin: isinstance(plugin, SchemaFilesPlugin))
    codes = report.codes()
    assert 'MISSING_REQUIRED_ENTITY' in codes
    assert 'NOT_INCLUDED' not in codes


def test_derivative_sidecar_keys_optional(tmp_path):
    root = tmp_path / 'ds'
    _write_ds(root, {
        'Name': 'Deriv',
        'BIDSVersion': '1.11.1',
        'DatasetType': 'derivative',
        'GeneratedBy': [{'Name': 'demo'}],
    })
    func = root / 'sub-01' / 'func'
    func.mkdir(parents=True)
    (func / 'sub-01_task-rest_bold.nii.gz').write_bytes(b'\0')
    (func / 'sub-01_task-rest_bold.json').write_text(json.dumps({
        'RepetitionTime': 2.0,
        'TaskName': 'rest',
        'SkullStripped': False,
    }))

    ds = load_dataset(str(root), DatasetOptions(lazy_loading=True, ignore_pickle_file=True))
    report = _internal_validate_dataset(
        ds, lambda plugin: isinstance(plugin, SchemaSidecarsPlugin))
    # Raw MRI sidecar recommendations should be skipped for derivatives unless
    # the rule itself selects DatasetType == derivative.
    sub_codes = {message.get('sub_code') for message in report.messages}
    assert 'Manufacturer' not in sub_codes
    assert 'MagneticFieldStrength' not in sub_codes
    assert 'SIDECAR_KEY_REQUIRED' not in report.codes()

def test_tsv_equal_rows(tmp_path):
    root = tmp_path / 'ds'
    _write_ds(root)
    (root / 'participants.tsv').write_text('participant_id\tsex\nsub-01\n')

    ds = load_dataset(str(root), DatasetOptions(lazy_loading=True, ignore_pickle_file=True))
    report = validate_dataset(ds)
    assert 'TSV_EQUAL_ROWS' in report.codes()
