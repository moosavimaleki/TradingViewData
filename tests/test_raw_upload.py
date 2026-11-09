from __future__ import annotations

import shutil
import subprocess

import pytest

from collector.pipeline.raw_archive import RawArchive


@pytest.mark.skipif(shutil.which("rclone") is None, reason="rclone not installed")
def test_upload_filters_and_immutable_retries_do_not_overwrite_archives(tmp_path):
    config = tmp_path / "jobs.json"
    config.write_text('{"jobs": []}')
    root = tmp_path / "raw"
    remote = tmp_path / "remote"
    with RawArchive(root, config_path=config) as archive:
        with archive.request(source="tradingview", symbol="TEST", broker="TEST", timeframe="100R", requested_bars=5) as capture:
            capture.message("original bytes")
    filters = ["--include", "**/data.parquet", "--include", "**/manifest.json"]
    command = ["rclone", "--config", "/dev/null", "copy", str(root), str(remote),
               "--immutable", "--checksum", *filters]
    subprocess.run(command, check=True, capture_output=True)
    subprocess.run(command, check=True, capture_output=True)  # Identical retry is permitted.
    subprocess.run(["rclone", "--config", "/dev/null", "check", str(root), str(remote), "--one-way", *filters],
                   check=True, capture_output=True)
    files = sorted(p.name for p in remote.rglob("*") if p.is_file())
    assert files == ["data.parquet", "manifest.json"]
    remote_data = remote / archive.run_dir.relative_to(root) / "data.parquet"
    original = remote_data.read_bytes()
    (archive.run_dir / "data.parquet").write_bytes(b"a different archive must not replace this run")
    assert subprocess.run(command, capture_output=True).returncode != 0
    assert remote_data.read_bytes() == original
