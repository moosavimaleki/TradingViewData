from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable

import pandas as pd

PROVENANCE_COLUMN = "faraz"
REQUIRED_COLUMNS = ("ts", "open", "high", "low", "close", "volume", PROVENANCE_COLUMN)


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


def normalize_ohlcv(df: pd.DataFrame, *, default_faraz: int = 0) -> pd.DataFrame:
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
            if col == "volume":
                out[col] = 0.0
            elif col == PROVENANCE_COLUMN:
                out[col] = int(1 if int(default_faraz) else 0)
            else:
                out[col] = pd.NA

    out["ts"] = pd.to_numeric(out["ts"], errors="coerce")
    for col in ("open", "high", "low", "close", "volume"):
        out[col] = pd.to_numeric(out[col], errors="coerce")
    out["volume"] = out["volume"].fillna(0.0)
    out[PROVENANCE_COLUMN] = pd.to_numeric(out[PROVENANCE_COLUMN], errors="coerce").fillna(int(1 if int(default_faraz) else 0))
    out[PROVENANCE_COLUMN] = (out[PROVENANCE_COLUMN] != 0).astype("int8")
    out = out.dropna(subset=["ts", "open", "high", "low", "close"])
    out = out.sort_values("ts")
    out = out.drop_duplicates(subset=["ts"], keep="last").reset_index(drop=True)

    out["ts"] = out["ts"].astype("float64")
    for col in ("open", "high", "low", "close", "volume"):
        out[col] = out[col].astype("float64")
    out[PROVENANCE_COLUMN] = out[PROVENANCE_COLUMN].astype("int8")
    return out[list(REQUIRED_COLUMNS)]


def load_parquet(path: Path, *, default_faraz: int = 0) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=list(REQUIRED_COLUMNS))
    return normalize_ohlcv(pd.read_parquet(path, engine="pyarrow"), default_faraz=default_faraz)


def merge_parquet(path: Path, incoming_df: pd.DataFrame, *, default_faraz: int = 0) -> Dict[str, int]:
    incoming = normalize_ohlcv(incoming_df, default_faraz=default_faraz)
    if incoming.empty:
        return {"before": 0, "after": 0, "deduped": 0, "added": 0}

    current = load_parquet(path, default_faraz=default_faraz)
    rows_before = int(len(current))
    merged = pd.concat([current, incoming], ignore_index=True, sort=False)
    before_dedup = int(len(merged))
    merged = normalize_ohlcv(merged, default_faraz=default_faraz)

    path.parent.mkdir(parents=True, exist_ok=True)
    merged.to_parquet(path, engine="pyarrow", compression="zstd", index=False)

    rows_after = int(len(merged))
    deduped = int(before_dedup - rows_after)
    added = int(rows_after - rows_before)
    return {"before": rows_before, "after": rows_after, "deduped": deduped, "added": added}


def split_by_year(df: pd.DataFrame, *, default_faraz: int = 0) -> Iterable[tuple[int, pd.DataFrame]]:
    normalized = normalize_ohlcv(df, default_faraz=default_faraz)
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
