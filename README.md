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
| 📄 [2026-03-19T19-08-36Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-19T19-08-36Z.md) | ✅ `success` | `2026-03-19` `22:38:36` |
| 📄 [2026-03-19T13-22-50Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-19T13-22-50Z.md) | ✅ `success` | `2026-03-19` `16:52:50` |
| 📄 [2026-03-19T07-07-29Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-19T07-07-29Z.md) | ✅ `success` | `2026-03-19` `10:37:29` |
| 📄 [2026-03-19T02-52-20Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-19T02-52-20Z.md) | ✅ `success` | `2026-03-19` `06:22:20` |
| 📄 [2026-03-18T19-12-45Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-18T19-12-45Z.md) | ✅ `success` | `2026-03-18` `22:42:45` |
| 📄 [2026-03-18T13-42-25Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-18T13-42-25Z.md) | ✅ `success` | `2026-03-18` `17:12:25` |
| 📄 [2026-03-18T07-12-21Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-18T07-12-21Z.md) | ✅ `success` | `2026-03-18` `10:42:21` |
| 📄 [2026-03-18T02-50-53Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-18T02-50-53Z.md) | ✅ `success` | `2026-03-18` `06:20:53` |
| 📄 [2026-03-17T19-12-50Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-17T19-12-50Z.md) | ✅ `success` | `2026-03-17` `22:42:50` |
| 📄 [2026-03-17T13-41-04Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-17T13-41-04Z.md) | ✅ `success` | `2026-03-17` `17:11:04` |

<!-- RUN_TABLE_END -->
