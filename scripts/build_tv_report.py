#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def _load_json(path: Path, default_payload: Dict[str, Any]) -> Dict[str, Any]:
    if not path.exists():
        return {**default_payload, "error": f"file not found: {path}"}
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return {**default_payload, "error": f"file is empty: {path}"}
    try:
        payload = json.loads(text)
        if isinstance(payload, dict):
            return payload
        return {**default_payload, "error": f"expected JSON object in: {path}"}
    except Exception as exc:
        return {**default_payload, "error": f"invalid JSON in {path}: {exc}"}


def _totals(ok: List[Dict[str, Any]], skipped: List[Dict[str, Any]], failed: List[Dict[str, Any]]) -> Dict[str, Any]:
    total_before = sum(int(item.get("rows_before", 0) or 0) for item in ok)
    total_after = sum(int(item.get("rows_after", 0) or 0) for item in ok)
    total_new = sum(int(item.get("fetched_rows", 0) or 0) for item in ok)
    total_deduped = sum(int(item.get("deduped", 0) or 0) for item in ok)
    return {
        "ok_count": len(ok),
        "skipped_count": len(skipped),
        "failed_count": len(failed),
        "rows_before_total": total_before,
        "rows_new_total": total_new,
        "rows_after_total": total_after,
        "deduped_total": total_deduped,
        "net_growth": total_after - total_before,
    }


def _fmt_int(value: Any) -> str:
    try:
        return f"{int(value or 0):,}"
    except Exception:
        return "0"


def _as_int(value: Any) -> int:
    try:
        return int(value or 0)
    except Exception:
        return 0


def _fmt_ts_cell(value: Any) -> str:
    raw = str(value or "").strip()
    if not raw or raw == "-":
        return "-"
    if "T" in raw:
        date_part, time_part = raw.split("T", 1)
        return f"`{date_part}`<br>`{time_part}`"
    if " " in raw:
        date_part, time_part = raw.split(" ", 1)
        return f"`{date_part}`<br>`{time_part}`"
    return f"`{raw}`"


def _fmt_symbol_broker_footnote(value: Any) -> str:
    text = str(value or "").strip()
    if not text:
        return "-"
    if ":" not in text:
        return f"`{text}`"
    symbol, broker = text.split(":", 1)
    symbol = symbol.strip() or "-"
    broker = broker.strip()
    if not broker:
        return f"`{symbol}`"
    return f"`{symbol}`<br><sub>{broker.lower()}</sub>"


def _short_path(path: str) -> str:
    text = str(path or "-")
    prefixes = (
        "/home/runner/work/TradingViewData/TradingViewData/",
        "/home/runner/work/TradingViewData/",
    )
    for prefix in prefixes:
        if text.startswith(prefix):
            return "./" + text[len(prefix) :]
    return text


def _overall_status(totals: Dict[str, Any], pull_report: Dict[str, Any]) -> tuple[str, str]:
    pull_status = str(pull_report.get("status", "")).strip().lower()
    failed_pull_states = {"ls_failed", "copy_failed", "copy_incomplete"}

    if int(totals.get("failed_count", 0) or 0) > 0 or pull_status in failed_pull_states:
        return "failed", "❌"
    if int(totals.get("ok_count", 0) or 0) > 0:
        return "success", "✅"
    if int(totals.get("skipped_count", 0) or 0) > 0:
        return "partial", "⚠️"
    return "unknown", "❔"


def _append_list(lines: List[str], title: str, values: List[str], *, emoji: str, limit: int = 200) -> None:
    lines.append(f"### {emoji} {title}")
    lines.append("")
    if not values:
        lines.append("- (none)")
        lines.append("")
        return

    lines.append("<details>")
    lines.append(f"<summary>{len(values)} item(s)</summary>")
    lines.append("")
    for value in values[:limit]:
        lines.append(f"- `{value}`")
    if len(values) > limit:
        lines.append(f"- ... and {len(values) - limit} more")
    lines.append("")
    lines.append("</details>")
    lines.append("")


