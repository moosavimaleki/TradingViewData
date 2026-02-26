from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd

from .normalize import PROVENANCE_COLUMN, REQUIRED_NUMERIC, normalize_frame


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


def load_existing_parquet(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=["ts", *REQUIRED_NUMERIC, PROVENANCE_COLUMN])
    df = pd.read_parquet(path, engine="pyarrow")
    return normalize_frame(df, drop_latest_candle=False)


def range_cutoff_ts(existing_df: pd.DataFrame, overlap_bars: int) -> Optional[float]:
    if existing_df.empty or "ts" not in existing_df.columns:
        return None
    tail = existing_df.sort_values("ts").tail(max(1, int(overlap_bars)))
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


def merge_and_save_parquet(path: Path, old_df: pd.DataFrame, new_df: pd.DataFrame) -> dict:
    rows_before = int(len(old_df))
    merged = pd.concat([old_df, new_df], ignore_index=True, sort=False)
    before_dedup = int(len(merged))
    merged = normalize_frame(merged, drop_latest_candle=False)

    merged = merged.sort_values("ts")
    merged = merged.drop_duplicates(subset=["ts"], keep="last")
    merged = merged.sort_values("ts").reset_index(drop=True)

    path.parent.mkdir(parents=True, exist_ok=True)
    merged.to_parquet(path, engine="pyarrow", compression="zstd", index=False)

    rows_after = int(len(merged))
    deduped = int(before_dedup - rows_after)
    after_last_row = _row_to_dict(merged.iloc[-1]) if not merged.empty else None
    return {
        "rows_before": rows_before,
        "rows_after": rows_after,
        "deduped": deduped,
        "after_last_row": after_last_row,
    }
