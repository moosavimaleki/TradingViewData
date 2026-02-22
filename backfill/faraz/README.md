# Faraz Backfill

این پوشه دو اسکریپت دارد:

1. `backfill_from_jobs.py`
- ورودی: `config/collect_jobs.json`
- فقط تایم‌فریم‌های non-range را پردازش می‌کند.
- داده را از Faraz می‌گیرد و در مسیر زیر به‌صورت سالیانه Parquet ذخیره می‌کند:
  - `data/faraz/{BROKER}/{TIMEFRAME}/{SYMBOL}/{YEAR}.parquet`

2. `prepend_from_faraz.py`
- ورودی: فایل map (نمونه: `config/backfill_prepend_maps.example.json`)
- برای هر map، قدیمی‌ترین `ts` مقصد را پیدا می‌کند.
- فقط کندل‌های قدیمی‌تر Faraz را prepend می‌کند.
- خروجی را بر اساس سال کندل داخل مقصد ذخیره می‌کند:
  - `data/tradingview/{BROKER}/{TIMEFRAME}/{SYMBOL}/{YEAR}.parquet`

## نیازمندی

- کوکی Faraz در env:
  - `FARAZ_COOKIE_STRING` (یا `FARAZ_COOKIES`)

## اجرای اسکریپت 1

```bash
python backfill/faraz/backfill_from_jobs.py \
  --config config/collect_jobs.json \
  --data-root data \
  --faraz-brokers FXCM,FOREXCOM,OANDA \
  --start 2017-01-01T00:00:00Z
```

## اجرای اسکریپت 2

```bash
cp config/backfill_prepend_maps.example.json config/backfill_prepend_maps.json

python backfill/faraz/prepend_from_faraz.py \
  --map-config config/backfill_prepend_maps.json \
  --data-root data
```
