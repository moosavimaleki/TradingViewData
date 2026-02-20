# Simple Collector (tvdatafeed)

این اسکریپت یک کلکتور ساده و مستقل است که:
- `config/collect_jobs.json` را می‌خواند.
- فقط سورس `tradingview` را با `tvdatafeed` (بدون proxy) دانلود می‌کند.
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
  --max-bars 5000
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

- تایم‌فریم‌هایی مثل `100R` توسط `tvdatafeed` پشتیبانی نمی‌شوند و `skip` می‌شوند.
