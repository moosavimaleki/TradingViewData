#!/usr/bin/env python3
from __future__ import annotations

import argparse
import io
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Union

import pandas as pd

REQUIRED_COLS = ("ts", "open", "high", "low", "close", "volume")
TS_ALIASES = ("ts", "timestamp", "time", "datetime", "date")
NUMERIC_COLS = ("open", "high", "low", "close", "volume")

logger = logging.getLogger("collector.yearly_candles_store")


def _parse_csv_string(csv_text: str) -> pd.DataFrame:
    text = str(csv_text or "").strip()
    if not text:
        raise ValueError("CSV input is empty.")
    return pd.read_csv(io.StringIO(text))


def _new_data_to_dataframe(new_data: Union[pd.DataFrame, str, list[str]]) -> pd.DataFrame:
    if isinstance(new_data, pd.DataFrame):
        return new_data.copy()

    if isinstance(new_data, str):
        return _parse_csv_string(new_data)

    if isinstance(new_data, list):
        if not new_data:
            raise ValueError("CSV list input is empty.")
        parts = [_parse_csv_string(item) for item in new_data]
        return pd.concat(parts, ignore_index=True, sort=False)

    raise TypeError(f"new_data type is not supported: {type(new_data).__name__}")


def _rename_required_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [str(c).strip() for c in out.columns]
    lower_map = {c.lower(): c for c in out.columns}

    rename_map: dict[str, str] = {}

    if "ts" not in out.columns:
        ts_actual = None
        for alias in TS_ALIASES:
            if alias in lower_map:
                ts_actual = lower_map[alias]
                break
        if ts_actual is not None:
            rename_map[ts_actual] = "ts"

    for col in NUMERIC_COLS:
        if col not in out.columns and col in lower_map:
            rename_map[lower_map[col]] = col

    if rename_map:
        out = out.rename(columns=rename_map)
    return out


