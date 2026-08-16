import gzip
import os
import struct
import tempfile

import pytest

from ancpbids import load_dataset, validate_dataset, DatasetOptions
from ancpbids.schema.headers import parse_gzip, parse_nifti_header, axis_codes
from ancpbids.schema.validate import _value_matches, _load_binary_headers
from ..base_test_case import DS005_DIR


def _write_minimal_nifti_gz(path):
    raw = bytearray(348)
    struct.pack_into('<i', raw, 0, 348)
    struct.pack_into('<8h', raw, 40, 3, 4, 4, 4, 1, 1, 1, 1)
    struct.pack_into('<8f', raw, 76, 1.0, 2.0, 2.0, 2.0, 1.0, 1.0, 1.0, 1.0)
    struct.pack_into('<B', raw, 123, 10)
    struct.pack_into('<h', raw, 252, 1)
    struct.pack_into('<h', raw, 254, 1)
    struct.pack_into('<4f', raw, 280, 1, 0, 0, 0)
    struct.pack_into('<4f', raw, 296, 0, 1, 0, 0)
    struct.pack_into('<4f', raw, 312, 0, 0, 1, 0)
    raw[344:348] = b'n+1\x00'
    with gzip.open(path, 'wb') as handle:
        handle.write(raw)


def test_parse_gzip_minimal():
    with tempfile.NamedTemporaryFile(suffix='.gz', delete=False) as handle:
        handle.write(b'\x1f\x8b\x08\x00\x01\x00\x00\x00\x00\x03')
        path = handle.name
    try:
        result = parse_gzip(path)
        assert result is not None
        assert result['timestamp'] == 1
    finally:
        os.unlink(path)


def test_parse_nifti_header_synthetic():
    path = tempfile.mktemp(suffix='.nii.gz')
    try:
        _write_minimal_nifti_gz(path)
        header = parse_nifti_header(path)
        assert header is not None
        assert header['shape'] == [4, 4, 4]
        assert header['axis_codes'] == ['R', 'A', 'S']
        gzip_meta = parse_gzip(path)
        assert gzip_meta is not None
    finally:
        os.unlink(path)


def test_parse_nifti_fallback_without_nibabel(monkeypatch):
    import ancpbids.schema.headers as headers

    monkeypatch.setattr(headers, 'nib', None)
    path = tempfile.mktemp(suffix='.nii.gz')
    try:
        _write_minimal_nifti_gz(path)
        header = headers.parse_nifti_header(path)
        assert header is not None
        assert header['shape'] == [4, 4, 4]
    finally:
        os.unlink(path)


def test_axis_codes_identity():
    affine = [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ]
    assert axis_codes(affine) == ['R', 'A', 'S']


def test_value_matches_constraints():
    assert _value_matches(3, {'type': 'integer', 'minimum': 1, 'maximum': 5})
    assert not _value_matches(0, {'type': 'integer', 'minimum': 1})
    assert _value_matches('abc', {'type': 'string', 'pattern': '[a-z]+'})
    assert not _value_matches('A', {'type': 'string', 'pattern': '[a-z]+'})
    assert _value_matches(
        [1, 2],
        {'type': 'array', 'minItems': 2, 'maxItems': 2, 'items': {'type': 'integer'}})


def test_load_binary_headers_into_context():
    path = tempfile.mktemp(suffix='_bold.nii.gz')
    try:
        _write_minimal_nifti_gz(path)

        class _File:
            name = os.path.basename(path)
            extension = '.nii.gz'

            def get_absolute_path(self):
                return path

        ctx = {}
        _load_binary_headers(_File(), ctx)
        assert ctx['nifti_header']['shape'] == [4, 4, 4]
        assert ctx['gzip'] is not None
    finally:
        os.unlink(path)


@pytest.mark.parametrize('lazy_loading', [True, False])
def test_validation_subject_context(lazy_loading):
    dataset = load_dataset(DS005_DIR, DatasetOptions(lazy_loading=lazy_loading))
    report = validate_dataset(dataset)
    session = report._schema_session
    events = None
    for file in session.iter_files():
        if getattr(file, 'suffix', None) == 'events':
            events = file
            break
    assert events is not None
    ctx = session.context(events, rich=True)
    assert ctx['subject'] is not None
    assert 'ses_dirs' in ctx['subject']['sessions']
    assert report.has_errors()
