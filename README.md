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

<!-- RUN_TABLE_START -->
## 🕒 آخرین اجراها

| گزارش | وضعیت | زمان اجرا (تهران) |
|---|---|---|
| 📄 [2026-03-25T07-12-21Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-25T07-12-21Z.md) | ✅ `success` | `2026-03-25` `10:42:21` |
| 📄 [2026-03-25T02-49-50Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-25T02-49-50Z.md) | ✅ `success` | `2026-03-25` `06:19:50` |
| 📄 [2026-03-24T19-14-42Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-24T19-14-42Z.md) | ❌ `failed` | `2026-03-24` `22:44:42` |
| 📄 [2026-03-24T13-40-38Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-24T13-40-38Z.md) | ✅ `success` | `2026-03-24` `17:10:38` |
| 📄 [2026-03-24T07-13-46Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-24T07-13-46Z.md) | ✅ `success` | `2026-03-24` `10:43:46` |
| 📄 [2026-03-24T02-44-58Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-24T02-44-58Z.md) | ✅ `success` | `2026-03-24` `06:14:58` |
| 📄 [2026-03-23T19-04-34Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-23T19-04-34Z.md) | ✅ `success` | `2026-03-23` `22:34:34` |
| 📄 [2026-03-23T13-24-43Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-23T13-24-43Z.md) | ✅ `success` | `2026-03-23` `16:54:43` |
| 📄 [2026-03-23T07-22-11Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-23T07-22-11Z.md) | ✅ `success` | `2026-03-23` `10:52:11` |
| 📄 [2026-03-23T02-53-03Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-23T02-53-03Z.md) | ✅ `success` | `2026-03-23` `06:23:03` |

<!-- RUN_TABLE_END -->
