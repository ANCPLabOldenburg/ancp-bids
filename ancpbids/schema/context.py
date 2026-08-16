"""Build schema validation context (sidecar, columns, associations, headers)."""
import gzip as gzip_mod
import os

from ancpbids.model_base import Artifact, DatatypeFolder, DerivativeFolder, Subject

from .headers import parse_gzip, parse_nifti_header, parse_tiff
from .session import queue_issue, selectors_match
from .values import relpath, schema_path


def build_context(session, file, rich=False):
    file_id = id(file)
    if rich:
        cached = session._contexts.get((file_id, True))
        if cached is not None:
            return cached
        ctx = dict(basic_context(file, session))
        ctx['subject'] = session.subject_context(file)
        ctx['sidecar'] = sidecar(file)
        ctx['json'] = load_json(file)
        ctx['associations'] = associations(file, session, ctx)
        ctx['columns'] = load_columns(file, session, ctx)
        ctx['size'] = file_size(file)
        load_binary_headers(file, ctx, session)
        session._contexts[(file_id, True)] = ctx
        session._contexts[(file_id, False)] = ctx
        return ctx

    cached = session._contexts.get((file_id, False))
    if cached is not None:
        return cached
    cached = session._contexts.get((file_id, True))
    if cached is not None:
        return cached
    ctx = basic_context(file, session)
    session._contexts[(file_id, False)] = ctx
    return ctx


def json_contents(file):
    if file is None:
        return {}
    value = getattr(file, 'contents', None)
    if value is None and hasattr(file, 'load_contents'):
        value = file.load_contents()
    return value if isinstance(value, dict) else {}


def load_json(file):
    if file is None or not file.name.endswith('.json'):
        return None
    return json_contents(file)


def load_columns(file, session=None, ctx=None):
    if file is None:
        return None
    extension = getattr(file, 'extension', None) or ''
    suffix = getattr(file, 'suffix', None)
    if extension == '.tsv.gz' or (extension == '.tsv' and suffix == 'motion'):
        return load_headerless_columns(file, session, ctx)
    if not file.name.endswith('.tsv'):
        return None
    rows = getattr(file, 'contents', None)
    if rows is None and hasattr(file, 'load_contents'):
        rows = file.load_contents()
    if not isinstance(rows, list):
        return load_tsv_from_disk(file, session)
    if not rows:
        return {}
    if not isinstance(rows[0], dict):
        return {}
    headers = list(rows[0])
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            tsv_issue(session, file, 'TSV_EQUAL_ROWS', index + 2)
            return {key: [] for key in headers}
        if any(row.get(key) is None for key in headers):
            tsv_issue(session, file, 'TSV_EQUAL_ROWS', index + 2)
            return {
                key: [r.get(key) for r in rows[:index] if isinstance(r, dict)]
                for key in headers
            }
    return {key: [row.get(key) for row in rows] for key in headers}


def load_headerless_columns(file, session, ctx):
    ctx = ctx or {}
    extension = getattr(file, 'extension', None) or ''
    compressed = extension == '.tsv.gz'
    if compressed:
        headers = (ctx.get('sidecar') or {}).get('Columns')
    else:
        channels = (ctx.get('associations') or {}).get('channels') or {}
        headers = channels.get('name')
    if not headers:
        return None
    size = file_size(file)
    if size == 0:
        return None
    try:
        lines = read_text_lines(file.get_absolute_path(), gzipped=compressed)
    except OSError:
        if compressed and session is not None:
            queue_issue(session, 'error', 'Invalid gzip', file, 'INVALID_GZIP')
        return {}
    return columns_from_lines(headers, lines, file, session, start_line=1)


def load_tsv_from_disk(file, session):
    try:
        lines = read_text_lines(file.get_absolute_path(), gzipped=False)
    except OSError:
        return {}
    if not lines:
        return {}
    headers = lines[0].split('\t')
    if len(headers) != len(set(headers)):
        tsv_issue(session, file, 'TSV_COLUMN_HEADER_DUPLICATE', 1)
    return columns_from_lines(headers, lines[1:], file, session, start_line=2)


def read_text_lines(path, gzipped=False):
    opener = gzip_mod.open if gzipped else open
    with opener(path, 'rt', encoding='utf-8', newline='') as handle:
        text = handle.read()
    if not text:
        return []
    return text.splitlines()


