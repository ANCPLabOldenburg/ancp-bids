#!/usr/bin/env python3
"""Create a synthetic heavy BIDS dataset for performance / validation benchmarks.

Builds the dataset graph with ancpbids (create_dataset / create_artifact /
create_derivative) and writes it with save_dataset / write_derivative.

Default layout:
  subjects × sessions × (anat + func tasks/runs) [+ optional fmriprep-like derivatives]

Examples
--------
  uv run python tools/create_heavy_dataset.py /tmp/heavy_bids
  uv run python tools/create_heavy_dataset.py /tmp/heavy_bids --subjects 50 --no-derivatives
  uv run python tools/create_heavy_dataset.py /tmp/heavy_bids --preset medium
"""
from __future__ import annotations

import argparse
import os
import time
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, Optional, Sequence, Tuple

import ancpbids
from ancpbids import model_latest as schema
from ancpbids.model_base import File

PRESETS = {
    # ~2.6k raw files (no derivatives)
    "small": dict(
        subjects=25, sessions=1, runs=2, tasks=("rest",), acqs=("",), derivatives=False
    ),
    # ~10k files with derivatives (50-sub head-to-head size)
    "medium": dict(
        subjects=50,
        sessions=2,
        runs=4,
        tasks=("rest", "nback"),
        acqs=("", "highres"),
        derivatives=True,
    ),
    # ~21k files — default heavy tree used for ancpbids vs BV timing
    "heavy": dict(
        subjects=100,
        sessions=2,
        runs=4,
        tasks=("rest", "nback"),
        acqs=("", "highres"),
        derivatives=True,
    ),
    # ~83k files — large stress tree
    "xlarge": dict(
        subjects=400,
        sessions=2,
        runs=4,
        tasks=("rest", "nback"),
        acqs=("", "highres"),
        derivatives=True,
    ),
}

SPACES = ("MNI152NLin2009cAsym", "T1w")
ANAT_ACQS = ("", "mp2rage")


def _strip_entity_prefix(value: str, key: str) -> str:
    """Accept either ``highres`` or legacy ``acq-highres`` style values."""
    if not value:
        return ""
    prefix = f"{key}-"
    if value.startswith(prefix):
        return value[len(prefix) :]
    return value


def _write_bytes(blob: bytes) -> Callable[[str], None]:
    def _write(path: str, data: bytes = blob) -> None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_bytes(data)

    return _write


def _add_fixed_file(folder, name: str, content: Any) -> None:
    node = File(name=name)
    node.parent_object_ = folder
    node.content = content
    folder.files.append(node)


def _add_artifact(
    folder,
    *,
    suffix: str,
    extension: str,
    content: Any,
    **entities: Any,
) -> None:
    art = folder.create_artifact()
    art.suffix = suffix
    art.extension = extension
    art.add_entities(**{k: v for k, v in entities.items() if v not in (None, "")})
    art.content = content


