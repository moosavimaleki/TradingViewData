# Simple Collector (tvdatafeed + TradingView WS for range bars)

این اسکریپت یک کلکتور ساده و مستقل است که:
- `config/collect_jobs.json` را می‌خواند.
- فقط سورس `tradingview` را دانلود می‌کند.
- برای time-barها از `tvdatafeed` استفاده می‌کند.
- برای range-barها مثل `100R` از TradingView websocket مستقیم استفاده می‌کند (بدون proxy و بدون fastpass).
- هر اجرا با `overlap` داده‌ی جدید را می‌گیرد و در همان فایل merge/update می‌کند.

## نصب

```bash
pip install --upgrade --no-cache-dir git+https://github.com/rongardF/tvdatafeed.git
```

## اجرا

```bash
python collector/simple_tvdatafeed_collector.py \
  --config config/collect_jobs.json \
  --data-root data \
  --overlap-bars 30 \
  --initial-bars 5000 \
  --max-bars 5000 \
  --range-overlap-bars 300 \
  --range-initial-bars 2000 \
  --range-max-bars 12000
```

## مسیر ذخیره‌سازی

```
data/tradingview/<BROKER>/<TIMEFRAME>/<SYMBOL>/data.csv
```

مثال:
```
data/tradingview/BLACKBULL/1m/XAUUSD/data.csv
```

## نکته

- range-barهایی مثل `100R` دیگر `skip` نمی‌شوند و با WS مستقیم گرفته می‌شوند.
- برای range-bar، آخرین کندل قبل از ذخیره حذف می‌شود (چون معمولا هنوز unstable است).
- برای لاگ کامل websocket می‌توانی قبل از اجرا `TV_WS_DEBUG=1` بگذاری.

## ذخیره سالانه Parquet

برای ذخیره‌ی سالانه (یک فایل برای سال اجرای job) از این اسکریپت استفاده کن:

```bash
python collector/yearly_candles_store.py \
  --broker BLACKBULL \
  --timeframe 1h \
  --symbol EURUSD \
  --base-dir data/tradingview
```

مسیر خروجی:
`data/tradingview/{BROKER}/{TIMEFRAME}/{SYMBOL}/{RUN_YEAR}.parquet`
