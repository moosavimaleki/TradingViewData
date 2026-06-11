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
| 📄 [2026-06-11T04-44-16Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-11T04-44-16Z.md) | ✅ `success` | `2026-06-11` `08:14:16` |
| 📄 [2026-06-10T20-39-56Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-10T20-39-56Z.md) | ✅ `success` | `2026-06-11` `00:09:56` |
| 📄 [2026-06-10T15-54-31Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-10T15-54-31Z.md) | ✅ `success` | `2026-06-10` `19:24:31` |
| 📄 [2026-06-10T10-14-35Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-10T10-14-35Z.md) | ✅ `success` | `2026-06-10` `13:44:35` |
| 📄 [2026-06-10T04-22-18Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-10T04-22-18Z.md) | ✅ `success` | `2026-06-10` `07:52:18` |
| 📄 [2026-06-09T20-14-21Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-09T20-14-21Z.md) | ✅ `success` | `2026-06-09` `23:44:21` |
| 📄 [2026-06-09T15-19-48Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-09T15-19-48Z.md) | ❌ `failed` | `2026-06-09` `18:49:48` |
| 📄 [2026-06-09T09-57-13Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-09T09-57-13Z.md) | ✅ `success` | `2026-06-09` `13:27:13` |
| 📄 [2026-06-09T04-10-53Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-09T04-10-53Z.md) | ✅ `success` | `2026-06-09` `07:40:53` |
| 📄 [2026-06-08T20-26-39Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-08T20-26-39Z.md) | ✅ `success` | `2026-06-08` `23:56:39` |

<!-- RUN_TABLE_END -->
