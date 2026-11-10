"""Execute the actual workflow's mode-resolution shell and verify hourly coverage."""
from collections import Counter
import json
import os
from pathlib import Path
import re
import subprocess
import sys

import pytest


WORKFLOW = Path(__file__).resolve().parents[1]/'.github/workflows/tvdatafeed-collect.yml'


def workflow():
    return WORKFLOW.read_text()


def cron_hours(expression):
    minute, hour, dom, month, dow = expression.split()
    assert minute == '0' and (dom, month, dow) == ('*', '*', '*')
    hours = set()
    for term in hour.split(','):
        if term.startswith('*/'):
            hours.update(range(0, 24, int(term[2:])))
        elif '-' in term:
            a, b = map(int, term.split('-'))
            hours.update(range(a, b+1))
        else:
            hours.add(int(term))
    return hours


def test_every_utc_hour_has_one_schedule_and_major_remains_six_hourly():
    crons = re.findall(r'^    - cron: "([^"]+)"$', workflow(), re.M)
    assert len(crons) == 2
    major = next(c for c in crons if c == '0 */6 * * *')
    minor = next(c for c in crons if c != major)
    assert cron_hours(major) == {0, 6, 12, 18}
    assert len(cron_hours(minor)) == 20
    counts = Counter(hour for cron in crons for hour in cron_hours(cron))
    assert counts == Counter({hour: 1 for hour in range(24)})


@pytest.mark.parametrize('event,schedule,mode,hour,expected', [
    ('schedule', '0 */6 * * *', 'auto', '00', 'major'),
    ('schedule', '0 */6 * * *', 'auto', '07', 'major'),  # Delayed startup.
    ('schedule', '0 1-5,7-11,13-17,19-23 * * *', 'auto', '01', 'minor'),
    ('schedule', '0 1-5,7-11,13-17,19-23 * * *', 'auto', '06', 'minor'),
    ('workflow_dispatch', '', 'auto', '06', 'major'),
    ('workflow_dispatch', '', 'auto', '08', 'minor'),
    ('workflow_dispatch', '', 'major', '08', 'major'),
    ('workflow_dispatch', '', 'minor', '06', 'minor'),
])
def test_actual_mode_resolution_shell(tmp_path, event, schedule, mode, hour, expected):
    jobs = {'jobs': [
        {'source': 'tradingview', 'broker': 'TEST', 'symbol': 'XAUUSD', 'timeframe': '100R'},
        {'source': 'tv', 'broker': 'TEST', 'symbol': 'XAUUSD', 'timeframe': '10R'},
        {'source': 'tradingview', 'broker': 'TEST', 'symbol': 'XAUUSD', 'timeframe': '1000R'},
        {'source': 'tradingview', 'broker': 'TEST', 'symbol': 'XAUUSD', 'timeframe': '1m'},
        {'source': 'other', 'broker': 'TEST', 'symbol': 'XAUUSD', 'timeframe': '100R'},
    ]}
    config, env_path = tmp_path/'jobs.json', tmp_path/'github-env'
    config.write_text(json.dumps(jobs))
    block = workflow().split('      - name: Resolve run mode and effective config\n', 1)[1]
    block = re.split(r'^      - ', block, maxsplit=1, flags=re.M)[0]
    shell = block.split('        run: |\n', 1)[1]
    shell = '\n'.join(line[10:] if line.startswith('          ') else line for line in shell.splitlines())
    substitutions = {
        "github.event.inputs.config_path || 'config/collect_jobs.json'": str(config),
        'github.event_name': event, "github.event.schedule || ''": schedule,
        "github.event.inputs.run_mode || 'auto'": mode,
    }
    for key, value in substitutions.items():
        shell = shell.replace('${{ '+key+' }}', value)
    assert '${{' not in shell
    shell = shell.replace('mktemp /tmp/collect_jobs_minor.XXXXXX.json', f'mktemp {tmp_path}/minor.XXXXXX.json')
    shell = 'date() { printf "%s\\n" "'+hour+'"; }\n'+shell
    result = subprocess.run(['bash', '-euo', 'pipefail', '-c', shell],
        env={**os.environ, 'GITHUB_ENV': str(env_path),
             'PATH': str(Path(sys.executable).parent)+os.pathsep+os.environ.get('PATH', '')},
        capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    saved = dict(line.split('=', 1) for line in env_path.read_text().splitlines())
    assert saved['RUN_MODE'] == expected
    effective = json.loads(Path(saved['EFFECTIVE_CONFIG_PATH']).read_text())
    if expected == 'minor':
        assert len(effective['jobs']) == 3
        assert {j['timeframe'] for j in effective['jobs']} == {'10R', '100R', '1000R'}
    else:
        assert effective == jobs


def test_source_guard_is_enabled_and_evidence_precedes_price_publication():
    source = workflow()
    collect = source.split('      - name: Run simple tvdatafeed collector\n', 1)[1].split('\n      - ', 1)[0]
    assert '--range-source-policy protect --range-fallback missing-only' in collect
    guard = source.index('      - name: Preserve primary-write decisions and separate M1 fallback blocks')
    publish = source.index('      - name: Push updated tvdatafeed files to Drive (optional)')
    assert guard < publish
    publish_block = source[publish:].split('\n      - ', 1)[0]
    assert "steps.push_raw.outcome == 'success'" in publish_block
    assert "steps.push_range_guard.outcome == 'success'" in publish_block
    assert source.count('cancel-in-progress: false') == 1
