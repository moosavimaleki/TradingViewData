from __future__ import annotations

import argparse
import json

import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

from collector.pipeline.normalize import normalize_frame
from collector.pipeline.range_guard import guarded_save, plan_update
from collector.pipeline.range_source import replay_m1


BASE = 1794232800.


def minute_reference(n=140):
    opening = 5000-np.arange(n)*2
    return pd.DataFrame({'ts': BASE+np.arange(n)*60, 'open': opening, 'high': opening+1.4,
                         'low': opening-1.6, 'close': opening-1.2, 'volume': 100.})


def fine_reference():
    raw = replay_m1(minute_reference(), 1.)
    raw['volume'] = 20.
    raw['ts'] = np.floor(raw.ts/60)*60+12+np.rint(raw.ts.mod(60)*1000)*10
    raw['open'] = (raw.high+raw.low)/2+.01
    return raw


def meta():
    return {'run_id': 'run1', 'request_id': 'r1', 'broker': 'TEST', 'symbol': 'XAUUSD',
            'timeframe': '100R', 'captured_at_UTC': '2026-11-10T00:00:00Z'}


def simple(n=40):
    d = pd.DataFrame({'ts': BASE+np.arange(n), 'open': np.arange(n)+100.,
                      'high': np.arange(n)+101., 'low': np.arange(n)+100.,
                      'close': np.arange(n)+101., 'volume': 10., 'faraz': 0})
    d['source_class'] = 'subminute_candidate'
    return d


def save(tmp_path, old, raw, minute, **kwargs):
    path = tmp_path/'2026.parquet'
    if old is not None:
        old.to_parquet(path, index=False)
    current = old if old is not None else pd.DataFrame()
    return path, guarded_save(path, current, raw, minute, folder=tmp_path/'guard', meta=meta(), **kwargs)


def test_m1_snapshot_cannot_overwrite_old_archive_and_stages_missing_tail_only(tmp_path):
    raw = replay_m1(minute_reference(), 1.)
    raw['volume'] = 1.
    old = normalize_frame(raw.iloc[:200], drop_latest_candle=False, is_range=True)
    path, result = save(tmp_path, old, raw, minute_reference())
    assert not result['primary_modified']
    assert result['source_guard']['counts']['m1_replay_match'] > 100
    assert_frame_equal(pd.read_parquet(path), old)
    report = json.loads((tmp_path/'guard/report.json').read_text())
    assert report['before_sha256'] == report['after_sha256']
    assert report['fallback_exports']
    for record in report['fallback_exports']:
        fallback = pd.read_parquet(record['file'])
        assert fallback.ts.min() > old.ts.max()
        assert fallback.source_class.eq('m1_replay_match').all()


def test_first_coarse_download_is_only_separate_labelled_fallback(tmp_path):
    raw = replay_m1(minute_reference(), 1.)
    path, result = save(tmp_path, None, raw, minute_reference())
    assert not path.exists() and not result['primary_modified']
    assert result['source_guard']['fallback_rows'] > 0
    assert (tmp_path/'guard/snapshot.parquet').exists()


@pytest.mark.parametrize('old_present', [True, False])
def test_no_reference_cannot_authorize_primary_write_or_m1_fallback(tmp_path, old_present):
    raw = fine_reference()
    old = normalize_frame(raw.iloc[:50], drop_latest_candle=False, is_range=True) if old_present else None
    path, result = save(tmp_path, old, raw, None, reference_error='M1 unavailable')
    assert not result['primary_modified'] and result['source_guard']['fallback_rows'] == 0
    assert path.exists() == old_present
    if old_present:
        assert_frame_equal(pd.read_parquet(path), old)


def test_first_fine_download_saves_one_contiguous_candidate_block(tmp_path):
    path, result = save(tmp_path, None, fine_reference(), minute_reference())
    assert path.exists() and result['primary_modified']
    assert result['source_guard']['decision'] == 'initialize_candidate'
    a, b = result['source_guard']['accepted_source_rows']
    annotated = pd.read_parquet(tmp_path/'guard/snapshot.parquet')
    assert_frame_equal(pd.read_parquet(path), normalize_frame(annotated.iloc[a:b+1],
        drop_latest_candle=False, is_range=True))
    assert annotated.iloc[a:b+1].copy_candidate.all()


def test_fallback_can_be_disabled(tmp_path):
    path, result = save(tmp_path, None, replay_m1(minute_reference(), 1.), minute_reference(), fallback='none')
    assert not path.exists() and result['source_guard']['fallback_rows'] == 0


def test_seam_replaces_only_candidate_suffix_with_unique_matching_context():
    incoming = simple()
    old = normalize_frame(incoming.iloc[:30], drop_latest_candle=False, is_range=True)
    old.loc[28:, ['open', 'high', 'low', 'close']] += 10
    planned, decision = plan_update(old, incoming, overlap_bars=12)
    assert decision['decision'] == 'replace_candidate_suffix'
    assert decision['replaced_rows'] == 2 and decision['anchor_rows'] == 8
    assert_frame_equal(planned.iloc[:28].reset_index(drop=True), old.iloc[:28].reset_index(drop=True))
    assert_frame_equal(planned, normalize_frame(incoming, drop_latest_candle=False, is_range=True))


