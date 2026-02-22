#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional
from zoneinfo import ZoneInfo

RUN_TABLE_START = "<!-- RUN_TABLE_START -->"
RUN_TABLE_END = "<!-- RUN_TABLE_END -->"

RUN_AT_RE = re.compile(r"^- run_at_utc:\s*(.+?)\s*$", re.MULTILINE)
PULL_STATUS_RE = re.compile(r"^- status:\s*(.+?)\s*$", re.MULTILINE)
FAILED_RE = re.compile(r"^- failed:\s*(\d+)\s*$", re.MULTILINE)


@dataclass
class ReportRow:
    filename: str
    rel_path: str
    run_at_utc: str
    run_at_dt: Optional[datetime]
    status: str


def _parse_run_at(text: str, path: Path) -> tuple[str, Optional[datetime]]:
    m = RUN_AT_RE.search(text)
    if m:
        raw = m.group(1).strip()
        try:
            return raw, datetime.fromisoformat(raw.replace("Z", "+00:00"))
        except Exception:
            return raw, None

    stem = path.stem
    try:
        dt = datetime.strptime(stem, "%Y-%m-%dT%H-%M-%SZ").replace(tzinfo=timezone.utc)
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ"), dt
    except Exception:
        return "-", None


def _parse_status(text: str) -> str:
    collect_failed = None
    collect_idx = text.find("## Collect Totals")
    if collect_idx >= 0:
        m = FAILED_RE.search(text[collect_idx:])
        if m:
            collect_failed = int(m.group(1))

    pull_status = None
    pull_idx = text.find("## Drive Pull")
    if pull_idx >= 0:
        m = PULL_STATUS_RE.search(text[pull_idx:])
        if m:
            pull_status = m.group(1).strip().lower()

    failed_pull_states = {"ls_failed", "copy_failed", "copy_incomplete"}

    if collect_failed is not None and collect_failed > 0:
        return "failed"
    if pull_status in failed_pull_states:
        return "failed"
    if collect_failed == 0:
        return "success"
    if pull_status in {"ok", "skipped"}:
        return "success"
    return "unknown"


def _collect_rows(reports_dir: Path, limit: int) -> List[ReportRow]:
    rows: List[ReportRow] = []
    for path in sorted(reports_dir.glob("*.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        run_at_utc, run_at_dt = _parse_run_at(text, path)
        status = _parse_status(text)
        try:
            rel_path = path.resolve().relative_to(Path.cwd().resolve()).as_posix()
        except Exception:
            rel_path = f"{reports_dir.name}/{path.name}"

        rows.append(
            ReportRow(
                filename=path.name,
                rel_path=rel_path,
                run_at_utc=run_at_utc,
                run_at_dt=run_at_dt,
                status=status,
            )
        )

    rows.sort(
        key=lambda x: (
            x.run_at_dt if x.run_at_dt is not None else datetime.fromtimestamp(0, tz=timezone.utc),
            x.filename,
        ),
        reverse=True,
    )
    return rows[: max(1, int(limit))]


def _build_table(rows: List[ReportRow], repo_base_url: str) -> str:
    base = repo_base_url.rstrip("/")

    def status_badge(status: str) -> str:
        value = (status or "").strip().lower()
        if value == "success":
            return "✅ `success`"
        if value == "failed":
            return "❌ `failed`"
        return "❔ `unknown`"

    def to_tehran(ts: str) -> str:
        raw = (ts or "-").strip()
        if raw == "-" or not raw:
            return "-"
        try:
            dt_utc = datetime.fromisoformat(raw.replace("Z", "+00:00"))
            if dt_utc.tzinfo is None:
                dt_utc = dt_utc.replace(tzinfo=timezone.utc)
            dt_tehran = dt_utc.astimezone(ZoneInfo("Asia/Tehran"))
            return f"`{dt_tehran.strftime('%Y-%m-%d')}` `{dt_tehran.strftime('%H:%M:%S')}`"
        except Exception:
            if "T" in raw:
                d, t = raw.split("T", 1)
                return f"`{d}` `{t}`"
            return f"`{raw}`"

    lines: List[str] = []
    lines.append("## 🕒 آخرین اجراها")
    lines.append("")
    lines.append("| گزارش | وضعیت | زمان اجرا (تهران) |")
    lines.append("|---|---|---|")
    for row in rows:
        url = f"{base}/blob/main/{row.rel_path}"
        lines.append(f"| 📄 [{row.filename}]({url}) | {status_badge(row.status)} | {to_tehran(row.run_at_utc)} |")
    if not rows:
        lines.append("| - | ❔ `unknown` | - |")
    lines.append("")
    return "\n".join(lines)


def _replace_or_append_section(readme: str, section: str) -> str:
    block = f"{RUN_TABLE_START}\n{section}\n{RUN_TABLE_END}"
    if RUN_TABLE_START in readme and RUN_TABLE_END in readme:
        pattern = re.compile(
            re.escape(RUN_TABLE_START) + r".*?" + re.escape(RUN_TABLE_END),
            flags=re.DOTALL,
        )
        return pattern.sub(block, readme)

    text = readme.rstrip()
    if text:
        text += "\n\n"
    return text + block + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Update README with last N report links.")
    parser.add_argument("--readme", default="README.md")
    parser.add_argument("--reports-dir", default="artifacts/tvdatafeed")
    parser.add_argument("--repo-base-url", required=True, help="e.g. https://github.com/owner/repo")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    readme_path = Path(args.readme).resolve()
    reports_dir = Path(args.reports_dir).resolve()

    if not readme_path.exists():
        raise SystemExit(f"README not found: {readme_path}")

    rows = _collect_rows(reports_dir=reports_dir, limit=int(args.limit))
    section = _build_table(rows=rows, repo_base_url=str(args.repo_base_url))

    readme_text = readme_path.read_text(encoding="utf-8")
    updated = _replace_or_append_section(readme_text, section)
    readme_path.write_text(updated, encoding="utf-8")

    print(f"updated_readme={readme_path}")
    print(f"rows={len(rows)}")


if __name__ == "__main__":
    main()
