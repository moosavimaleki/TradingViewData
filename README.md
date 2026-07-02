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
| 📄 [2026-07-02T09-25-13Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-02T09-25-13Z.md) | ✅ `success` | `2026-07-02` `12:55:13` |
| 📄 [2026-07-02T04-08-23Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-02T04-08-23Z.md) | ✅ `success` | `2026-07-02` `07:38:23` |
| 📄 [2026-07-01T20-03-58Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-01T20-03-58Z.md) | ✅ `success` | `2026-07-01` `23:33:58` |
| 📄 [2026-07-01T14-50-35Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-01T14-50-35Z.md) | ✅ `success` | `2026-07-01` `18:20:35` |
| 📄 [2026-07-01T10-02-28Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-01T10-02-28Z.md) | ✅ `success` | `2026-07-01` `13:32:28` |
| 📄 [2026-07-01T04-41-23Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-01T04-41-23Z.md) | ❌ `failed` | `2026-07-01` `08:11:23` |
| 📄 [2026-06-30T20-06-55Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-30T20-06-55Z.md) | ✅ `success` | `2026-06-30` `23:36:55` |
| 📄 [2026-06-30T14-33-19Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-30T14-33-19Z.md) | ✅ `success` | `2026-06-30` `18:03:19` |
| 📄 [2026-06-30T09-53-34Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-30T09-53-34Z.md) | ✅ `success` | `2026-06-30` `13:23:34` |
| 📄 [2026-06-30T04-12-40Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-30T04-12-40Z.md) | ✅ `success` | `2026-06-30` `07:42:40` |

<!-- RUN_TABLE_END -->
