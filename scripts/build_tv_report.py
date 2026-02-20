#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


def _load_summary(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {"ok": [], "skipped": [], "failed": [], "error": "summary file not found"}
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return {"ok": [], "skipped": [], "failed": [], "error": "summary file is empty"}
    try:
        return json.loads(text)
    except Exception as exc:
        return {"ok": [], "skipped": [], "failed": [], "error": f"invalid JSON summary: {exc}"}


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
    }


def _build_markdown(summary: Dict[str, Any], totals: Dict[str, Any]) -> str:
    ok = list(summary.get("ok") or [])
    skipped = list(summary.get("skipped") or [])
    failed = list(summary.get("failed") or [])

    lines: List[str] = []
    lines.append("# tvdatafeed Collect Report")
    lines.append("")
    lines.append("## Totals")
    lines.append("")
    lines.append(f"- ok: {totals['ok_count']}")
    lines.append(f"- skipped: {totals['skipped_count']}")
    lines.append(f"- failed: {totals['failed_count']}")
    lines.append(f"- rows_before_total: {totals['rows_before_total']}")
    lines.append(f"- rows_new_total: {totals['rows_new_total']}")
    lines.append(f"- rows_after_total: {totals['rows_after_total']}")
    lines.append(f"- deduped_total: {totals['deduped_total']}")
    lines.append("")

    if ok:
        lines.append("## Per Parquet")
        lines.append("")
        lines.append("| symbol | tf | file | before | after | new | deduped | prev_last | new_first | new_last | overlap_rows | overlap_min |")
        lines.append("|---|---|---|---:|---:|---:|---:|---|---|---|---:|---:|")
        for item in ok:
            lines.append(
                "| {symbol} | {tf} | `{file}` | {before} | {after} | {new} | {deduped} | {prev_last} | {new_first} | {new_last} | {overlap_rows} | {overlap_min} |".format(
                    symbol=item.get("symbol", ""),
                    tf=item.get("timeframe", ""),
                    file=item.get("file", ""),
                    before=int(item.get("rows_before", 0) or 0),
                    after=int(item.get("rows_after", 0) or 0),
                    new=int(item.get("fetched_rows", 0) or 0),
                    deduped=int(item.get("deduped", 0) or 0),
                    prev_last=item.get("before_last_ts_iso") or "-",
                    new_first=item.get("fetched_first_ts_iso") or "-",
                    new_last=item.get("fetched_last_ts_iso") or "-",
                    overlap_rows=int(item.get("overlap_rows", 0) or 0),
                    overlap_min=item.get("overlap_minutes", 0) or 0,
                )
            )
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
        lines.append("## Error")
        lines.append("")
        lines.append(f"- {summary['error']}")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build detailed report artifacts from tvdatafeed_summary.json")
    parser.add_argument("--summary", default="tvdatafeed_summary.json")
    parser.add_argument("--out-json", default="tvdatafeed_report.json")
    parser.add_argument("--out-md", default="tvdatafeed_report.md")
    args = parser.parse_args()

    summary_path = Path(args.summary).resolve()
    out_json = Path(args.out_json).resolve()
    out_md = Path(args.out_md).resolve()

    summary = _load_summary(summary_path)
    ok = list(summary.get("ok") or [])
    skipped = list(summary.get("skipped") or [])
    failed = list(summary.get("failed") or [])
    totals = _totals(ok, skipped, failed)

    report = {
        "totals": totals,
        "summary": summary,
    }
    out_json.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    out_md.write_text(_build_markdown(summary, totals), encoding="utf-8")

    print(f"report_json={out_json}")
    print(f"report_md={out_md}")
    print(json.dumps(totals, ensure_ascii=False))


if __name__ == "__main__":
    main()