def columns_from_lines(headers, lines, file, session, start_line=1):
    columns = {header: [] for header in headers}
    for offset, line in enumerate(lines):
        line_no = start_line + offset
        if line == '':
            if offset + 1 == len(lines):
                break
            tsv_issue(session, file, 'TSV_EMPTY_LINE', line_no)
            return {header: [] for header in headers}
        values = line.split('\t')
        if len(values) != len(headers):
            tsv_issue(session, file, 'TSV_EQUAL_ROWS', line_no)
            return {header: columns[header] for header in headers}
        for header, value in zip(headers, values):
            columns[header].append(value)
    return columns


def tsv_issue(session, file, code, line):
    if session is None:
        return
    queue_issue(
        session,
        'error',
        "%s at line %s in '%s'" % (code, line, relpath(file)),
        file,
        code)


def sidecar(file):
    if not isinstance(file, Artifact):
        return {}
    try:
        return file.get_metadata() or {}
    except Exception:
        return {}


def file_size(file):
    try:
        return os.path.getsize(file.get_absolute_path())
    except OSError:
        return None


def modalities_for(datatypes, document):
    found = []
    for name, spec in (document['rules'].get('modalities') or {}).items():
        if any(dt in datatypes for dt in spec.get('datatypes') or ()):
            found.append(name)
    return found


def basic_context(file, session):
    entities = {}
    if isinstance(file, Artifact):
        for key, value in file.entities.items():
            entities[session.entity_long.get(key, key)] = value
    description = local_dataset_description(file, session.dataset_description)
    dataset_ctx = dict(session.dataset_ctx)
    dataset_ctx['dataset_description'] = description
    return {
        'path': schema_path(file),
        'suffix': getattr(file, 'suffix', None),
        'extension': file.extension,
        'datatype': datatype(file),
        'modality': modality(datatype(file), session.document),
        'entities': entities,
        'subject': None,
        'sidecar': {},
        'json': None,
        'columns': None,
        'associations': {},
        'nifti_header': None,
        'gzip': None,
        'ome': None,
        'tiff': None,
        'dataset': dataset_ctx,
        'schema': session.document,
        'size': None,
        '_files': session.files_index,
    }


def ancestor_subject(file):
    current = file
    while current is not None:
        if isinstance(current, Subject):
            return current
        current = getattr(current, 'parent_object_', None)
    return None


def load_binary_headers(file, ctx, session=None):
    path = file.get_absolute_path()
    extension = file.extension or ''
    if extension.endswith('.gz'):
        ctx['gzip'] = parse_gzip(path)
    if extension.startswith('.nii'):
        header = parse_nifti_header(path)
        ctx['nifti_header'] = header
        if header is not None and header.get('axis_codes') is None and session is not None:
            queue_issue(
                session,
                'error',
                "Ambiguous affine in '%s'" % relpath(file),
                file,
                'AMBIGUOUS_AFFINE')
    if extension.endswith('.tif') or extension.endswith('.btf') or '.ome.tif' in file.name:
        ome = extension.startswith('.ome') or '.ome.' in file.name
        tiff, ome_meta = parse_tiff(path, ome=ome)
        ctx['tiff'] = tiff
        ctx['ome'] = ome_meta


def local_dataset_description(file, root_description):
    current = file
    while current is not None:
        if isinstance(current, DerivativeFolder):
            contents = json_contents(current.dataset_description)
            return contents or {'DatasetType': 'derivative'}
        current = getattr(current, 'parent_object_', None)
    return root_description


def datatype(file):
    value = getattr(file, 'datatype', None)
    if value:
        return value
    current = file.get_parent()
    while current is not None:
        if isinstance(current, DatatypeFolder):
            return current.name
        current = current.get_parent()
    return None


def modality(datatype_name, document):
    if not datatype_name:
        return None
    for name, spec in (document['rules'].get('modalities') or {}).items():
        if datatype_name in (spec.get('datatypes') or ()):
            return name
    return None


def associations(file, session, ctx):
    result = {}
    for name, rule in (session.document.get('meta', {}).get('associations') or {}).items():
        if not selectors_match(rule.get('selectors'), ctx):
            result[name] = None
            continue
        found = find_associated(file, rule.get('target') or {}, rule.get('inherit', False), session)
        result[name] = association_context(found, name, session)
    return result


