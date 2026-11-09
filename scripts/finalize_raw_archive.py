#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from collector.pipeline.raw_archive import finalize_archive


def main():
    parser = argparse.ArgumentParser(description="Seal and verify raw archives, including interrupted runs")
    parser.add_argument("--raw-root", required=True, type=Path)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    runs = sorted(args.raw_root.glob("tradingview/*/*/metadata.json"))
    if not runs:
        raise SystemExit("No raw archive was created; refusing to publish processed data")
    for metadata in runs:
        print(json.dumps(finalize_archive(metadata.parent)))


if __name__ == "__main__":
    main()
