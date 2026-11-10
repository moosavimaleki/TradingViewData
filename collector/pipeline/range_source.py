"""Evidence about a range snapshot's resolution, without claiming tick truth.

The M1 replay matches an observed TradingView construction for phantomBars=False.
Timestamp precision alone never authorizes export. Unknown rows stay in the
annotated snapshot, and exports preserve contiguous source segments.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import asdict, dataclass

import numpy as np
import pandas as pd

from .normalize import normalize_frame

OHLC = ["open", "high", "low", "close"]
FINE_LABELS = {"subminute_candidate", "corroborated_candidate"}


@dataclass(frozen=True)
class SourcePolicy:
    window_bars: int = 8
    minimum_clock_fraction: float = .5
    minimum_price_mismatches: int = 3
    warmup_m1_bars: int = 20
    context_bars: int = 8

    def __post_init__(self):
        if self.window_bars < 2 or self.context_bars < 1 or self.warmup_m1_bars < 1:
            raise ValueError("Source evidence requires positive warmup/context and a multirow window")
        if not 0 < self.minimum_clock_fraction <= 1 or not 1 <= self.minimum_price_mismatches <= self.window_bars:
            raise ValueError("Invalid source evidence thresholds")


def replay_m1(minute: pd.DataFrame, width: float) -> pd.DataFrame:
    """Replay four events per M1; event labels are not recovered tick times."""
    current = None
    result, counts = [], Counter()
    epsilon = max(width*1e-7, 1e-12)
    for t, o, h, l, c in minute[["ts", *OHLC]].itertuples(index=False, name=None):
        for price in ((o, h, l, c) if c < o else (o, l, h, c)):
            if current is not None:
                upper, lower = max(current["high"], price), min(current["low"], price)
                if upper-lower <= width+epsilon:
                    current.update(high=upper, low=lower, close=price)
                    continue
                if price > current["high"]:
                    current["high"] = current["low"]+width
                    current["close"] = current["high"]
                else:
                    current["low"] = current["high"]-width
                    current["close"] = current["low"]
                result.append(current)
            ordinal = counts[t]
            counts[t] += 1
            current = {"ts": t+ordinal*.001, "open": price, "high": price, "low": price, "close": price}
    return pd.DataFrame(result, columns=["ts", *OHLC])


def _groups(frame):
    groups = {}
    for minute, part in frame.groupby(np.floor(frame.ts/60).astype("int64"), sort=False):
        groups[int(minute)] = part
    return groups


def _unique_contexts(frame, width):
    result = defaultdict(list)
    values = np.round(frame[["ts", *OHLC]].to_numpy(float), 12)
    for i in range(width, len(frame)):
        result[values[i-width:i+1].tobytes()].append(i)
    return result


def corroboration(current, previous, *, policy):
    """Match unique9-row price/time contexts across distinct collection runs."""
    result = np.zeros(len(current), bool)
    if previous is None or previous.empty or not FINE_LABELS.intersection(previous.source_class):
        return result
    if not previous.run_id.nunique() == current.run_id.nunique() == 1:
        return result
    if previous.run_id.iloc[0] == current.run_id.iloc[0]:
        return result
    if pd.Timestamp(previous.captured_at_UTC.iloc[0]) >= pd.Timestamp(current.captured_at_UTC.iloc[0]):
        return result
    old, new = _unique_contexts(previous, policy.context_bars), _unique_contexts(current, policy.context_bars)
    for key in old.keys() & new.keys():
        if len(old[key]) != 1 or len(new[key]) != 1:
            continue
        a, b = old[key][0], new[key][0]
        result[b] = previous.source_class.iloc[a] in FINE_LABELS and current.source_class.iloc[b] in FINE_LABELS
    return result


def classify_snapshot(raw_range, raw_m1, *, run_id, request_id, captured_at_UTC,
                      previous=None, policy=SourcePolicy()):
    received = normalize_frame(raw_range, drop_latest_candle=False, is_range=True)
    if not received.ts.is_monotonic_increasing:
        raise ValueError("Out-of-order source snapshot")
    if not received.empty and ((received.high < received[["open", "close", "low"]].max(axis=1)-1e-9).any()
                               or (received.low > received[["open", "close", "high"]].min(axis=1)+1e-9).any()):
        raise ValueError("Invalid range OHLC ordering")
    # The final potentially forming range bar is never included in exports.
    frame = received.iloc[:-1].reset_index(drop=True).copy()
    frame["source_row"] = np.arange(len(frame))
    if raw_range is not None and "bar_index" in raw_range and len(raw_range) == len(received):
        frame["bar_index"] = raw_range.bar_index.iloc[:-1].to_numpy()
    frame["run_id"], frame["request_id"] = run_id, request_id
    frame["captured_at_UTC"] = str(captured_at_UTC)
    frame["source_class"] = "unknown"
    frame["clock_subminute"] = (frame.ts % 60 >= 1-1e-5) & (abs(frame.ts-frame.ts.round()) < 1e-5)
    frame["m1_price_sequence_match"] = False
    frame["m1_timestamp_sequence_match"] = False
    frame["M1_span_covered"] = False
    frame["M1_span_contains_prices"] = False
    frame["reason"] = "M1 reference missing or insufficient"
    frame["copy_candidate"] = False
    summary = {"schema_version": 1, "run_id": run_id, "request_id": request_id,
               "captured_at_UTC": str(captured_at_UTC), "closed_rows": len(frame),
               "policy": asdict(policy), "certified_tick_true_rows": 0,
               "claim": "Resolution evidence only; candidate exports are not verified against independent ticks."}
    if frame.empty:
        summary.update(counts={}, segments=[], candidate_suffix=None, candidate_rows=0)
        return frame, summary
    widths = (frame.high-frame.low).to_numpy(float)
    width = float(np.median(widths))
    summary["median_range_price_width"] = width
    valid_width = width > 0 and np.isclose(widths, width, rtol=1e-6, atol=1e-12).all()
    if raw_m1 is not None and not raw_m1.empty and valid_width:
        minute = normalize_frame(raw_m1, drop_latest_candle=True)
        minute = minute[minute.faraz == 0].reset_index(drop=True)
        if len(minute) > policy.warmup_m1_bars and minute.ts.is_unique:
            # A native M1 reference must use exact UTC minute boundaries.
            if not np.allclose(minute.ts % 60, 0, rtol=0, atol=1e-6):
                raise ValueError("M1 reference is not aligned to UTC minute starts")
            # Missing M1 minutes, including session breaks, do not provide a
            # known price path. Reset the hypothesis and warm it up after every
            # discontinuity rather than learning false mismatches from a gap.
            segment = minute.ts.diff().ne(60).cumsum()
            replayed, warmed = [], set()
            for _, part in minute.groupby(segment, sort=False):
                replayed.append(replay_m1(part, width))
                warmed.update(part.ts.iloc[policy.warmup_m1_bars:].tolist())
            generated = pd.concat(replayed, ignore_index=True)
            generated_groups = _groups(generated)
            epsilon = max(width*1e-6, 1e-12)
            for minute_id, part in _groups(frame).items():
                replay = generated_groups.get(minute_id)
                if replay is None or minute_id*60 not in warmed or len(replay) != len(part):
                    continue
                same = np.allclose(part[OHLC], replay[OHLC], rtol=0, atol=epsilon)
                frame.loc[part.index, "m1_price_sequence_match"] = same
                if same:
                    frame.loc[part.index, "m1_timestamp_sequence_match"] = np.allclose(part.ts, replay.ts, rtol=0, atol=1e-5)
            mts, ml, mh = minute.ts.to_numpy(), minute.low.to_numpy(), minute.high.to_numpy()
            # Use a bar's start through the next range bar's start; never force
            # its entire OHLC into just the minute of its own timestamp.
            spans, contained = np.zeros(len(frame), bool), np.zeros(len(frame), bool)
            prices = frame[OHLC].to_numpy(float)
            for i, (start, following) in enumerate(zip(frame.ts, received.ts.iloc[1:])):
                first = np.floor(start/60)*60
                last = np.floor(following/60)*60
                a, b = np.searchsorted(mts, first), np.searchsorted(mts, last, side="right")
                covered = b-a == int((last-first)/60)+1 and first in warmed
                spans[i] = covered
                if covered:
                    contained[i] = ml[a:b].min() <= prices[i].min()+epsilon and mh[a:b].max() >= prices[i].max()-epsilon
            frame["M1_span_covered"], frame["M1_span_contains_prices"] = spans, contained
            covered = frame.M1_span_covered & frame.M1_span_contains_prices
            frame.loc[covered, "reason"] = "M1 covered; source resolution remains ambiguous"
            exact = covered & frame.m1_price_sequence_match & frame.m1_timestamp_sequence_match
            # Isolated one-row coincidences never establish a reconstruction
            # segment: require eight consecutive exact source rows.
            cuts = np.r_[0, np.flatnonzero(exact.to_numpy()[1:] != exact.to_numpy()[:-1])+1, len(frame)]
            for a, b in zip(cuts, cuts[1:]):
                if exact.iloc[a] and b-a >= policy.window_bars:
                    frame.loc[a:b-1, ["source_class", "reason"]] = ["m1_replay_match", "Sustained matching M1-replayed OHLC and timestamp sequences"]
            # Unknown gaps reset the rolling evidence; evidence from before an
            # M1 outage must never qualify the first bar after it.
            evidence_group = (~covered).cumsum()
            def rolling(values):
                return values.astype(int).groupby(evidence_group).transform(
                    lambda part: part.rolling(policy.window_bars, min_periods=policy.window_bars).sum())
            clock_count = rolling(frame.clock_subminute)
            price_differences = rolling(~frame.m1_price_sequence_match & covered)
            fine = (covered & ~exact & (clock_count >= policy.window_bars*policy.minimum_clock_fraction)
                    & (price_differences >= policy.minimum_price_mismatches))
            frame.loc[fine, ["source_class", "reason"]] = ["subminute_candidate", "Subminute clocks plus repeated price-sequence differences from M1 replay"]
            frame.loc[~covered, "reason"] = "M1 span missing, warmup, incomplete end or prices outside the covered envelope"
    elif not valid_width:
        frame["reason"] = "Range width varies; source semantics need review"
    if previous is not None:
        required = {"source_class", "run_id", "captured_at_UTC", "ts", *OHLC}
        if not required.issubset(previous):
            raise ValueError("Previous state lacks provenance or quality labels")
        repeated = corroboration(frame, previous, policy=policy)
        frame.loc[repeated, ["source_class", "reason"]] = ["corroborated_candidate", "Unique price/time context also occurred as a candidate in an earlier collection run"]
    frame["copy_candidate"] = frame.source_class.isin(FINE_LABELS)
    cuts = np.r_[0, np.flatnonzero(frame.source_class.to_numpy()[1:] != frame.source_class.to_numpy()[:-1])+1, len(frame)]
    segments = [{"source_class": frame.source_class.iloc[a], "first_source_row": int(a), "last_source_row": int(b-1),
                 "rows": int(b-a), "first_UTC": pd.Timestamp(frame.ts.iloc[a], unit="s", tz="UTC").isoformat(),
                 "last_UTC": pd.Timestamp(frame.ts.iloc[b-1], unit="s", tz="UTC").isoformat()}
                for a, b in zip(cuts, cuts[1:])]
    # Report a conservative uninterrupted candidate tail, if it exists. An
    # unknown row near the incomplete M1 end means there is no such suffix.
    eligible = frame.copy_candidate.to_numpy()
    suffix = None
    if eligible[-1]:
        excluded = np.flatnonzero(~eligible)
        start = int(excluded[-1]+1) if len(excluded) else 0
        suffix = {"first_source_row": start, "rows": len(frame)-start,
                  "first_UTC": pd.Timestamp(frame.ts.iloc[start], unit="s", tz="UTC").isoformat(),
                  "last_UTC": pd.Timestamp(frame.ts.iloc[-1], unit="s", tz="UTC").isoformat()}
    summary.update(counts={k: int(v) for k, v in frame.source_class.value_counts().items()},
                   candidate_rows=int(eligible.sum()), segments=segments, candidate_suffix=suffix)
    return frame, summary