def create_heavy_dataset(
    root: Path,
    *,
    subjects: int = 100,
    sessions: int = 2,
    runs: int = 4,
    tasks: Sequence[str] = ("rest", "nback"),
    acqs: Sequence[str] = ("", "highres"),
    derivatives: bool = True,
    bids_version: str = "1.10.1",
    blob: bytes = b"\0" * 64,
) -> Tuple[int, int]:
    """Create the synthetic dataset under ``root`` using ancpbids writers.

    Returns
    -------
    (n_files, n_dirs)
    """
    root = Path(root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    if any(root.iterdir()):
        raise ValueError(f"Destination is not empty: {root}")

    acqs = tuple(_strip_entity_prefix(a, "acq") for a in acqs)
    anat_acqs = tuple(_strip_entity_prefix(a, "acq") for a in ANAT_ACQS)

    write_blob = _write_bytes(blob)
    bold_meta = {
        "TaskName": "rest",
        "RepetitionTime": 2.0,
        "EchoTime": 0.03,
        "FlipAngle": 90,
        "SliceTiming": [i * 0.05 for i in range(40)],
    }
    t1_meta = {"RepetitionTime": 2.3, "EchoTime": 0.002, "FlipAngle": 9}
    events_rows = [
        {"onset": i * 2, "duration": 1, "trial_type": f"c{i % 3}"} for i in range(40)
    ]
    confounds_rows = [
        {"trans_x": 0.1, "trans_y": 0.2, "trans_z": 0.3} for _ in range(50)
    ]

    # base_dir.endswith(name) → files land directly under ``root`` (no extra nesting).
    ds = schema.create_dataset(str(root), name=root.name)
    ds.dataset_description.Name = "Heavy Synthetic"
    ds.dataset_description.BIDSVersion = bids_version
    ds.dataset_description.DatasetType = "raw"
    ds.dataset_description.content = {
        "Name": "Heavy Synthetic",
        "BIDSVersion": bids_version,
        "DatasetType": "raw",
    }

    participants_rows = [
        {
            "participant_id": f"sub-{s:04d}",
            "age": 20 + (s % 40),
            "sex": "M" if s % 2 else "F",
        }
        for s in range(subjects)
    ]
    _add_fixed_file(ds, "participants.tsv", participants_rows)
    _add_fixed_file(
        ds,
        "participants.json",
        {
            "age": {"Description": "age", "Units": "years"},
            "sex": {"Description": "sex"},
        },
    )

    n_files = 3  # dataset_description + participants.{tsv,json}
    for s in range(subjects):
        sub = ds.create_folder(name=f"sub-{s:04d}", type_=schema.Subject)
        for ses_i in range(sessions):
            ses = sub.create_folder(
                name=f"ses-{ses_i + 1:02d}", type_=schema.SessionFolder
            )
            anat = ses.create_folder(name="anat", type_=schema.DatatypeFolder)
            func = ses.create_folder(name="func", type_=schema.DatatypeFolder)

            for acq in anat_acqs:
                ents = {"acq": acq} if acq else {}
                _add_artifact(
                    anat, suffix="T1w", extension=".nii.gz", content=write_blob, **ents
                )
                _add_artifact(
                    anat, suffix="T1w", extension=".json", content=t1_meta, **ents
                )
                n_files += 2

            for task in tasks:
                for run in range(1, runs + 1):
                    for acq in acqs:
                        ents: Dict[str, Any] = {"task": task, "run": run}
                        if acq:
                            ents["acq"] = acq
                        _add_artifact(
                            func,
                            suffix="bold",
                            extension=".nii.gz",
                            content=write_blob,
                            **ents,
                        )
                        _add_artifact(
                            func,
                            suffix="bold",
                            extension=".json",
                            content=bold_meta,
                            **ents,
                        )
                        _add_artifact(
                            func,
                            suffix="events",
                            extension=".tsv",
                            content=events_rows,
                            **ents,
                        )
                        n_files += 3

    if derivatives:
        deriv = ds.create_derivative(name="fmriprep")
        deriv.dataset_description.Name = "fMRIPrep - synthetic"
        deriv.dataset_description.BIDSVersion = bids_version
        deriv.dataset_description.DatasetType = "derivative"
        deriv.dataset_description.GeneratedBy.Name = "fmriprep"
        deriv.dataset_description.GeneratedBy.Version = "23.1.0"
        deriv.dataset_description.content = {
            "Name": "fMRIPrep - synthetic",
            "BIDSVersion": bids_version,
            "DatasetType": "derivative",
            "GeneratedBy": [{"Name": "fmriprep", "Version": "23.1.0"}],
        }
        n_files += 1

        for s in range(subjects):
            sub = deriv.create_folder(name=f"sub-{s:04d}", type_=schema.Subject)
            for ses_i in range(sessions):
                ses = sub.create_folder(
                    name=f"ses-{ses_i + 1:02d}", type_=schema.SessionFolder
                )
                anat = ses.create_folder(name="anat", type_=schema.DatatypeFolder)
                func = ses.create_folder(name="func", type_=schema.DatatypeFolder)

                for space in SPACES:
                    ents = {"space": space, "desc": "preproc"}
                    _add_artifact(
                        anat, suffix="T1w", extension=".nii.gz", content=write_blob, **ents
                    )
                    _add_artifact(
                        anat, suffix="T1w", extension=".json", content=t1_meta, **ents
                    )
                    n_files += 2

                for task in tasks:
                    for run in range(1, runs + 1):
                        for space in SPACES:
                            ents = {
                                "task": task,
                                "run": run,
                                "space": space,
                                "desc": "preproc",
                            }
                            _add_artifact(
                                func,
                                suffix="bold",
                                extension=".nii.gz",
                                content=write_blob,
                                **ents,
                            )
                            _add_artifact(
                                func,
                                suffix="bold",
                                extension=".json",
                                content=bold_meta,
                                **ents,
                            )
                            n_files += 2
                        conf_ents = {"task": task, "run": run, "desc": "confounds"}
                        _add_artifact(
                            func,
                            suffix="timeseries",
                            extension=".tsv",
                            content=confounds_rows,
                            **conf_ents,
                        )
                        _add_artifact(
                            func,
                            suffix="timeseries",
                            extension=".json",
                            content={},
                            **conf_ents,
                        )
                        n_files += 2

    ancpbids.save_dataset(ds, str(root))
    n_dirs = sum(len(dirs) for _, dirs, _ in os.walk(root))
    return n_files, n_dirs


def _parse_csv(value: str) -> Tuple[str, ...]:
    parts = tuple(p.strip() for p in value.split(",") if p.strip())
    if not parts:
        raise argparse.ArgumentTypeError("expected at least one comma-separated value")
    return parts


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "output",
        type=Path,
        help="Destination directory (created if missing; must be empty)",
    )
    parser.add_argument(
        "--preset",
        choices=sorted(PRESETS),
        default="heavy",
        help="Named size profile (default: heavy)",
    )
    parser.add_argument("--subjects", type=int, help="Override number of subjects")
    parser.add_argument("--sessions", type=int, help="Override number of sessions")
    parser.add_argument("--runs", type=int, help="Override runs per task")
    parser.add_argument(
        "--tasks",
        type=_parse_csv,
        help="Comma-separated task names (default from preset)",
    )
    parser.add_argument(
        "--acqs",
        type=_parse_csv,
        help='Comma-separated acq values (e.g. highres); "" for no acq',
    )
    deriv_group = parser.add_mutually_exclusive_group()
    deriv_group.add_argument(
        "--derivatives",
        dest="derivatives",
        action="store_true",
        default=None,
        help="Include fmriprep-like derivatives (overrides preset)",
    )
    deriv_group.add_argument(
        "--no-derivatives",
        dest="derivatives",
        action="store_false",
        help="Skip derivatives (overrides preset)",
    )
    parser.add_argument(
        "--bids-version",
        default="1.10.1",
        help="BIDSVersion written to dataset_description.json (default: 1.10.1)",
    )
    return parser


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    cfg = dict(PRESETS[args.preset])
    if args.subjects is not None:
        cfg["subjects"] = args.subjects
    if args.sessions is not None:
        cfg["sessions"] = args.sessions
    if args.runs is not None:
        cfg["runs"] = args.runs
    if args.tasks is not None:
        cfg["tasks"] = args.tasks
    if args.acqs is not None:
        cfg["acqs"] = tuple("" if a in {"", '""', "''"} else a for a in args.acqs)
    if args.derivatives is not None:
        cfg["derivatives"] = args.derivatives

    t0 = time.perf_counter()
    n_files, n_dirs = create_heavy_dataset(
        args.output,
        subjects=cfg["subjects"],
        sessions=cfg["sessions"],
        runs=cfg["runs"],
        tasks=cfg["tasks"],
        acqs=cfg["acqs"],
        derivatives=cfg["derivatives"],
        bids_version=args.bids_version,
    )
    elapsed = time.perf_counter() - t0
    print(
        f"created {args.output} in {elapsed:.2f}s "
        f"(preset={args.preset}, subjects={cfg['subjects']}, "
        f"sessions={cfg['sessions']}, files≈{n_files}, dirs≈{n_dirs}, "
        f"derivatives={cfg['derivatives']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
