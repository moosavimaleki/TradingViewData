from __future__ import annotations

import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Optional

import pandas as pd

from .normalize import PROVENANCE_COLUMN, REQUIRED_NUMERIC, normalize_frame


class RangeBoundaryError(ValueError):
    pass


def validate_range_snapshot(
    current: pd.DataFrame,
    incoming: pd.DataFrame,
    *,
    overlap_start_ts: float | None = None,
    snapshot_first_ts: float | None = None,
    snapshot_last_ts: float | None = None,
) -> None:
    for name, frame in (("existing", current), ("incoming", incoming)):
        if not frame.empty and not frame["ts"].is_monotonic_increasing:
            raise ValueError(f"Range {name} timestamps are out of order; refusing to rewrite history")
    if current.empty or incoming.empty:
        return
    covered_end = snapshot_last_ts if snapshot_last_ts is not None else float(incoming["ts"].iloc[-1])
    if covered_end < current["ts"].iloc[-1]:
        raise ValueError("Range snapshot ends before existing history; refusing to truncate newer bars")
    if snapshot_last_ts is None and incoming["ts"].iloc[-1] == current["ts"].iloc[-1]:
        last_ts = current["ts"].iloc[-1]
        if (incoming["ts"] == last_ts).sum() < (current["ts"] == last_ts).sum():
            raise ValueError("Range snapshot has a shorter same-second tail; refusing to truncate known bars")

    first_ts = overlap_start_ts if overlap_start_ts is not None else float(incoming["ts"].iloc[0])
    covered_start = snapshot_first_ts if snapshot_first_ts is not None else float(incoming["ts"].iloc[0])
    if covered_start > first_ts:
        raise RangeBoundaryError("Range snapshot does not cover the configured overlap boundary")
    if covered_start < first_ts:
        # Receiving an earlier timestamp proves this entire boundary group
        # was included. Its values/count may legitimately repaint inside
        # the overwrite window; matching old prices is not required.
        return
    old_group = current.loc[current["ts"] == first_ts, list(REQUIRED_NUMERIC)].astype("float64").reset_index(drop=True)
    new_group = incoming.loc[incoming["ts"] == first_ts, list(REQUIRED_NUMERIC)].astype("float64").reset_index(drop=True)
    if old_group.empty and current["ts"].iloc[0] < first_ts:
        raise RangeBoundaryError(
            f"Unmatched range boundary at ts={first_ts}. Fetch more history to establish an overlap anchor."
        )
    if not old_group.empty:
        # The first received second may be cut by the request's bar limit.
        # A missing/changed prefix of a known timestamp group is ambiguous;
        # fetch farther back instead of deleting potentially omitted candles.
        if not old_group.equals(new_group.iloc[:len(old_group)].reset_index(drop=True)):
            raise RangeBoundaryError(
                f"Ambiguous range boundary at ts={first_ts}: existing_bars={len(old_group)} "
                f"incoming_bars={len(new_group)}. Fetch more history before replacing this second."
            )


def year_file_path(
    *,
    data_root: Path,
    source: str,
    broker: str,
    timeframe: str,
    symbol: str,
    run_year: int,
) -> Path:
    return data_root / source / broker / timeframe / symbol / f"{run_year}.parquet"


def load_existing_parquet(path: Path, *, is_range: bool = False) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=["ts", *REQUIRED_NUMERIC, PROVENANCE_COLUMN])
    df = pd.read_parquet(path, engine="pyarrow")
    return normalize_frame(df, drop_latest_candle=False, is_range=is_range)


def range_cutoff_ts(existing_df: pd.DataFrame, overlap_bars: int) -> Optional[float]:
    if existing_df.empty or "ts" not in existing_df.columns:
        return None
    tail = existing_df.tail(max(1, int(overlap_bars)))
    if tail.empty:
        return None
    return float(tail["ts"].iloc[0])


def _row_to_dict(row: pd.Series) -> dict:
    out: dict = {}
    for k, v in row.items():
        if pd.isna(v):
            out[k] = None
        elif hasattr(v, "item"):
            out[k] = v.item()
        else:
            out[k] = v
    return out


def _write_parquet_atomic(path: Path, frame: pd.DataFrame) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with NamedTemporaryFile(dir=path.parent, suffix=".parquet.tmp", delete=False) as tmp:
        tmp_path = Path(tmp.name)
    try:
        frame.to_parquet(tmp_path, engine="pyarrow", compression="zstd", index=False)
        os.replace(tmp_path, path)
    finally:
        tmp_path.unlink(missing_ok=True)


def merge_and_save_parquet(
    path: Path,
    old_df: pd.DataFrame,
    new_df: pd.DataFrame,
    *,
    is_range: bool = False,
    range_overlap_bars: int = 300,
    snapshot_first_ts: float | None = None,
    snapshot_last_ts: float | None = None,
) -> dict:
    rows_before = int(len(old_df))
    replaced_rows = 0
    replacement_start_ts = None

    if is_range:
        current = normalize_frame(old_df, drop_latest_candle=False, is_range=True)
        incoming = normalize_frame(new_df, drop_latest_candle=False, is_range=True)
        replacement_start_ts = range_cutoff_ts(current, max(1, int(range_overlap_bars)))
        if not incoming.empty:
            if snapshot_first_ts is None:
                snapshot_first_ts = float(incoming["ts"].iloc[0])
            if replacement_start_ts is not None:
                incoming = incoming.loc[incoming["ts"] >= replacement_start_ts].reset_index(drop=True)
        validate_range_snapshot(
            current, incoming, overlap_start_ts=replacement_start_ts,
            snapshot_first_ts=snapshot_first_ts, snapshot_last_ts=snapshot_last_ts,
        )

        if incoming.empty:
            merged = current
        else:
            if replacement_start_ts is None:
                replacement_start_ts = float(incoming["ts"].iloc[0])
            # Freeze the archive before the configured overlap, regardless
            # of how much older history the download contains.
            prefix = current[current["ts"] < replacement_start_ts]
            replaced_rows = int(len(current) - len(prefix))
            merged = pd.concat([prefix, incoming], ignore_index=True)
        deduped = 0
    else:
        combined = pd.concat([old_df, new_df], ignore_index=True, sort=False)
        merged = normalize_frame(combined, drop_latest_candle=False)
        deduped = int(len(combined) - len(merged))

    _write_parquet_atomic(path, merged)

    rows_after = int(len(merged))
    after_last_row = _row_to_dict(merged.iloc[-1]) if not merged.empty else None
    return {
        "rows_before": rows_before,
        "rows_after": rows_after,
        "deduped": deduped,
        "replaced_rows": replaced_rows,
        "replacement_start_ts": replacement_start_ts,
        "merge_mode": "replace_range_overlap" if is_range else "upsert_timestamp",
        "after_last_row": after_last_row,
    }
