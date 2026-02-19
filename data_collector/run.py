from __future__ import annotations

import argparse
import json
import os
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from data_collector.collector import DataCollector
from data_collector.config.settings import Settings


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _parse_dt(raw: Optional[str]) -> Optional[datetime]:
    if not raw:
        return None
    value = str(raw).strip()
    if not value:
        return None
    value = value.replace("Z", "+00:00")
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt


def _normalize_source(raw: str) -> str:
    src = str(raw).strip().lower()
    if src in {"tv", "tradingview"}:
        return "tradingview"
    if src in {"tv_fastpass", "fastpass"}:
        return "tv_fastpass"
    if src in {"faraz", "yahoo_finance"}:
        return src
    raise ValueError(f"Unsupported source: {raw}")


def _to_contract(symbol: str, broker: Optional[str]) -> str:
    base = str(symbol).strip().upper()
    br = str(broker).strip().upper() if broker else ""
    if ":" in base or not br:
        return base
    return f"{base}:{br}"


def _load_json(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass
class Job:
    symbol: str
    timeframe: str
    source: str
    broker: Optional[str] = None
    start_date: Optional[datetime] = None
    update_only: bool = True
    enabled: bool = True
    note: str = ""


def _build_jobs(payload: Dict[str, Any]) -> List[Job]:
    default_cfg = dict(payload.get("default") or {})
    jobs: List[Job] = []
    for item in list(payload.get("jobs") or []):
        merged = dict(default_cfg)
        merged.update(item or {})
        job = Job(
            symbol=str(merged["symbol"]).strip().upper(),
            timeframe=str(merged.get("timeframe", "1m")).strip(),
            source=_normalize_source(str(merged.get("source", "tradingview"))),
            broker=(str(merged.get("broker")).strip().upper() if merged.get("broker") else None),
            start_date=_parse_dt(merged.get("start_date")),
            update_only=bool(merged.get("update_only", True)),
            enabled=bool(merged.get("enabled", True)),
            note=str(merged.get("note", "")).strip(),
        )
        jobs.append(job)
    return [j for j in jobs if j.enabled]


def _enable_sources_in_settings(settings: Settings, jobs: List[Job]) -> None:
    src_cfg = settings.config.setdefault("sources", {})
    required_sources = {job.source for job in jobs}
    for source_name in ["yahoo_finance", "faraz", "tv_fastpass", "tradingview"]:
        src_cfg.setdefault(source_name, {})
        src_cfg[source_name]["enabled"] = source_name in required_sources


def _build_collector(settings_path: Optional[str], jobs: List[Job]) -> DataCollector:
    settings = Settings(settings_path) if settings_path else Settings()
    _enable_sources_in_settings(settings, jobs)
    collector = DataCollector(settings=settings)

    faraz_cookies = os.getenv("FARAZ_COOKIES", "").strip()
    if faraz_cookies:
        collector.set_faraz_cookies(faraz_cookies)
    return collector


def main() -> None:
    parser = argparse.ArgumentParser(description="Run incremental market data collection jobs.")
    parser.add_argument("--config", default="config/collect_jobs.json", help="Jobs config path")
    parser.add_argument("--settings", default="", help="Optional settings.json override path")
    parser.add_argument("--full", action="store_true", help="Ignore update_only and run full range for all jobs")
    parser.add_argument("--dry-run", action="store_true", help="Only print planned jobs")
    parser.add_argument("--fail-on-error", action="store_true", help="Exit non-zero when any job fails")
    args = parser.parse_args()

    config_path = Path(args.config).resolve()
    payload = _load_json(config_path)
    jobs = _build_jobs(payload)
    delay_seconds = float((payload.get("default") or {}).get("delay_seconds", 0.5))
    fallback_start = _parse_dt((payload.get("default") or {}).get("fallback_start_date"))
    if fallback_start is None:
        fallback_start = datetime(2010, 1, 1, tzinfo=timezone.utc)

    if args.dry_run:
        print(
            json.dumps(
                {
                    "config": str(config_path),
                    "jobs": [
                        {
                            "source": j.source,
                            "symbol": j.symbol,
                            "broker": j.broker,
                            "timeframe": j.timeframe,
                            "start_date": (j.start_date.isoformat() if j.start_date else None),
                            "update_only": j.update_only and not args.full,
                            "note": j.note,
                        }
                        for j in jobs
                    ],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    settings_path = args.settings.strip() or None
    collector = _build_collector(settings_path, jobs)

    summary: Dict[str, Any] = {
        "started_at": _utc_now().isoformat(),
        "jobs_total": len(jobs),
        "success": [],
        "failed": [],
    }

    for i, job in enumerate(jobs, start=1):
        symbol_contract = _to_contract(job.symbol, job.broker)
        end_date = _utc_now()
        start_date = job.start_date or fallback_start
        update_only = False if args.full else bool(job.update_only)

        result = collector.collect(
            symbols=[symbol_contract],
            sources=[job.source],
            timeframe=job.timeframe,
            start_date=start_date,
            end_date=end_date,
            update_only=update_only,
        )
        ok = bool(result.get("success")) and not bool(result.get("failed"))

        item = {
            "idx": i,
            "source": job.source,
            "symbol": symbol_contract,
            "timeframe": job.timeframe,
            "update_only": update_only,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "result": result,
        }
        if ok:
            summary["success"].append(item)
        else:
            summary["failed"].append(item)

        time.sleep(max(0.0, delay_seconds))

    summary["finished_at"] = _utc_now().isoformat()
    summary["ok"] = len(summary["failed"]) == 0
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    if args.fail_on_error and summary["failed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