def _build_markdown(
    *,
    summary: Dict[str, Any],
    pull_report: Dict[str, Any],
    totals: Dict[str, Any],
    run_year: str,
    run_date: str,
    run_id: str,
    run_url: str,
    run_artifacts_url: str,
    run_artifact_url: str,
    run_at_utc: str,
    run_mode: str,
    run_event_name: str,
    run_event_schedule: str,
    run_hour_utc: str,
    run_config_path: str,
) -> str:
    ok = list(summary.get("ok") or [])
    skipped = list(summary.get("skipped") or [])
    failed = list(summary.get("failed") or [])
    overall_state, overall_emoji = _overall_status(totals, pull_report)

    lines: List[str] = []
    lines.append("# 📊 tvdatafeed Collect Report")
    lines.append("")
    lines.append(f"**{overall_emoji} overall_status:** `{overall_state}`")
    lines.append("")
    lines.append("## 🔗 Run Links")
    lines.append("")
    if run_url and run_url != "-":
        lines.append(f"- ▶️ Run: {run_url}")
    if run_artifacts_url and run_artifacts_url != "-":
        lines.append(f"- 📦 Artifacts: {run_artifacts_url}")
    if run_artifact_url and run_artifact_url != "-":
        lines.append(f"- ⬇️ Artifact Download: {run_artifact_url}")
    lines.append("")
    lines.append("## Run Context 🧭")
    lines.append("")
    lines.append(f"- run_date_utc: {run_date}")
    lines.append(f"- run_at_utc: {run_at_utc}")
    lines.append(f"- run_year: {run_year}")
    lines.append(f"- github_run_id: {run_id}")
    lines.append("")
    lines.append("## Run Resolution 🕹️")
    lines.append("")
    lines.append(
        "- `{}`".format(
            "Resolved RUN_MODE={mode} EVENT_NAME={event} EVENT_SCHEDULE={schedule} RUN_HOUR_UTC={hour} config={config}".format(
                mode=run_mode,
                event=run_event_name,
                schedule=run_event_schedule,
                hour=run_hour_utc,
                config=run_config_path,
            )
        )
    )
    lines.append("")

    lines.append("## Drive Pull ☁️ (Yearly Parquet Restore)")
    lines.append("")
    lines.append(f"- status: {pull_report.get('status', '-')}")
    lines.append(f"- expected_count: {_fmt_int(pull_report.get('expected_count', 0))}")
    lines.append(f"- listed_count: {_fmt_int(pull_report.get('listed_count', 0))}")
    lines.append(f"- pulled_count: {_fmt_int(pull_report.get('pulled_count', 0))}")
    lines.append(f"- remote_absent_count: {_fmt_int(pull_report.get('remote_absent_count', 0))}")
    lines.append(f"- copy_missing_count: {_fmt_int(pull_report.get('copy_missing_count', 0))}")
    lines.append(f"- failed_count: {_fmt_int(pull_report.get('failed_count', 0))}")
    lines.append(f"- retries: {pull_report.get('retries', '-')}")
    lines.append(f"- remote_root: {pull_report.get('remote', '-')}")
    lines.append("")

    if pull_report.get("ls_error"):
        lines.append("### ❌ LS Error")
        lines.append("")
        lines.append("```text")
        lines.append(str(pull_report.get("ls_error", "")).strip())
        lines.append("```")
        lines.append("")

    _append_list(lines, "Pulled Files From GDrive", list(pull_report.get("pulled_files") or []), emoji="📥")
    _append_list(lines, "Expected But Not On Remote (new targets)", list(pull_report.get("remote_absent_files") or []), emoji="🆕")
    _append_list(lines, "Copy Missing Files", list(pull_report.get("copy_missing_files") or []), emoji="⚠️")

    lines.append("### 🚨 Copy Failures")
    lines.append("")
    failed_files = list(pull_report.get("failed_files") or [])
    if failed_files:
        lines.append("<details>")
        lines.append(f"<summary>{len(failed_files)} failure(s)</summary>")
        lines.append("")
        for item in failed_files:
            rel = item.get("file", "-")
            err = str(item.get("error", "")).strip()
            lines.append(f"- file: `{rel}`")
            lines.append("```text")
            lines.append(err if err else "(no error text)")
            lines.append("```")
        lines.append("")
        lines.append("</details>")
    else:
        lines.append("- (none)")
    lines.append("")

    lines.append("## Collect Totals 📈")
    lines.append("")
    lines.append(f"- ok: {_fmt_int(totals['ok_count'])}")
    lines.append(f"- skipped: {_fmt_int(totals['skipped_count'])}")
    lines.append(f"- failed: {_fmt_int(totals['failed_count'])}")
    lines.append(f"- rows_before_total: {_fmt_int(totals['rows_before_total'])}")
    lines.append(f"- rows_new_total: {_fmt_int(totals['rows_new_total'])}")
    lines.append(f"- rows_after_total: {_fmt_int(totals['rows_after_total'])}")
    lines.append(f"- deduped_total: {_fmt_int(totals['deduped_total'])}")
    lines.append(f"- net_growth: {_fmt_int(totals['net_growth'])}")
    lines.append("")

    if ok:
        lines.append("## Per Parquet Change 🧩")
        lines.append("")
        lines.append(
            "| symbol + broker | tf | added | overridden (overlap) | mode | before | fetched | after | overlap_rows | overlap_min | prev_last | new_first | new_last | after_last |"
        )
        lines.append("|---|---|---:|---:|---|---:|---:|---:|---:|---:|---|---|---|---|")
        for item in ok:
            before = _as_int(item.get("rows_before", 0))
            after = _as_int(item.get("rows_after", 0))
            fetched = _as_int(item.get("fetched_rows", 0))
            overridden = _as_int(item.get("deduped", 0))
            added = after - before
            lines.append(
                "| {symbol} | {tf} | {added} | {overridden} | {mode} | {before} | {fetched} | {after} | {overlap_rows} | {overlap_min} | {prev_last} | {new_first} | {new_last} | {after_last} |".format(
                    symbol=_fmt_symbol_broker_footnote(item.get("symbol", "")),
                    tf=item.get("timeframe", ""),
                    added=added,
                    overridden=overridden,
                    mode=item.get("mode", ""),
                    before=before,
                    fetched=fetched,
                    after=after,
                    prev_last=_fmt_ts_cell(item.get("before_last_ts_iso")),
                    new_first=_fmt_ts_cell(item.get("fetched_first_ts_iso")),
                    new_last=_fmt_ts_cell(item.get("fetched_last_ts_iso")),
                    after_last=_fmt_ts_cell(item.get("after_last_ts_iso")),
                    overlap_rows=_as_int(item.get("overlap_rows", 0)),
                    overlap_min=item.get("overlap_minutes", 0) or 0,
                )
            )
        lines.append("")

        lines.append("### 🗂️ Output Files")
        lines.append("")
        lines.append("<details>")
        lines.append(f"<summary>{len(ok)} output file(s)</summary>")
        lines.append("")
        for item in ok:
            lines.append(f"- `{_short_path(item.get('file', '-'))}`")
        lines.append("")
        lines.append("</details>")
        lines.append("")

    if skipped:
        lines.append("## Skipped ⏭️")
        lines.append("")
        for item in skipped:
            lines.append(f"- {item}")
        lines.append("")

    if failed:
        lines.append("## Failed ❌")
        lines.append("")
        for item in failed:
            lines.append(f"- {item}")
        lines.append("")

    if summary.get("error"):
        lines.append("## Summary Error 🚨")
        lines.append("")
        lines.append(f"- {summary['error']}")
        lines.append("")

    if pull_report.get("error"):
        lines.append("## Pull Report Error 🚨")
        lines.append("")
        lines.append(f"- {pull_report['error']}")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build markdown report from tvdatafeed summary + drive pull report")
    parser.add_argument("--summary", default="tvdatafeed_summary.json")
    parser.add_argument("--pull-json", default="tvdatafeed_pull.json")
    parser.add_argument("--out-md", default="tvdatafeed_report.md")
    parser.add_argument("--run-year", default="")
    parser.add_argument("--run-date", default="")
    parser.add_argument("--run-id", default="")
    parser.add_argument("--run-url", default="")
    parser.add_argument("--run-artifacts-url", default="")
    parser.add_argument("--run-artifact-url", default="")
    parser.add_argument("--run-at-utc", default="")
    parser.add_argument("--run-mode", default="")
    parser.add_argument("--run-event-name", default="")
    parser.add_argument("--run-event-schedule", default="")
    parser.add_argument("--run-hour-utc", default="")
    parser.add_argument("--run-config-path", default="")
    args = parser.parse_args()

    summary_path = Path(args.summary).resolve()
    pull_path = Path(args.pull_json).resolve()
    out_md = Path(args.out_md).resolve()

    summary = _load_json(summary_path, {"ok": [], "skipped": [], "failed": []})
    pull_report = _load_json(
        pull_path,
        {
            "status": "missing",
            "expected_count": 0,
            "listed_count": 0,
            "pulled_count": 0,
            "remote_absent_count": 0,
            "copy_missing_count": 0,
            "failed_count": 0,
            "pulled_files": [],
            "remote_absent_files": [],
            "copy_missing_files": [],
            "failed_files": [],
        },
    )

    ok = list(summary.get("ok") or [])
    skipped = list(summary.get("skipped") or [])
    failed = list(summary.get("failed") or [])
    totals = _totals(ok, skipped, failed)

    run_year = str(args.run_year).strip() or "-"
    run_date = str(args.run_date).strip() or "-"
    run_id = str(args.run_id).strip() or "-"
    run_url = str(args.run_url).strip() or "-"
    run_artifacts_url = str(args.run_artifacts_url).strip() or "-"
    run_artifact_url = str(args.run_artifact_url).strip() or "-"
    run_at_utc = str(args.run_at_utc).strip() or "-"
    run_mode = str(args.run_mode).strip() or "-"
    run_event_name = str(args.run_event_name).strip() or "-"
    run_event_schedule = str(args.run_event_schedule).strip() or "-"
    run_hour_utc = str(args.run_hour_utc).strip() or "-"
    run_config_path = str(args.run_config_path).strip() or "-"

    out_md.write_text(
        _build_markdown(
            summary=summary,
            pull_report=pull_report,
            totals=totals,
            run_year=run_year,
            run_date=run_date,
            run_id=run_id,
            run_url=run_url,
            run_artifacts_url=run_artifacts_url,
            run_artifact_url=run_artifact_url,
            run_at_utc=run_at_utc,
            run_mode=run_mode,
            run_event_name=run_event_name,
            run_event_schedule=run_event_schedule,
            run_hour_utc=run_hour_utc,
            run_config_path=run_config_path,
        ),
        encoding="utf-8",
    )

    print(f"report_md={out_md}")
    print(json.dumps(totals, ensure_ascii=False))


if __name__ == "__main__":
    main()
