"""Binary header readers for schema validation context.

NIfTI headers prefer nibabel when installed; otherwise a stdlib fallback is used.
GZIP/TIFF/OME parsing is stdlib-only.

Adapted from the BIDS Validator (https://github.com/bids-standard/bids-validator),
especially ``src/files/nifti.ts`` (``loadHeader``, ``axisCodes``), ``gzip.ts``, and
``tiff.ts``. The context field shapes, pixdim rounding, ``dim_info`` /
``xyzt_units`` unpacking, and nearest-axis ``axis_codes`` logic follow that
implementation. ``axisCodes`` there is itself an extract of
``transforms3d.affines.decompose44``
(https://github.com/matthew-brett/transforms3d).

Copyright (c) BIDS Validator contributors; used under the MIT license.
"""
import gzip as gzip_mod
import struct
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional, Tuple

try:
    import nibabel as nib
except ImportError:  # pragma: no cover - optional dependency
    nib = None


def parse_gzip(path: str, max_bytes: int = 1024) -> Optional[Dict[str, Any]]:
    try:
        with open(path, 'rb') as handle:
            buf = handle.read(max_bytes)
    except OSError:
        return None
    if len(buf) < 10 or buf[0] != 0x1F or buf[1] != 0x8B:
        return None
    flags = buf[3]
    timestamp = struct.unpack_from('<I', buf, 4)[0]
    offset = 10
    if flags & 0x04:
        if offset + 2 > len(buf):
            return {'timestamp': timestamp, 'filename': '', 'comment': ''}
        xlen = struct.unpack_from('<H', buf, offset)[0]
        offset += 2 + xlen
    filename = ''
    if flags & 0x08:
        filename, offset = _c_string(buf, offset)
    comment = ''
    if flags & 0x10:
        comment, offset = _c_string(buf, offset)
    return {'timestamp': timestamp, 'filename': filename, 'comment': comment}


def parse_nifti_header(path: str) -> Optional[Dict[str, Any]]:
    if nib is not None:
        header = _parse_nifti_nibabel(path)
        if header is not None:
            return header
    return _parse_nifti_fallback(path)


def _parse_nifti_nibabel(path: str) -> Optional[Dict[str, Any]]:
    try:
        image = nib.load(path)
        hdr = image.header
        affine = image.affine
    except Exception:
        return None
    dims = [int(v) for v in list(hdr['dim'])]
    pixdims = [round(float(v) * 1000) / 1000 for v in list(hdr['pixdim'])]
    ndim = max(0, min(int(dims[0]), 7))
    xyzt = int(hdr['xyzt_units'])
    dim_info = int(hdr['dim_info'])
    affine_rows = affine.tolist() if hasattr(affine, 'tolist') else list(affine)
    if len(affine_rows) == 3:
        affine_rows = affine_rows + [[0.0, 0.0, 0.0, 1.0]]
    return {
        'dim': dims,
        'pixdim': pixdims,
        'shape': dims[1:ndim + 1],
        'voxel_sizes': pixdims[1:ndim + 1],
        'dim_info': {
            'freq': dim_info & 0x03,
            'phase': (dim_info >> 2) & 0x03,
            'slice': (dim_info >> 4) & 0x03,
        },
        'xyzt_units': {
            'xyz': ['unknown', 'meter', 'mm', 'um'][xyzt & 0x03],
            't': ['unknown', 'sec', 'msec', 'usec'][(xyzt >> 3) & 0x03],
        },
        'qform_code': int(hdr['qform_code']),
        'sform_code': int(hdr['sform_code']),
        'axis_codes': axis_codes(affine_rows),
    }


def _parse_nifti_fallback(path: str) -> Optional[Dict[str, Any]]:
    try:
        raw = _read_nifti_bytes(path)
        if raw is None or len(raw) < 348:
            return None
        return _parse_nifti_buffer(raw)
    except (OSError, ValueError, struct.error):
        return None


def parse_tiff(path: str, ome: bool = False) -> Tuple[Optional[Dict], Optional[Dict]]:
    try:
        with open(path, 'rb') as handle:
            buf = handle.read(4096)
    except OSError:
        return None, None
    if len(buf) < 8:
        return None, None
    magic = struct.unpack_from('<H', buf, 0)[0]
    little = magic == 0x4949
    if not little and magic != 0x4D4D:
        return None, None
    endian = '<' if little else '>'
    version = struct.unpack_from(endian + 'H', buf, 2)[0]
    tiff = {'version': version}
    if not ome:
        return tiff, None
    description = _tiff_image_description(buf, endian, 12 if version == 42 else 20)
    ome_meta = _parse_ome_xml(description) if description else None
    return tiff, ome_meta


