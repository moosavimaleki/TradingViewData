"""Keep M1-replayed/unknown range observations out of the primary archive.

An accepted update is one contiguous subminute-candidate block joined through
a unique eight-bar price/time context. M1 fallback blocks are separate files
and may cover only history outside the primary archive's known time extent.
Candidate is resolution evidence, not a certificate of native ticks.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from .normalize import normalize_frame
from .range_source import FINE_LABELS, OHLC, classify_snapshot
from .storage import _write_parquet_atomic, _row_to_dict


def digest(path):
    if not path.exists():
        return None
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def blocks(mask, minimum=8):
    mask = np.asarray(mask, dtype=bool)
    if not len(mask):
        return []
    cuts = np.r_[0, np.flatnonzero(mask[1:] != mask[:-1])+1, len(mask)]
    return [(int(a), int(b)) for a, b in zip(cuts, cuts[1:]) if mask[a] and b-a >= minimum]


def contexts(frame, width=8):
    values = np.round(frame[['ts', *OHLC]].to_numpy(float), 8)
    found = {}
    for end in range(width-1, len(frame)):
        key = values[end-width+1:end+1].tobytes()
        found.setdefault(key, []).append(end)
    return found


def plan_update(current, annotated, *, overlap_bars=300, context_bars=8):
    """Plan a primary update without modifying inputs or stitching fine islands."""
    current = normalize_frame(current, drop_latest_candle=False, is_range=True)
    if not current.ts.is_monotonic_increasing or not annotated.ts.is_monotonic_increasing:
        raise ValueError('Range guard refuses an out-of-order snapshot')
    eligible = annotated.source_class.isin(FINE_LABELS).to_numpy()
    segments = []
    for a, b in blocks(eligible, context_bars):
        if a and annotated.ts.iloc[a] == annotated.ts.iloc[a-1]:
            stamp = annotated.ts.iloc[a]
            while a < b and annotated.ts.iloc[a] == stamp:
                a += 1
        if b < len(annotated) and annotated.ts.iloc[b-1] == annotated.ts.iloc[b]:
            stamp = annotated.ts.iloc[b-1]
            while b > a and annotated.ts.iloc[b-1] == stamp:
                b -= 1
        if b-a >= context_bars:
            segments.append((a, b))
    if current.empty:
        if not segments:
            return None, {'decision': 'preserve_primary', 'reason': 'No contiguous subminute candidate block'}
        # Starting a new archive at the latest fine block never concatenates
        # separated islands across unknown/coarse observations.
        a, b = segments[-1]
        result = normalize_frame(annotated.iloc[a:b], drop_latest_candle=False, is_range=True)
        return result, {'decision': 'initialize_candidate', 'accepted_source_rows': [a, b-1],
                        'accepted_rows': len(result), 'replaced_rows': 0, 'replacement_start_ts': None}
    if not segments:
        return None, {'decision': 'preserve_primary', 'reason': 'Only M1 replay or unknown observations'}
    cutoff = float(current.ts.iloc[-min(len(current), max(1, int(overlap_bars)))])
    # Include enough context before the overlap but never replace that prefix.
    context_start = max(0, len(current)-max(1, int(overlap_bars))-context_bars)
    old_contexts = contexts(current.iloc[context_start:].reset_index(drop=True), context_bars)
    source_contexts = contexts(annotated, context_bars)
    for a, b in reversed(segments):
        part = annotated.iloc[a:b]
        if part.ts.iloc[-1] < current.ts.iloc[-1]:
            continue  # Never shorten a previously saved tail.
        anchors = []
        for key, old_ends in old_contexts.items():
            new_ends = source_contexts.get(key, [])
            if len(old_ends) != 1 or len(new_ends) != 1:
                continue
            old_end, new_end = context_start+old_ends[0], new_ends[0]
            if not a <= new_end-context_bars+1 <= new_end < b:
                continue
            stamp = float(current.ts.iloc[old_end])
            if stamp < cutoff:
                continue
            # Never splice halfway through a shared timestamp group. A full
            # source second's rows must remain in the original series order.
            if old_end+1 < len(current) and current.ts.iloc[old_end+1] == stamp:
                continue
            if new_end+1 < len(annotated) and annotated.ts.iloc[new_end+1] == stamp:
                continue
            anchors.append((old_end, new_end))
        if not anchors:
            continue
        old_end, new_end = max(anchors)
        suffix = normalize_frame(annotated.iloc[new_end+1:b], drop_latest_candle=False, is_range=True)
        if suffix.empty:
            continue
        result = pd.concat([current.iloc[:old_end+1], suffix], ignore_index=True)
        if not result.ts.is_monotonic_increasing:
            raise ValueError('Range guard produced a nonmonotonic seam')
        if result.equals(current):
            return None, {'decision': 'preserve_primary', 'reason': 'Accepted candidate equals existing archive'}
        return result, {'decision': 'replace_candidate_suffix', 'accepted_source_rows': [new_end+1, b-1],
                        'accepted_rows': len(suffix), 'replaced_rows': len(current)-old_end-1,
                        'replacement_start_ts': float(suffix.ts.iloc[0]),
                        'anchor_old_end': old_end, 'anchor_source_end': new_end,
                        'anchor_rows': context_bars, 'configured_overlap_start_ts': cutoff}
    return None, {'decision': 'preserve_primary',
                  'reason': 'No unique complete candidate context joins the existing tail inside the overlap'}


def guarded_save(path, current, raw, minute, *, folder, meta, overlap_bars=300,
                 fallback='missing-only', reference_error=None):
    """Write evidence before a protected primary update; fallback never overwrites it."""
    if fallback not in ('missing-only', 'none'):
        raise ValueError('Unsupported range fallback policy')
    path, folder = Path(path), Path(folder)
    folder.mkdir(parents=True, exist_ok=False)
    annotated, evidence = classify_snapshot(raw, minute, run_id=meta['run_id'],
        request_id=meta.get('request_id', 'collector'), captured_at_UTC=meta['captured_at_UTC'])
    current = normalize_frame(current, drop_latest_candle=False, is_range=True)
    planned, decision = plan_update(current, annotated, overlap_bars=overlap_bars)
    annotated['broker'], annotated['symbol'], annotated['timeframe'] = meta['broker'], meta['symbol'], meta['timeframe']
    annotated.to_parquet(folder/'snapshot.parquet', index=False, compression='zstd')
    fallback_exports = []
    if fallback == 'missing-only':
        absent = np.ones(len(annotated), dtype=bool) if current.empty else (
            (annotated.ts < current.ts.iloc[0]) | (annotated.ts > current.ts.iloc[-1])).to_numpy()
        mask = annotated.source_class.eq('m1_replay_match').to_numpy() & absent
        for a, b in blocks(mask):
            target = folder/f'fallback-m1-{a:06d}-{b-1:06d}.parquet'
            annotated.iloc[a:b].to_parquet(target, index=False, compression='zstd')
            fallback_exports.append({'file': str(target), 'rows': b-a, 'sha256': digest(target),
                                     'first_ts': float(annotated.ts.iloc[a]), 'last_ts': float(annotated.ts.iloc[b-1])})
    before_sha = digest(path)
    changed = planned is not None
    reference_sha = None
    if minute is not None:
        normalized_reference = normalize_frame(minute, drop_latest_candle=False)
        reference_sha = hashlib.sha256(pd.util.hash_pandas_object(
            normalized_reference, index=False).to_numpy().tobytes()).hexdigest()
    report = {**evidence, **meta, **decision, 'policy': 'protect-primary-v1',
              'reference_error': reference_error, 'fallback_policy': fallback,
              'reference_rows': len(minute) if minute is not None else 0,
              'normalized_reference_sha256': reference_sha,
              'fallback_exports': fallback_exports, 'primary_file': str(path),
              'before_sha256': before_sha, 'primary_modified': False,
              'claim': 'Subminute candidates only; no independent tick-truth certificate. M1 fallback is separate.'}
    report_path = folder/'report.json'
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str))
    if changed:
        _write_parquet_atomic(path, planned)
    else:
        planned = current
    report.update(primary_modified=changed, after_sha256=digest(path), rows_after=len(planned))
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str))
    return {'rows_before': len(current), 'rows_after': len(planned), 'deduped': 0,
            'replaced_rows': decision.get('replaced_rows', 0),
            'replacement_start_ts': decision.get('replacement_start_ts'), 'merge_mode': 'source_guard',
            'after_last_row': _row_to_dict(planned.iloc[-1]) if len(planned) else None,
            'primary_modified': changed, 'source_guard': {**decision, 'report': str(report_path),
                'counts': evidence['counts'], 'fallback_rows': sum(r['rows'] for r in fallback_exports),
                'reference_error': reference_error}}
