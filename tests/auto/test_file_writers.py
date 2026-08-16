import os
import tempfile

import pandas as pd

from ancpbids import model_latest as schema
from ancpbids.plugins.plugin_files_handlers import write_tsv
from ancpbids.utils import load_contents, write_contents


def test_write_tsv_list_of_dicts(tmp_path):
    path = tmp_path / "participants.tsv"
    rows = [
        {"participant_id": "sub-01", "age": 25, "sex": "F"},
        {"participant_id": "sub-02", "age": 30, "sex": "M"},
    ]
    write_tsv(str(path), rows)
    loaded = load_contents(str(path))
    assert loaded == [
        {"participant_id": "sub-01", "age": "25", "sex": "F"},
        {"participant_id": "sub-02", "age": "30", "sex": "M"},
    ]


def test_write_tsv_dataframe(tmp_path):
    path = tmp_path / "events.tsv"
    df = pd.DataFrame({"onset": [0, 2], "duration": [1, 1], "trial_type": ["a", "b"]})
    write_tsv(str(path), df)
    text = path.read_text()
    assert text.splitlines()[0] == "onset\tduration\ttrial_type"
    assert "0\t1\ta" in text


def test_write_tsv_string(tmp_path):
    path = tmp_path / "plain.tsv"
    write_tsv(str(path), "col_a\tcol_b\n1\t2")
    assert path.read_text() == "col_a\tcol_b\n1\t2\n"


def test_write_contents_dispatches_tsv(tmp_path):
    path = tmp_path / "rows.tsv"
    write_contents(str(path), [{"a": 1, "b": 2}])
    assert path.read_text().startswith("a\tb\n")


def test_artifact_content_list_writes_tsv():
    output_dir = tempfile.mkdtemp()
    ds = schema.create_dataset(output_dir, name="tsv-ds")
    sub = ds.create_folder(name="sub-01", type_=schema.Subject)
    func = sub.create_folder(name="func", type_=schema.DatatypeFolder)
    events = func.create_artifact()
    events.suffix = "events"
    events.extension = ".tsv"
    events.add_entities(task="rest")
    events.content = [{"onset": 0, "duration": 1, "trial_type": "go"}]

    path = events.write()
    assert os.path.exists(path)
    assert path.endswith("_task-rest_events.tsv")
    assert load_contents(path) == [
        {"onset": "0", "duration": "1", "trial_type": "go"}
    ]


def test_artifact_content_string_writes_txt():
    output_dir = tempfile.mkdtemp()
    ds = schema.create_dataset(output_dir, name="txt-ds")
    sub = ds.create_folder(name="sub-01", type_=schema.Subject)
    note = sub.create_artifact()
    note.suffix = "textual"
    note.extension = ".txt"
    note.content = "hello from content"

    path = note.write()
    assert open(path).read() == "hello from content"