def _c_string(buf: bytes, offset: int) -> Tuple[str, int]:
    end = buf.find(b'\x00', offset)
    if end < 0:
        return '', len(buf)
    return buf[offset:end].decode('utf-8', errors='replace'), end + 1


def _read_nifti_bytes(path: str) -> Optional[bytes]:
    with open(path, 'rb') as handle:
        head = handle.read(2)
        handle.seek(0)
        if head == b'\x1f\x8b':
            with gzip_mod.open(path, 'rb') as gz:
                return gz.read(540)
        return handle.read(540)


def _parse_nifti_buffer(raw: bytes) -> Dict[str, Any]:
    for endian in ('<', '>'):
        sizeof = struct.unpack_from(endian + 'i', raw, 0)[0]
        if sizeof == 348 and len(raw) >= 348:
            return _nifti1(raw, endian)
        if sizeof == 540 and len(raw) >= 540:
            return _nifti2(raw, endian)
    magic = raw[344:348] if len(raw) >= 348 else b''
    if magic in (b'n+1\x00', b'ni1\x00'):
        return _nifti1(raw, '<')
    raise ValueError('unreadable nifti header')


def _nifti1(raw: bytes, endian: str) -> Dict[str, Any]:
    dims = list(struct.unpack_from(endian + '8h', raw, 40))
    pixdims = [round(v * 1000) / 1000 for v in struct.unpack_from(endian + '8f', raw, 76)]
    xyzt_units = struct.unpack_from(endian + 'B', raw, 123)[0]
    dim_info = struct.unpack_from(endian + 'B', raw, 39)[0]
    qform = struct.unpack_from(endian + 'h', raw, 252)[0]
    sform = struct.unpack_from(endian + 'h', raw, 254)[0]
    srow = [
        list(struct.unpack_from(endian + '4f', raw, 280)),
        list(struct.unpack_from(endian + '4f', raw, 296)),
        list(struct.unpack_from(endian + '4f', raw, 312)),
        [0.0, 0.0, 0.0, 1.0],
    ]
    ndim = max(0, min(int(dims[0]), 7))
    return {
        'dim': dims,
        'pixdim': pixdims,
        'shape': dims[1:ndim + 1],
        'voxel_sizes': pixdims[1:ndim + 1],
        'dim_info': {
            'freq': dim_info & 0x03,
            'phase': (dim_info >> 2) & 0x03,
            'slice': (dim_info >> 4) & 0x03,
        },
        'xyzt_units': {
            'xyz': ['unknown', 'meter', 'mm', 'um'][xyzt_units & 0x03],
            't': ['unknown', 'sec', 'msec', 'usec'][(xyzt_units >> 3) & 0x03],
        },
        'qform_code': int(qform),
        'sform_code': int(sform),
        'axis_codes': axis_codes(srow),
    }


def _nifti2(raw: bytes, endian: str) -> Dict[str, Any]:
    dims = [int(v) for v in struct.unpack_from(endian + '8q', raw, 16)]
    pixdims = [round(v * 1000) / 1000 for v in struct.unpack_from(endian + '8d', raw, 104)]
    xyzt_units = struct.unpack_from(endian + 'i', raw, 344)[0]
    qform = struct.unpack_from(endian + 'i', raw, 344)[0]
    sform = struct.unpack_from(endian + 'i', raw, 348)[0]
    srow = [
        list(struct.unpack_from(endian + '4d', raw, 364)),
        list(struct.unpack_from(endian + '4d', raw, 396)),
        list(struct.unpack_from(endian + '4d', raw, 428)),
        [0.0, 0.0, 0.0, 1.0],
    ]
    ndim = max(0, min(dims[0], 7))
    return {
        'dim': dims,
        'pixdim': pixdims,
        'shape': dims[1:ndim + 1],
        'voxel_sizes': pixdims[1:ndim + 1],
        'dim_info': {'freq': 0, 'phase': 0, 'slice': 0},
        'xyzt_units': {
            'xyz': ['unknown', 'meter', 'mm', 'um'][xyzt_units & 0x03],
            't': ['unknown', 'sec', 'msec', 'usec'][(xyzt_units >> 3) & 0x03],
        },
        'qform_code': qform,
        'sform_code': sform,
        'axis_codes': axis_codes(srow),
    }


