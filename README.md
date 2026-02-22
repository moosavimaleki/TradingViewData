# TradingViewData

این پروژه برای جمع‌آوری و به‌روزرسانی دیتای بازار از TradingView ساخته شده است.

## ✨ نمای کلی
- منبع داده: `TradingView`
- خروجی: فایل‌های سالانه `Parquet`
- هدف: نگهداری دیتای سبک، قابل‌همگام‌سازی و قابل‌به‌روزرسانی

## 📥 دریافت داده

- Google Drive (دیتای اصلی):
  - https://drive.google.com/drive/folders/189HIU2eouf3Ftzil_0Nmm1fk1yAgs61B?usp=sharing

## 🗂️ ساختار ذخیره‌سازی

- مسیر فایل‌ها به‌صورت سالانه ذخیره می‌شود:
  - `data/tradingview/{BROKER}/{TIMEFRAME}/{SYMBOL}/{RUN_YEAR}.parquet`

## ⏱️ زمان‌بندی اجرا

- هر ۳ ساعت: اجرای `minor` (فقط تایم‌فریم‌های رنج: `10R`, `100R`, `1000R`)
- هر ۶ ساعت: اجرای `major` (همه تایم‌فریم‌ها + گزارش کامل)

## 🧱 Faraz Backfill

- بک‌فیل خام از روی `config/collect_jobs.json`:
  - `python backfill/faraz/backfill_from_jobs.py --config config/collect_jobs.json --data-root data --faraz-brokers FXCM,FOREXCOM,OANDA --start 2017-01-01T00:00:00Z`
- prepend کردن دیتای Faraz قبل از دیتای TradingView با map config:
  - `python backfill/faraz/prepend_from_faraz.py --map-config config/backfill_prepend_maps.json --data-root data`
- فایل نمونه map:
  - `config/backfill_prepend_maps.example.json`

<!-- RUN_TABLE_START -->
## 🕒 آخرین اجراها

| گزارش | وضعیت | زمان اجرا (تهران) |
|---|---|---|
| 📄 [2026-02-22T02-49-42Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-22T02-49-42Z.md) | ✅ `success` | `2026-02-22` `06:19:42` |
| 📄 [2026-02-22T02-38-14Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-22T02-38-14Z.md) | ✅ `success` | `2026-02-22` `06:08:14` |
| 📄 [2026-02-21T18-47-11Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-21T18-47-11Z.md) | ✅ `success` | `2026-02-21` `22:17:11` |
| 📄 [2026-02-21T13-04-00Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-21T13-04-00Z.md) | ✅ `success` | `2026-02-21` `16:34:00` |
| 📄 [2026-02-21T11-34-51Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-21T11-34-51Z.md) | ✅ `success` | `2026-02-21` `15:04:51` |
| 📄 [2026-02-21T06-53-47Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-21T06-53-47Z.md) | ✅ `success` | `2026-02-21` `10:23:47` |
| 📄 [2026-02-21T04-04-22Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-21T04-04-22Z.md) | ✅ `success` | `2026-02-21` `07:34:22` |
| 📄 [2026-02-20T18-31-14Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-20T18-31-14Z.md) | ✅ `success` | `2026-02-20` `22:01:14` |
| 📄 [2026-02-20T17-08-16Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-20T17-08-16Z.md) | ✅ `success` | `2026-02-20` `20:38:16` |
| 📄 [2026-02-20.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-20.md) | ❌ `failed` | `2026-02-20` `20:06:34` |

<!-- RUN_TABLE_END -->
