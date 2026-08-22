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
| 📄 [2026-08-22T12-50-56Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-22T12-50-56Z.md) | ✅ `success` | `2026-08-22` `16:20:56` |
| 📄 [2026-08-22T06-50-28Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-22T06-50-28Z.md) | ✅ `success` | `2026-08-22` `10:20:28` |
| 📄 [2026-08-22T01-37-59Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-22T01-37-59Z.md) | ✅ `success` | `2026-08-22` `05:07:59` |
| 📄 [2026-08-21T18-45-56Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-21T18-45-56Z.md) | ✅ `success` | `2026-08-21` `22:15:56` |
| 📄 [2026-08-21T12-59-49Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-21T12-59-49Z.md) | ✅ `success` | `2026-08-21` `16:29:49` |
| 📄 [2026-08-21T06-56-48Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-21T06-56-48Z.md) | ✅ `success` | `2026-08-21` `10:26:48` |
| 📄 [2026-08-21T01-44-42Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-21T01-44-42Z.md) | ✅ `success` | `2026-08-21` `05:14:42` |
| 📄 [2026-08-20T18-49-14Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-20T18-49-14Z.md) | ✅ `success` | `2026-08-20` `22:19:14` |
| 📄 [2026-08-20T13-00-53Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-20T13-00-53Z.md) | ✅ `success` | `2026-08-20` `16:30:53` |
| 📄 [2026-08-20T06-55-23Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-20T06-55-23Z.md) | ✅ `success` | `2026-08-20` `10:25:23` |

<!-- RUN_TABLE_END -->