def _to_epoch_ms(series: pd.Series) -> pd.Series:
    raw = series.copy()
    numeric = pd.to_numeric(raw, errors="coerce")
    result = pd.Series(index=raw.index, dtype="float64")

    numeric_mask = numeric.notna()
    if numeric_mask.any():
        num_vals = numeric[numeric_mask].astype("float64")
        abs_vals = num_vals.abs()
        ms_vals = pd.Series(index=num_vals.index, dtype="float64")

        ns_mask = abs_vals >= 1e17
        us_mask = (abs_vals >= 1e14) & (abs_vals < 1e17)
        ms_mask = (abs_vals >= 1e11) & (abs_vals < 1e14)
        sec_mask = abs_vals < 1e11

        ms_vals.loc[ns_mask] = num_vals.loc[ns_mask] / 1_000_000.0
        ms_vals.loc[us_mask] = num_vals.loc[us_mask] / 1_000.0
        ms_vals.loc[ms_mask] = num_vals.loc[ms_mask]
        ms_vals.loc[sec_mask] = num_vals.loc[sec_mask] * 1_000.0

        result.loc[numeric_mask] = ms_vals

    non_numeric_mask = ~numeric_mask
    if non_numeric_mask.any():
        dt = pd.to_datetime(raw[non_numeric_mask], utc=True, errors="coerce")
        dt_vals = pd.Series(index=dt.index, dtype="float64")
        valid_dt = dt.notna()
        if valid_dt.any():
            dt_vals.loc[valid_dt] = (dt.loc[valid_dt].astype("int64") // 1_000_000).astype("float64")
        result.loc[non_numeric_mask] = dt_vals

    bad_mask = result.isna()
    if bad_mask.any():
        bad_values = raw.loc[bad_mask].head(5).tolist()
        raise ValueError(f"Could not convert some ts values to epoch ms. sample={bad_values}")

    return result.round().astype("int64")


def _normalize_candles_df(df: pd.DataFrame, *, drop_latest_candle: bool) -> pd.DataFrame:
    out = _rename_required_columns(df)
    missing = [c for c in REQUIRED_COLS if c not in out.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}. Available columns={list(out.columns)}")

    out = out.copy()
    out["ts"] = _to_epoch_ms(out["ts"])

    for col in NUMERIC_COLS:
        out[col] = pd.to_numeric(out[col], errors="coerce").astype("float64")
        bad = out[col].isna()
        if bad.any():
            bad_values = df.loc[bad, col].head(5).tolist() if col in df.columns else []
            raise ValueError(f"Could not convert column={col} to float. sample={bad_values}")

    out = out.sort_values("ts")
    out = out.drop_duplicates(subset=["ts"], keep="last").reset_index(drop=True)

    if drop_latest_candle and not out.empty:
        out = out.iloc[:-1].reset_index(drop=True)

    out["ts"] = out["ts"].astype("int64")
    for col in NUMERIC_COLS:
        out[col] = out[col].astype("float64")
    return out


def upsert_yearly_candles(
    broker: str,
    timeframe: str,
    symbol: str,
    new_data: Union[pd.DataFrame, str, list[str]],
    base_dir: str = "data/tradingview",
) -> dict:
    run_year = datetime.now(timezone.utc).year
    file_path = Path(base_dir) / str(broker) / str(timeframe) / str(symbol) / f"{run_year}.parquet"
    file_path.parent.mkdir(parents=True, exist_ok=True)

    df_new_raw = _new_data_to_dataframe(new_data)
    df_new = _normalize_candles_df(df_new_raw, drop_latest_candle=True)

    if file_path.exists():
        df_old_raw = pd.read_parquet(file_path, engine="pyarrow")
        df_old = _normalize_candles_df(df_old_raw, drop_latest_candle=False)
    else:
        if df_new.empty:
            df_old = pd.DataFrame(columns=list(REQUIRED_COLS))
        else:
            df_old = pd.DataFrame(columns=list(df_new.columns))

    rows_before = int(len(df_old))
    rows_new = int(len(df_new))

    df_all = pd.concat([df_old, df_new], ignore_index=True, sort=False)
    before_dedup = int(len(df_all))

    if "ts" not in df_all.columns:
        raise ValueError("Merged dataframe does not contain 'ts' column.")

    if not df_all.empty:
        df_all["ts"] = _to_epoch_ms(df_all["ts"]).astype("int64")
        for col in NUMERIC_COLS:
            if col in df_all.columns:
                df_all[col] = pd.to_numeric(df_all[col], errors="coerce").astype("float64")

    df_all = df_all.sort_values("ts")
    df_all = df_all.drop_duplicates(subset=["ts"], keep="last")
    df_all = df_all.sort_values("ts").reset_index(drop=True)

    rows_after = int(len(df_all))
    deduped = int(before_dedup - rows_after)

    df_all.to_parquet(file_path, engine="pyarrow", compression="zstd", index=False)

    result = {
        "path": str(file_path),
        "run_year": int(run_year),
        "rows_before": rows_before,
        "rows_new": rows_new,
        "rows_after": rows_after,
        "deduped": deduped,
    }
    logger.info("yearly parquet upsert result: %s", result)
    return result


def _build_example_input() -> str:
    # Example CSV text that could come from a TradingView fetch result.
    return """ts,open,high,low,close,volume
1709164800000,1.0810,1.0815,1.0805,1.0812,1200
1709168400000,1.0812,1.0819,1.0809,1.0816,1500
1709172000000,1.0816,1.0821,1.0811,1.0813,1400
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Upsert yearly TradingView candles parquet")
    parser.add_argument("--broker", default="BLACKBULL")
    parser.add_argument("--timeframe", default="1h")
    parser.add_argument("--symbol", default="EURUSD")
    parser.add_argument("--base-dir", default="data/tradingview")
    parser.add_argument(
        "--csv-file",
        help="Optional path to a CSV text file. If omitted, a built-in sample is used.",
    )
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args()

    logging.basicConfig(
        level=getattr(logging, str(args.log_level).upper(), logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    if args.csv_file:
        csv_text = Path(args.csv_file).read_text(encoding="utf-8")
    else:
        csv_text = _build_example_input()

    result = upsert_yearly_candles(
        broker=args.broker,
        timeframe=args.timeframe,
        symbol=args.symbol,
        new_data=csv_text,
        base_dir=args.base_dir,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
