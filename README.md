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
| 📄 [2026-06-09T15-19-48Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-09T15-19-48Z.md) | ❌ `failed` | `2026-06-09` `18:49:48` |
| 📄 [2026-06-09T09-57-13Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-09T09-57-13Z.md) | ✅ `success` | `2026-06-09` `13:27:13` |
| 📄 [2026-06-09T04-10-53Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-09T04-10-53Z.md) | ✅ `success` | `2026-06-09` `07:40:53` |
| 📄 [2026-06-08T20-26-39Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-08T20-26-39Z.md) | ✅ `success` | `2026-06-08` `23:56:39` |
| 📄 [2026-06-08T16-07-48Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-08T16-07-48Z.md) | ✅ `success` | `2026-06-08` `19:37:48` |
| 📄 [2026-06-08T11-10-21Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-08T11-10-21Z.md) | ✅ `success` | `2026-06-08` `14:40:21` |
| 📄 [2026-06-08T04-48-30Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-08T04-48-30Z.md) | ✅ `success` | `2026-06-08` `08:18:30` |
| 📄 [2026-06-07T19-41-25Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-07T19-41-25Z.md) | ✅ `success` | `2026-06-07` `23:11:25` |
| 📄 [2026-06-07T14-09-23Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-07T14-09-23Z.md) | ✅ `success` | `2026-06-07` `17:39:23` |
| 📄 [2026-06-07T09-26-44Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-07T09-26-44Z.md) | ✅ `success` | `2026-06-07` `12:56:44` |

<!-- RUN_TABLE_END -->
