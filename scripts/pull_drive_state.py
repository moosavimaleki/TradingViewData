#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Dict, Iterable, List


def _run(cmd: List[str], *, check: bool = True) -> int:
    print("+", " ".join(cmd), flush=True)
    proc = subprocess.run(cmd, check=False)
    if check and proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, cmd)
    return proc.returncode


def _load_manifest(path: Path) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _remote_join(remote_root: str, rel: str) -> str:
    root = remote_root.rstrip("/")
    if not rel or rel == ".":
        return root
    rel_norm = rel.replace("\\", "/").strip("/")
    return f"{root}/{rel_norm}"


def _iter_manifest_files(local_dir: Path) -> Iterable[Path]:
    for p in sorted(local_dir.rglob("manifest.json")):
        if p.is_file():
            yield p


def main() -> None:
    parser = argparse.ArgumentParser(description="Pull only manifests + latest chunk files from rclone remote.")
    parser.add_argument("--remote", default="gdrive:", help="rclone remote root")
    parser.add_argument("--local-dir", default="data", help="local data directory")
    parser.add_argument("--tail-chunks", type=int, default=2, help="how many latest chunks per dataset to pull")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    local_dir = Path(args.local_dir).resolve()
    local_dir.mkdir(parents=True, exist_ok=True)
    tail_chunks = max(1, int(args.tail_chunks))

    # 1) Pull all manifests (tiny files).
    _run(
        [
            "rclone",
            "copy",
            args.remote,
            str(local_dir),
            "--include",
            "**/manifest.json",
            "--create-empty-src-dirs",
            "-v",
        ]
    )

    # 2) For each manifest, pull only last N chunks.
    pulled = 0
    for manifest_path in _iter_manifest_files(local_dir):
        try:
            manifest = _load_manifest(manifest_path)
        except Exception as e:
            print(f"skip invalid manifest {manifest_path}: {e}", flush=True)
            continue

        chunks = list(manifest.get("chunks") or [])
        if not chunks:
            continue
        selected = chunks[-tail_chunks:]

        rel_dataset_dir = manifest_path.parent.relative_to(local_dir).as_posix()
        remote_dataset_dir = _remote_join(args.remote, rel_dataset_dir)

        for entry in selected:
            file_name = str(entry.get("file", "")).strip()
            if not file_name:
                continue
            remote_file = _remote_join(remote_dataset_dir, file_name)
            local_file = manifest_path.parent / file_name
            local_file.parent.mkdir(parents=True, exist_ok=True)
            rc = _run(["rclone", "copyto", remote_file, str(local_file), "-v"], check=False)
            if rc == 0:
                pulled += 1
            else:
                print(f"warn: failed to pull {remote_file} (rc={rc})", flush=True)

    if args.verbose:
        print(f"pulled chunk files: {pulled}", flush=True)


if __name__ == "__main__":
    main()
