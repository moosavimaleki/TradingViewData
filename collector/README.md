# Collector

ساختار ساده و لایه‌ای:

- `simple_tvdatafeed_collector.py`: Runner
- `pipeline/config.py`: خواندن jobها و نرمال‌سازی تنظیمات
- `pipeline/fetchers.py`: دریافت time-bar با `tvdatafeed`
- `pipeline/ws_fetcher.py`: دریافت range-bar مثل `100R` با websocket
- `pipeline/normalize.py`: نرمال‌سازی دیتافریم (تبدیل `ts` به epoch-ms و حذف آخرین کندل)
- `pipeline/storage.py`: خواندن/ادغام/ذخیره Parquet سالانه

فرمت خروجی:

`data/tradingview/{BROKER}/{TIMEFRAME}/{SYMBOL}/{RUN_YEAR}.parquet`

مثال اجرا:

```bash
python collector/simple_tvdatafeed_collector.py \
  --config config/collect_jobs.json \
  --data-root data
```

