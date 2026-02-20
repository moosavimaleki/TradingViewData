from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

RANGE_TF_RE = re.compile(r"^[0-9]+[rR]$")


@dataclass
class Job:
    source: str
    symbol: str
    broker: Optional[str]
    timeframe: str
    enabled: bool


def is_range_timeframe(tf: str) -> bool:
    return bool(RANGE_TF_RE.fullmatch(str(tf).strip()))


def normalize_timeframe(raw: str) -> str:
    tf = str(raw).strip()
    if tf in {"1D", "D"}:
        return "1d"
    if tf in {"1W", "W"}:
        return "1w"
    if is_range_timeframe(tf):
        return tf.upper()
    return tf


def load_jobs(config_path: Path) -> List[Job]:
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    default_cfg = dict(payload.get("default") or {})

    out: List[Job] = []
    for item in payload.get("jobs") or []:
        merged = dict(default_cfg)
        merged.update(item or {})
        out.append(
            Job(
                source=str(merged.get("source", "tradingview")).strip().lower(),
                symbol=str(merged.get("symbol", "")).strip().upper(),
                broker=(str(merged.get("broker")).strip().upper() if merged.get("broker") else None),
                timeframe=str(merged.get("timeframe", "1m")).strip(),
                enabled=bool(merged.get("enabled", True)),
            )
        )
    return [j for j in out if j.enabled]


def resolve_symbol_exchange(job: Job) -> tuple[str, str]:
    symbol = job.symbol
    broker = (job.broker or "").strip().upper()

    if ":" in symbol:
        left, right = symbol.split(":", 1)
        left = left.strip().upper()
        right = right.strip().upper()
        if broker:
            if left == broker:
                return right, broker
            if right == broker:
                return left, broker
            return left, broker
        return left, right

    if not broker:
        raise ValueError(f"job has no broker/exchange: symbol={symbol!r}")
    return symbol, broker

