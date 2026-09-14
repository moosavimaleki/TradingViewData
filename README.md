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
| 📄 [2026-09-14T12-27-33Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-14T12-27-33Z.md) | ✅ `success` | `2026-09-14` `15:57:33` |
| 📄 [2026-09-14T04-31-41Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-14T04-31-41Z.md) | ✅ `success` | `2026-09-14` `08:01:41` |
| 📄 [2026-09-13T20-37-03Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-13T20-37-03Z.md) | ✅ `success` | `2026-09-14` `00:07:03` |
| 📄 [2026-09-13T16-01-45Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-13T16-01-45Z.md) | ✅ `success` | `2026-09-13` `19:31:45` |
| 📄 [2026-09-13T11-33-30Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-13T11-33-30Z.md) | ✅ `success` | `2026-09-13` `15:03:30` |
| 📄 [2026-09-13T04-25-01Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-13T04-25-01Z.md) | ✅ `success` | `2026-09-13` `07:55:01` |
| 📄 [2026-09-12T20-25-35Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-12T20-25-35Z.md) | ✅ `success` | `2026-09-12` `23:55:35` |
| 📄 [2026-09-12T15-23-28Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-12T15-23-28Z.md) | ✅ `success` | `2026-09-12` `18:53:28` |
| 📄 [2026-09-12T10-30-30Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-12T10-30-30Z.md) | ✅ `success` | `2026-09-12` `14:00:30` |
| 📄 [2026-09-12T04-12-36Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-12T04-12-36Z.md) | ✅ `success` | `2026-09-12` `07:42:36` |

<!-- RUN_TABLE_END -->
