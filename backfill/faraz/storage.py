from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable

import pandas as pd

REQUIRED_COLUMNS = ("ts", "open", "high", "low", "close", "volume")


def parquet_path_for_year(
    *,
    data_root: Path,
    source: str,
    broker: str,
    timeframe: str,
    symbol: str,
    year: int,
) -> Path:
    return data_root / source.lower() / broker.upper() / timeframe / symbol.upper() / f"{int(year)}.parquet"


def normalize_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame(columns=list(REQUIRED_COLUMNS))

    out = df.copy()
    out.columns = [str(c).strip().lower() for c in out.columns]
    col_map = {
        "timestamp": "ts",
        "time": "ts",
        "datetime": "ts",
        "date": "ts",
    }
    for src, dst in col_map.items():
        if src in out.columns and dst not in out.columns:
            out = out.rename(columns={src: dst})

    for col in REQUIRED_COLUMNS:
        if col not in out.columns:
            out[col] = 0.0 if col == "volume" else pd.NA

    out["ts"] = pd.to_numeric(out["ts"], errors="coerce")
    for col in ("open", "high", "low", "close", "volume"):
        out[col] = pd.to_numeric(out[col], errors="coerce")
    out["volume"] = out["volume"].fillna(0.0)
    out = out.dropna(subset=["ts", "open", "high", "low", "close"])
    out = out.sort_values("ts")
    out = out.drop_duplicates(subset=["ts"], keep="last").reset_index(drop=True)

    out["ts"] = out["ts"].astype("float64")
    for col in ("open", "high", "low", "close", "volume"):
        out[col] = out[col].astype("float64")
    return out[list(REQUIRED_COLUMNS)]


def load_parquet(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=list(REQUIRED_COLUMNS))
    return normalize_ohlcv(pd.read_parquet(path, engine="pyarrow"))


def merge_parquet(path: Path, incoming_df: pd.DataFrame) -> Dict[str, int]:
    incoming = normalize_ohlcv(incoming_df)
    if incoming.empty:
        return {"before": 0, "after": 0, "deduped": 0, "added": 0}

    current = load_parquet(path)
    rows_before = int(len(current))
    merged = pd.concat([current, incoming], ignore_index=True, sort=False)
    before_dedup = int(len(merged))
    merged = normalize_ohlcv(merged)

    path.parent.mkdir(parents=True, exist_ok=True)
    merged.to_parquet(path, engine="pyarrow", compression="zstd", index=False)

    rows_after = int(len(merged))
    deduped = int(before_dedup - rows_after)
    added = int(rows_after - rows_before)
    return {"before": rows_before, "after": rows_after, "deduped": deduped, "added": added}


def split_by_year(df: pd.DataFrame) -> Iterable[tuple[int, pd.DataFrame]]:
    normalized = normalize_ohlcv(df)
    if normalized.empty:
        return []

    dt = pd.to_datetime(normalized["ts"], unit="s", utc=True, errors="coerce")
    normalized = normalized.assign(_year=dt.dt.year)
    normalized = normalized.dropna(subset=["_year"])
    normalized["_year"] = normalized["_year"].astype(int)

    groups = []
    for year, part in normalized.groupby("_year", sort=True):
        groups.append((int(year), part.drop(columns=["_year"]).reset_index(drop=True)))
    return groups