def find_associated(file, target, inherit, session):
    suffix = target.get('suffix')
    extensions = target.get('extension')
    if isinstance(extensions, str):
        extensions = [extensions]
    allowed_extra = []
    for entity in target.get('entities') or []:
        allowed_extra.append(session.entity_short.get(entity, entity))
    multi = bool(allowed_extra)
    current = file.get_parent()
    while current is not None:
        matches = associated_in_folder(
            file, current, suffix, extensions, allowed_extra)
        if matches:
            if multi:
                return matches
            if len(matches) == 1:
                return matches[0]
            exact = exact_associated(file, matches, allowed_extra)
            if exact is not None:
                return exact
            paths = sorted(schema_path(item) for item in matches)
            queue_issue(
                session,
                'error',
                "Multiple inheritable files for '%s': %s" % (relpath(file), paths),
                matches[0],
                'MULTIPLE_INHERITABLE_FILES')
            return None
        if not inherit:
            return None
        current = current.get_parent()
    return None


def associated_in_folder(file, folder, suffix, extensions, allowed_extra):
    file_ents = file.get_entities() if isinstance(file, Artifact) else {}
    matches = []
    for candidate in folder.files or []:
        if candidate is file:
            continue
        if suffix and getattr(candidate, 'suffix', None) != suffix:
            continue
        if extensions and candidate.extension not in extensions:
            continue
        if isinstance(candidate, Artifact) and file_ents:
            cand_ents = candidate.get_entities()
            compatible = True
            for key, value in cand_ents.items():
                if key in file_ents:
                    if str(file_ents[key]) != str(value):
                        compatible = False
                        break
                elif key not in allowed_extra:
                    compatible = False
                    break
            if not compatible:
                continue
        matches.append(candidate)
    return matches


def exact_associated(file, matches, allowed_extra):
    file_ents = file.get_entities() if isinstance(file, Artifact) else {}
    needed = list(file_ents) + list(allowed_extra)
    for candidate in matches:
        if not isinstance(candidate, Artifact):
            continue
        cand_ents = candidate.get_entities()
        if all(cand_ents.get(key) == file_ents.get(key) for key in needed):
            return candidate
    return None


def association_context(found, name, session):
    if name == 'coordsystems':
        files = found if isinstance(found, list) else ([found] if found else [])
        return coordsystems_context(files)
    if found is None:
        return None
    if isinstance(found, list):
        found = found[0] if found else None
    if found is None:
        return None
    path = schema_path(found)
    if name == 'physio':
        return {'path': path, 'sidecar': sidecar(found)}
    name_on_disk = found.name
    if name_on_disk.endswith('.bval') or name_on_disk.endswith('.bvec'):
        return bval_bvec_context(found, path)
    if isinstance(found, Artifact) and found.extension == '.json':
        return {'path': path}
    ctx = {'path': path, 'n_rows': None}
    columns = load_columns(found, session, {'sidecar': sidecar(found), 'associations': {}})
    if columns:
        ctx['n_rows'] = len(next(iter(columns.values())))
        ctx.update(columns)
    if getattr(found, 'suffix', None) == 'events':
        ctx['sidecar'] = sidecar(found)
    return ctx


def coordsystems_context(files):
    if not files:
        return None
    paths = []
    spaces = []
    parents = []
    for item in files:
        paths.append(schema_path(item))
        ents = item.get_entities() if isinstance(item, Artifact) else {}
        spaces.append(ents.get('space'))
        contents = json_contents(item)
        parent = contents.get('ParentCoordinateSystem')
        if parent:
            parents.append(parent)
    return {
        'paths': paths,
        'spaces': spaces,
        'ParentCoordinateSystems': parents,
    }


def bval_bvec_context(file, path):
    try:
        text = open(file.get_absolute_path(), 'r', encoding='utf-8').read()
    except OSError:
        return {'path': path, 'n_cols': 0, 'n_rows': 0, 'values': []}
    rows = [line.split() for line in text.strip().splitlines() if line.strip()]
    if not rows:
        return {'path': path, 'n_cols': 0, 'n_rows': 0, 'values': []}
    values = []
    for item in rows[0]:
        try:
            values.append(float(item))
        except ValueError:
            values.append(item)
    return {
        'path': path,
        'n_cols': len(rows[0]),
        'n_rows': len(rows),
        'values': values,
    }