def axis_codes(affine: List[List[float]]) -> Optional[List[str]]:
    if any(not _finite(v) for row in affine[:3] for v in row[:3]):
        return None
    cos_x = [affine[0][0], affine[1][0], affine[2][0]]
    cos_y = [affine[0][1], affine[1][1], affine[2][1]]
    cos_z = [affine[0][2], affine[1][2], affine[2][2]]
    orth_x = _norm(cos_x)
    orth_y = _norm(_sub(cos_y, _scale(orth_x, _dot(orth_x, cos_y))))
    orth_z = _norm(_sub(
        cos_z,
        _add(_scale(orth_x, _dot(orth_x, cos_z)), _scale(orth_y, _dot(orth_y, cos_z))),
    ))
    basis = [orth_x, orth_y, orth_z]
    magnitudes = [[abs(v) for v in row] for row in basis]
    max_mags = [max(row) for row in magnitudes]
    dims = sorted(range(3), key=lambda i: max_mags[i], reverse=True)
    codes = ['RL', 'AP', 'SI']
    result = ['', '', '']
    for dim in dims:
        idx = max(range(3), key=lambda i: magnitudes[dim][i])
        for row in magnitudes:
            row[idx] = 0
        result[dim] = codes[idx][0 if basis[dim][idx] > 0 else 1]
    return result


def _finite(value: float) -> bool:
    return value == value and value not in (float('inf'), float('-inf'))


def _dot(a: List[float], b: List[float]) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def _scale(vec: List[float], scalar: float) -> List[float]:
    return [v * scalar for v in vec]


def _add(a: List[float], b: List[float]) -> List[float]:
    return [a[i] + b[i] for i in range(3)]


def _sub(a: List[float], b: List[float]) -> List[float]:
    return [a[i] - b[i] for i in range(3)]


def _norm(vec: List[float]) -> List[float]:
    length = _dot(vec, vec) ** 0.5
    if length == 0:
        return [0.0, 0.0, 0.0]
    return _scale(vec, 1.0 / length)


def _tiff_image_description(buf: bytes, endian: str, ifd_size: int) -> Optional[str]:
    ifd_offset = struct.unpack_from(endian + 'I', buf, 4)[0]
    if ifd_offset + 2 > len(buf):
        return None
    count = struct.unpack_from(endian + 'H', buf, ifd_offset)[0]
    for i in range(count):
        entry = ifd_offset + 2 + i * ifd_size
        if entry + ifd_size > len(buf):
            break
        tag = struct.unpack_from(endian + 'H', buf, entry)[0]
        if tag != 0x010E:
            continue
        nbytes = struct.unpack_from(endian + 'I', buf, entry + 4)[0]
        value_or_offset = struct.unpack_from(endian + 'I', buf, entry + 8)[0]
        if nbytes <= 4:
            raw = struct.pack(endian + 'I', value_or_offset)[:nbytes]
            return raw.decode('utf-8', errors='replace').rstrip('\x00')
        if value_or_offset + nbytes > len(buf):
            return None
        return buf[value_or_offset:value_or_offset + nbytes].decode('utf-8', errors='replace')
    return None


def _parse_ome_xml(text: str) -> Optional[Dict[str, Any]]:
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        return None
    pixels = None
    for node in root.iter():
        if node.tag.endswith('Pixels'):
            pixels = node
            break
    if pixels is None:
        return None

    def attr(name):
        for key, value in pixels.attrib.items():
            if key == name or key.endswith('}' + name):
                return value
        return None

    result = {}
    for key in (
        'PhysicalSizeX', 'PhysicalSizeY', 'PhysicalSizeZ',
        'PhysicalSizeXUnit', 'PhysicalSizeYUnit', 'PhysicalSizeZUnit',
    ):
        value = attr(key)
        if value is None:
            continue
        if key.endswith('Unit'):
            result[key] = value
            continue
        try:
            result[key] = float(value)
        except ValueError:
            result[key] = value
    return result or None
