#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List

import pandas as pd

# Allow running as `python backfill/faraz/prepend_from_faraz.py`.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backfill.faraz.storage import load_parquet, merge_parquet, normalize_ohlcv, parquet_path_for_year, split_by_year

logger = logging.getLogger("backfill.faraz.prepend_from_faraz")


@dataclass(frozen=True)
class MapItem:
    faraz_symbol: str
    faraz_broker: str
    faraz_timeframe: str
    target_symbol: str
    target_broker: str
    target_timeframe: str
    target_source: str = "tradingview"


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Prepend Faraz historical parquet before TradingView history")
    p.add_argument("--map-config", default="config/backfill_prepend_maps.json")
    p.add_argument("--data-root", default="data")
    p.add_argument("--log-level", default="INFO")
    return p.parse_args()


def _setup_logging(level_name: str) -> None:
    level = getattr(logging, str(level_name).strip().upper(), logging.INFO)
    logging.basicConfig(level=level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def _load_map_items(path: Path) -> List[MapItem]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    raw_items = payload.get("maps")
    if not isinstance(raw_items, list):
        raise ValueError("map config must include a 'maps' list")

    out: List[MapItem] = []
    for raw in raw_items:
        if not isinstance(raw, dict):
            continue
        faraz = raw.get("faraz") or {}
        target = raw.get("target") or {}
        out.append(
            MapItem(
                faraz_symbol=str(faraz.get("symbol", "")).strip().upper(),
                faraz_broker=str(faraz.get("broker", "")).strip().upper(),
                faraz_timeframe=str(faraz.get("timeframe", "")).strip(),
                target_symbol=str(target.get("symbol", "")).strip().upper(),
                target_broker=str(target.get("broker", "")).strip().upper(),
                target_timeframe=str(target.get("timeframe", "")).strip(),
                target_source=str(target.get("source", "tradingview")).strip().lower() or "tradingview",
            )
        )
    return out


def _all_year_files(base: Path) -> List[Path]:
    if not base.exists():
        return []
    files = [p for p in base.glob("*.parquet") if p.is_file()]
    files.sort(key=lambda x: x.name)
    return files


def _load_concat_years(base: Path) -> pd.DataFrame:
    parts = []
    for path in _all_year_files(base):
        try:
            parts.append(load_parquet(path))
        except Exception:
            continue
    if not parts:
        return pd.DataFrame(columns=["ts", "open", "high", "low", "close", "volume"])
    return normalize_ohlcv(pd.concat(parts, ignore_index=True, sort=False))


def main() -> None:
    args = _parse_args()
    _setup_logging(args.log_level)

    map_path = Path(args.map_config).resolve()
    data_root = Path(args.data_root).resolve()

    if not map_path.exists():
        raise SystemExit(f"map config not found: {map_path}")

    maps = _load_map_items(map_path)
    summary = {"ok": [], "skipped": [], "failed": []}

    for item in maps:
        if not all(
            [
                item.faraz_symbol,
                item.faraz_broker,
                item.faraz_timeframe,
                item.target_symbol,
                item.target_broker,
                item.target_timeframe,
            ]
        ):
            summary["failed"].append({"map": item.__dict__, "error": "invalid map item (missing fields)"})
            continue

        faraz_base = data_root / "faraz" / item.faraz_broker / item.faraz_timeframe / item.faraz_symbol
        target_base = data_root / item.target_source / item.target_broker / item.target_timeframe / item.target_symbol

        target_df = _load_concat_years(target_base)
        if target_df.empty:
            summary["skipped"].append({"target": item.__dict__, "reason": "target has no data"})
            continue

        faraz_df = _load_concat_years(faraz_base)
        if faraz_df.empty:
            summary["skipped"].append({"target": item.__dict__, "reason": "faraz source has no data"})
            continue

        earliest_target_ts = float(target_df["ts"].min())
        prepend_df = faraz_df[faraz_df["ts"] < earliest_target_ts].copy()
        prepend_df = normalize_ohlcv(prepend_df)
        if prepend_df.empty:
            summary["skipped"].append({"target": item.__dict__, "reason": "no older rows to prepend"})
            continue

        file_stats = []
        for year, part in split_by_year(prepend_df):
            target_file = parquet_path_for_year(
                data_root=data_root,
                source=item.target_source,
                broker=item.target_broker,
                timeframe=item.target_timeframe,
                symbol=item.target_symbol,
                year=year,
            )
            stats = merge_parquet(target_file, part)
            file_stats.append({"year": int(year), "file": str(target_file), **stats})

        summary["ok"].append(
            {
                "map": item.__dict__,
                "earliest_target_ts": earliest_target_ts,
                "prepended_rows": int(len(prepend_df)),
                "files": file_stats,
            }
        )

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if summary["failed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