def test_cannot_downgrade_or_shorten_tail_even_with_matching_prices():
    incoming = simple()
    old = normalize_frame(incoming.iloc[:30], drop_latest_candle=False, is_range=True)
    incoming.loc[20:, 'source_class'] = 'm1_replay_match'
    planned, decision = plan_update(old, incoming)
    assert planned is None and decision['decision'] == 'preserve_primary'


def test_identical_prices_with_shifted_time_are_not_a_seam():
    incoming = simple()
    old = normalize_frame(incoming.iloc[:30], drop_latest_candle=False, is_range=True)
    incoming['ts'] += .25
    planned, _ = plan_update(old, incoming)
    assert planned is None


def test_fine_islands_are_not_stitched_over_unknown_rows():
    incoming = simple()
    incoming.loc[15:24, 'source_class'] = 'unknown'
    planned, decision = plan_update(pd.DataFrame(), incoming)
    assert decision['accepted_source_rows'] == [25, 39]
    assert len(planned) == 15
    old = normalize_frame(incoming.iloc[:12], drop_latest_candle=False, is_range=True)
    planned, decision = plan_update(old, incoming)
    assert decision['accepted_source_rows'][1] == 14
    assert len(planned) == 15  # Stops at the first unknown boundary.


def test_candidate_from_outside_configured_overlap_cannot_rewrite_history():
    incoming = simple()
    old = normalize_frame(incoming.iloc[:30], drop_latest_candle=False, is_range=True)
    old.loc[20:, ['open', 'high', 'low', 'close']] += 10
    planned, _ = plan_update(old, incoming, overlap_bars=5)
    assert planned is None


def test_classification_boundaries_cannot_split_a_shared_timestamp_group():
    incoming = simple()
    incoming.loc[10, 'ts'] = incoming.ts.iloc[9]
    incoming.loc[:9, 'source_class'] = 'unknown'
    incoming.loc[30, 'ts'] = incoming.ts.iloc[29]
    incoming.loc[30:, 'source_class'] = 'unknown'
    planned, decision = plan_update(pd.DataFrame(), incoming)
    assert decision['accepted_source_rows'] == [11, 28]
    assert len(planned) == 18


def test_collector_default_protection_blocks_m1_before_primary_write(tmp_path, monkeypatch, capsys):
    from collector import simple_tvdatafeed_collector as collector

    raw, minute = replay_m1(minute_reference(), 1.), minute_reference()
    raw['volume'] = 1.
    config = tmp_path/'jobs.json'
    config.write_text(json.dumps({'jobs': [{'source': 'tradingview', 'broker': 'TEST',
                                           'symbol': 'XAUUSD', 'timeframe': '100R'}]}))
    data_root = tmp_path/'data'
    path = data_root/'tradingview/TEST/100R/XAUUSD/2026.parquet'
    path.parent.mkdir(parents=True)
    old = normalize_frame(raw.iloc[:250], drop_latest_candle=False, is_range=True)
    old.to_parquet(path, index=False)
    original = path.read_bytes()

    class Fetcher:
        def __init__(self, **kwargs):
            self.archive = kwargs['raw_archive']

        def fetch_latest_range(self, **kwargs):
            with self.archive.request(source='tradingview', symbol=kwargs['symbol'], broker=kwargs['broker'],
                                      timeframe=kwargs['timeframe'], requested_bars=kwargs['n_bars']) as request:
                request.frame(raw)
            return raw

        def fetch_latest_time(self, **kwargs):
            with self.archive.request(source='tradingview', symbol=kwargs['symbol'], broker=kwargs['broker'],
                                      timeframe='1', requested_bars=kwargs['n_bars']) as request:
                request.frame(minute)
            return minute

    monkeypatch.setenv('RUN_YEAR', '2026')
    monkeypatch.setattr(collector, 'TvDatafeedFetcher', lambda **kwargs: None)
    monkeypatch.setattr(collector, 'TradingViewWSFetcher', Fetcher)
    monkeypatch.setattr(collector, '_parse_args', lambda: argparse.Namespace(config=str(config),
        data_root=str(data_root), log_level='INFO', range_overlap_bars=30,
        range_initial_bars=1000, range_max_bars=1000))  # No opt-in: protect is the default.
    collector.main()
    assert path.read_bytes() == original
    summary = json.loads(capsys.readouterr().out)
    assert not summary['ok'] and not summary['failed']
    guard = summary['skipped'][0]['details']['source_guard']
    assert guard['counts']['m1_replay_match'] > 100 and guard['fallback_rows'] > 0
