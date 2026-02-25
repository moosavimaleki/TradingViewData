#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

import pandas as pd

# Allow running as `python backfill/faraz/prepend_from_faraz.py`.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backfill.faraz.storage import load_parquet, merge_parquet, normalize_ohlcv, parquet_path_for_year, split_by_year
from backfill.faraz.client import storage_broker_for_symbol

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


def _is_range_timeframe(raw: str) -> bool:
    return bool(re.fullmatch(r"\d+R", str(raw or "").strip(), flags=re.IGNORECASE))


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


def _discover_target_timeframes(*, data_root: Path, item: MapItem) -> List[str]:
    broker_root = data_root / item.target_source / item.target_broker
    if not broker_root.exists():
        return []

    out: List[str] = []
    for tf_dir in sorted(p for p in broker_root.iterdir() if p.is_dir()):
        symbol_dir = tf_dir / item.target_symbol
        if not symbol_dir.exists() or not symbol_dir.is_dir():
            continue
        if not any(symbol_dir.glob("*.parquet")):
            continue
        out.append(tf_dir.name)
    return out


def _expand_map_targets(*, data_root: Path, item: MapItem) -> Iterable[tuple[str, str]]:
    discovered_tfs = _discover_target_timeframes(data_root=data_root, item=item)
    if discovered_tfs:
        for tf in discovered_tfs:
            yield (tf, tf)
        return

    # Fallback for older configs or partially-downloaded local state.
    if item.target_timeframe:
        tf = item.target_timeframe
        yield (tf, tf if not item.faraz_timeframe else item.faraz_timeframe)


def main() -> None:
    args = _parse_args()
    _setup_logging(args.log_level)

    map_path = Path(args.map_config).resolve()
    data_root = Path(args.data_root).resolve()

    if not map_path.exists():
        raise SystemExit(f"map config not found: {map_path}")

    maps = _load_map_items(map_path)
    summary = {"ok": [], "skipped": [], "failed": []}
    logger.info("Starting Faraz prepend map_config=%s data_root=%s maps=%s", map_path, data_root, len(maps))
    seen = set()

    for idx, item in enumerate(maps, start=1):
        logger.info(
            "[map %s/%s] faraz=%s/%s/%s -> target=%s/%s/%s/%s (timeframes in map are treated as hints; target discovery is automatic)",
            idx,
            len(maps),
            item.faraz_broker,
            item.faraz_symbol,
            item.faraz_timeframe,
            item.target_source,
            item.target_broker,
            item.target_symbol,
            item.target_timeframe,
        )
        if not all(
            [
                item.faraz_symbol,
                item.faraz_broker,
                item.target_symbol,
                item.target_broker,
            ]
        ):
            summary["failed"].append({"map": item.__dict__, "error": "invalid map item (missing fields)"})
            continue

        expanded = list(_expand_map_targets(data_root=data_root, item=item))
        if not expanded:
            logger.info(
                "  skip: no local target timeframe directories found for %s/%s/%s",
                item.target_source,
                item.target_broker,
                item.target_symbol,
            )
            summary["skipped"].append({"target": item.__dict__, "reason": "no target timeframes discovered"})
            continue

        for target_timeframe, faraz_timeframe in expanded:
            map_key = (
                item.faraz_symbol,
                item.faraz_broker,
                item.target_source,
                item.target_symbol,
                item.target_broker,
                target_timeframe,
            )
            if map_key in seen:
                logger.info("  skip duplicate expanded target timeframe=%s", target_timeframe)
                continue
            seen.add(map_key)

            if _is_range_timeframe(target_timeframe):
                logger.info("  skip range timeframe=%s (Faraz prepend supports non-range only)", target_timeframe)
                summary["skipped"].append(
                    {"target": {**item.__dict__, "timeframe": target_timeframe}, "reason": "range timeframe is not supported"}
                )
                continue

            faraz_storage_broker = storage_broker_for_symbol(symbol=item.faraz_symbol, requested_broker=item.faraz_broker)
            faraz_base = data_root / "faraz" / faraz_storage_broker / faraz_timeframe / item.faraz_symbol
            target_base = data_root / item.target_source / item.target_broker / target_timeframe / item.target_symbol

            logger.info(
                "  prepend timeframe=%s faraz_tf=%s faraz_storage_broker=%s",
                target_timeframe,
                faraz_timeframe,
                faraz_storage_broker,
            )

            target_df = _load_concat_years(target_base)
            if target_df.empty:
                summary["skipped"].append(
                    {"target": {**item.__dict__, "timeframe": target_timeframe}, "reason": "target has no data"}
                )
                continue

            faraz_df = _load_concat_years(faraz_base)
            if faraz_df.empty:
                summary["skipped"].append(
                    {
                        "target": {**item.__dict__, "timeframe": target_timeframe},
                        "faraz_storage_broker": faraz_storage_broker,
                        "reason": "faraz source has no data",
                    }
                )
                continue

            earliest_target_ts = float(target_df["ts"].min())
            prepend_df = faraz_df[faraz_df["ts"] < earliest_target_ts].copy()
            prepend_df = normalize_ohlcv(prepend_df)
            if prepend_df.empty:
                summary["skipped"].append(
                    {"target": {**item.__dict__, "timeframe": target_timeframe}, "reason": "no older rows to prepend"}
                )
                continue

            file_stats = []
            for year, part in split_by_year(prepend_df):
                target_file = parquet_path_for_year(
                    data_root=data_root,
                    source=item.target_source,
                    broker=item.target_broker,
                    timeframe=target_timeframe,
                    symbol=item.target_symbol,
                    year=year,
                )
                stats = merge_parquet(target_file, part)
                logger.info(
                    "  merged target symbol=%s broker=%s tf=%s year=%s added=%s deduped=%s after=%s path=%s",
                    item.target_symbol,
                    item.target_broker,
                    target_timeframe,
                    year,
                    stats.get("added"),
                    stats.get("deduped"),
                    stats.get("after"),
                    target_file,
                )
                file_stats.append({"year": int(year), "file": str(target_file), **stats})

            summary["ok"].append(
                {
                    "map": item.__dict__,
                    "effective_target_timeframe": target_timeframe,
                    "effective_faraz_timeframe": faraz_timeframe,
                    "faraz_storage_broker": faraz_storage_broker,
                    "earliest_target_ts": earliest_target_ts,
                    "prepended_rows": int(len(prepend_df)),
                    "files": file_stats,
                }
            )

    logger.info(
        "Faraz prepend finished ok=%s skipped=%s failed=%s",
        len(summary["ok"]),
        len(summary["skipped"]),
        len(summary["failed"]),
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if summary["failed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
