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


def _append_list(lines: List[str], title: str, values: List[str], limit: int = 200) -> None:
    lines.append(f"### {title}")
    lines.append("")
    if not values:
        lines.append("- (none)")
        lines.append("")
        return
    for value in values[:limit]:
        lines.append(f"- `{value}`")
    if len(values) > limit:
        lines.append(f"- ... and {len(values) - limit} more")
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
    run_at_utc: str,
) -> str:
    ok = list(summary.get("ok") or [])
    skipped = list(summary.get("skipped") or [])
    failed = list(summary.get("failed") or [])

    lines: List[str] = []
    lines.append("# tvdatafeed Collect Report")
    lines.append("")
    lines.append("## Run Context")
    lines.append("")
    lines.append(f"- run_date_utc: {run_date}")
    lines.append(f"- run_at_utc: {run_at_utc}")
    lines.append(f"- run_year: {run_year}")
    lines.append(f"- github_run_id: {run_id}")
    if run_url and run_url != "-":
        lines.append(f"- github_run_url: {run_url}")
    lines.append("")

    lines.append("## Drive Pull (Yearly Parquet Restore)")
    lines.append("")
    lines.append(f"- status: {pull_report.get('status', '-')}")
    lines.append(f"- expected_count: {int(pull_report.get('expected_count', 0) or 0)}")
    lines.append(f"- listed_count: {int(pull_report.get('listed_count', 0) or 0)}")
    lines.append(f"- pulled_count: {int(pull_report.get('pulled_count', 0) or 0)}")
    lines.append(f"- remote_absent_count: {int(pull_report.get('remote_absent_count', 0) or 0)}")
    lines.append(f"- copy_missing_count: {int(pull_report.get('copy_missing_count', 0) or 0)}")
    lines.append(f"- failed_count: {int(pull_report.get('failed_count', 0) or 0)}")
    lines.append(f"- retries: {pull_report.get('retries', '-')}")
    lines.append(f"- remote_root: {pull_report.get('remote', '-')}")
    lines.append("")

    if pull_report.get("ls_error"):
        lines.append("### LS Error")
        lines.append("")
        lines.append("```text")
        lines.append(str(pull_report.get("ls_error", "")).strip())
        lines.append("```")
        lines.append("")

    _append_list(lines, "Pulled Files From GDrive", list(pull_report.get("pulled_files") or []))
    _append_list(lines, "Expected But Not On Remote (new targets)", list(pull_report.get("remote_absent_files") or []))
    _append_list(lines, "Copy Missing Files", list(pull_report.get("copy_missing_files") or []))

    lines.append("### Copy Failures")
    lines.append("")
    failed_files = list(pull_report.get("failed_files") or [])
    if failed_files:
        for item in failed_files:
            rel = item.get("file", "-")
            err = str(item.get("error", "")).strip()
            lines.append(f"- file: `{rel}`")
            lines.append("```text")
            lines.append(err if err else "(no error text)")
            lines.append("```")
    else:
        lines.append("- (none)")
    lines.append("")

    lines.append("## Collect Totals")
    lines.append("")
    lines.append(f"- ok: {totals['ok_count']}")
    lines.append(f"- skipped: {totals['skipped_count']}")
    lines.append(f"- failed: {totals['failed_count']}")
    lines.append(f"- rows_before_total: {totals['rows_before_total']}")
    lines.append(f"- rows_new_total: {totals['rows_new_total']}")
    lines.append(f"- rows_after_total: {totals['rows_after_total']}")
    lines.append(f"- deduped_total: {totals['deduped_total']}")
    lines.append(f"- net_growth: {totals['net_growth']}")
    lines.append("")

    if ok:
        lines.append("## Per Parquet Change")
        lines.append("")
        lines.append(
            "| symbol | tf | mode | before | new | after | deduped | delta | prev_last | new_first | new_last | after_last | overlap_rows | overlap_min |"
        )
        lines.append("|---|---|---|---:|---:|---:|---:|---:|---|---|---|---|---:|---:|")
        for item in ok:
            before = int(item.get("rows_before", 0) or 0)
            after = int(item.get("rows_after", 0) or 0)
            lines.append(
                "| {symbol} | {tf} | {mode} | {before} | {new} | {after} | {deduped} | {delta} | {prev_last} | {new_first} | {new_last} | {after_last} | {overlap_rows} | {overlap_min} |".format(
                    symbol=item.get("symbol", ""),
                    tf=item.get("timeframe", ""),
                    mode=item.get("mode", ""),
                    before=before,
                    new=int(item.get("fetched_rows", 0) or 0),
                    after=after,
                    deduped=int(item.get("deduped", 0) or 0),
                    delta=after - before,
                    prev_last=item.get("before_last_ts_iso") or "-",
                    new_first=item.get("fetched_first_ts_iso") or "-",
                    new_last=item.get("fetched_last_ts_iso") or "-",
                    after_last=item.get("after_last_ts_iso") or "-",
                    overlap_rows=int(item.get("overlap_rows", 0) or 0),
                    overlap_min=item.get("overlap_minutes", 0) or 0,
                )
            )
        lines.append("")

        lines.append("### Output Files")
        lines.append("")
        for item in ok:
            lines.append(f"- `{item.get('file', '-')}`")
        lines.append("")

    if skipped:
        lines.append("## Skipped")
        lines.append("")
        for item in skipped:
            lines.append(f"- {item}")
        lines.append("")

    if failed:
        lines.append("## Failed")
        lines.append("")
        for item in failed:
            lines.append(f"- {item}")
        lines.append("")

    if summary.get("error"):
        lines.append("## Summary Error")
        lines.append("")
        lines.append(f"- {summary['error']}")
        lines.append("")

    if pull_report.get("error"):
        lines.append("## Pull Report Error")
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
    parser.add_argument("--run-at-utc", default="")
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
    run_at_utc = str(args.run_at_utc).strip() or "-"

    out_md.write_text(
        _build_markdown(
            summary=summary,
            pull_report=pull_report,
            totals=totals,
            run_year=run_year,
            run_date=run_date,
            run_id=run_id,
            run_url=run_url,
            run_at_utc=run_at_utc,
        ),
        encoding="utf-8",
    )

    print(f"report_md={out_md}")
    print(json.dumps(totals, ensure_ascii=False))


if __name__ == "__main__":
    main()
