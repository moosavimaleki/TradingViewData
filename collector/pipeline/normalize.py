from __future__ import annotations

import pandas as pd

REQUIRED_NUMERIC = ("open", "high", "low", "close", "volume")
PROVENANCE_COLUMN = "faraz"
TS_ALIASES = ("ts", "timestamp", "time", "datetime", "date", "index")


def to_epoch_seconds(series: pd.Series) -> pd.Series:
    raw = series.copy()
    numeric = pd.to_numeric(raw, errors="coerce")
    out = pd.Series(index=raw.index, dtype="float64")

    numeric_mask = numeric.notna()
    if numeric_mask.any():
        num = numeric[numeric_mask].astype("float64")
        abs_num = num.abs()
        sec = pd.Series(index=num.index, dtype="float64")

        ns_mask = abs_num >= 1e17
        us_mask = (abs_num >= 1e14) & (abs_num < 1e17)
        ms_mask = (abs_num >= 1e11) & (abs_num < 1e14)
        sec_mask = abs_num < 1e11

        sec.loc[ns_mask] = num.loc[ns_mask] / 1_000_000_000.0
        sec.loc[us_mask] = num.loc[us_mask] / 1_000_000.0
        sec.loc[ms_mask] = num.loc[ms_mask] / 1_000.0
        sec.loc[sec_mask] = num.loc[sec_mask]
        out.loc[numeric_mask] = sec

    non_numeric_mask = ~numeric_mask
    if non_numeric_mask.any():
        dt = pd.to_datetime(raw[non_numeric_mask], utc=True, errors="coerce")
        valid = dt.notna()
        if valid.any():
            out.loc[dt[valid].index] = dt[valid].astype("int64").astype("float64") / 1_000_000_000.0

    if out.isna().any():
        bad = raw[out.isna()].head(5).tolist()
        raise ValueError(f"Could not convert ts values to epoch-seconds. sample={bad}")

    return out.astype("float64")


def normalize_frame(
    df: pd.DataFrame | None,
    *,
    drop_latest_candle: bool,
) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame(columns=["ts", *REQUIRED_NUMERIC, PROVENANCE_COLUMN])

    out = df.copy()

    if not isinstance(out.index, pd.RangeIndex):
        out = out.reset_index()

    out.columns = [str(c).strip() for c in out.columns]
    lower_map = {c.lower(): c for c in out.columns}

    if "ts" not in out.columns:
        ts_col = None
        for alias in TS_ALIASES:
            if alias in lower_map:
                ts_col = lower_map[alias]
                break
        if ts_col is None:
            raise ValueError(f"Missing timestamp column. Available columns={list(out.columns)}")
        out = out.rename(columns={ts_col: "ts"})

    for col in REQUIRED_NUMERIC:
        if col not in out.columns:
            if col in lower_map:
                out = out.rename(columns={lower_map[col]: col})
            else:
                out[col] = 0.0 if col == "volume" else pd.NA

    if PROVENANCE_COLUMN not in out.columns:
        if PROVENANCE_COLUMN in lower_map:
            out = out.rename(columns={lower_map[PROVENANCE_COLUMN]: PROVENANCE_COLUMN})
        else:
            out[PROVENANCE_COLUMN] = 0

    out["ts"] = to_epoch_seconds(out["ts"])

    for col in REQUIRED_NUMERIC:
        out[col] = pd.to_numeric(out[col], errors="coerce")
        if col == "volume":
            out[col] = out[col].fillna(0.0)
    out[PROVENANCE_COLUMN] = pd.to_numeric(out[PROVENANCE_COLUMN], errors="coerce").fillna(0)
    out[PROVENANCE_COLUMN] = (out[PROVENANCE_COLUMN] != 0).astype("int8")

    out = out.dropna(subset=["ts", "open", "high", "low", "close"])
    out = out.sort_values("ts")
    out = out.drop_duplicates(subset=["ts"], keep="last").reset_index(drop=True)

    if drop_latest_candle and not out.empty:
        out = out.iloc[:-1].reset_index(drop=True)

    out["ts"] = out["ts"].astype("float64")
    for col in REQUIRED_NUMERIC:
        out[col] = out[col].astype("float64")
    out[PROVENANCE_COLUMN] = out[PROVENANCE_COLUMN].astype("int8")
    return out[["ts", *REQUIRED_NUMERIC, PROVENANCE_COLUMN]]
