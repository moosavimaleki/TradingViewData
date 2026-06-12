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
| 📄 [2026-06-12T15-30-59Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-12T15-30-59Z.md) | ✅ `success` | `2026-06-12` `19:00:59` |
| 📄 [2026-06-12T10-24-25Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-12T10-24-25Z.md) | ✅ `success` | `2026-06-12` `13:54:25` |
| 📄 [2026-06-12T04-47-03Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-12T04-47-03Z.md) | ✅ `success` | `2026-06-12` `08:17:03` |
| 📄 [2026-06-11T20-30-09Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-11T20-30-09Z.md) | ✅ `success` | `2026-06-12` `00:00:09` |
| 📄 [2026-06-11T16-14-27Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-11T16-14-27Z.md) | ✅ `success` | `2026-06-11` `19:44:27` |
| 📄 [2026-06-11T10-49-45Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-11T10-49-45Z.md) | ✅ `success` | `2026-06-11` `14:19:45` |
| 📄 [2026-06-11T04-44-16Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-11T04-44-16Z.md) | ✅ `success` | `2026-06-11` `08:14:16` |
| 📄 [2026-06-10T20-39-56Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-10T20-39-56Z.md) | ✅ `success` | `2026-06-11` `00:09:56` |
| 📄 [2026-06-10T15-54-31Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-10T15-54-31Z.md) | ✅ `success` | `2026-06-10` `19:24:31` |
| 📄 [2026-06-10T10-14-35Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-10T10-14-35Z.md) | ✅ `success` | `2026-06-10` `13:44:35` |

<!-- RUN_TABLE_END -->
