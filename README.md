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
| 📄 [2026-06-14T14-19-18Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-14T14-19-18Z.md) | ✅ `success` | `2026-06-14` `17:49:18` |
| 📄 [2026-06-14T09-48-11Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-14T09-48-11Z.md) | ✅ `success` | `2026-06-14` `13:18:11` |
| 📄 [2026-06-14T04-52-54Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-14T04-52-54Z.md) | ✅ `success` | `2026-06-14` `08:22:54` |
| 📄 [2026-06-13T19-45-37Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-13T19-45-37Z.md) | ✅ `success` | `2026-06-13` `23:15:37` |
| 📄 [2026-06-13T14-15-39Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-13T14-15-39Z.md) | ✅ `success` | `2026-06-13` `17:45:39` |
| 📄 [2026-06-13T09-26-33Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-13T09-26-33Z.md) | ✅ `success` | `2026-06-13` `12:56:33` |
| 📄 [2026-06-13T04-25-38Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-13T04-25-38Z.md) | ✅ `success` | `2026-06-13` `07:55:38` |
| 📄 [2026-06-12T20-19-36Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-12T20-19-36Z.md) | ✅ `success` | `2026-06-12` `23:49:36` |
| 📄 [2026-06-12T15-30-59Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-12T15-30-59Z.md) | ✅ `success` | `2026-06-12` `19:00:59` |
| 📄 [2026-06-12T10-24-25Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-12T10-24-25Z.md) | ✅ `success` | `2026-06-12` `13:54:25` |

<!-- RUN_TABLE_END -->
