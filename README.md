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
| 📄 [2026-03-08T18-45-39Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-08T18-45-39Z.md) | ✅ `success` | `2026-03-08` `22:15:39` |
| 📄 [2026-03-08T13-04-04Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-08T13-04-04Z.md) | ✅ `success` | `2026-03-08` `16:34:04` |
| 📄 [2026-03-08T06-54-48Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-08T06-54-48Z.md) | ✅ `success` | `2026-03-08` `10:24:48` |
| 📄 [2026-03-08T02-46-38Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-08T02-46-38Z.md) | ✅ `success` | `2026-03-08` `06:16:38` |
| 📄 [2026-03-07T18-44-03Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-07T18-44-03Z.md) | ✅ `success` | `2026-03-07` `22:14:03` |
| 📄 [2026-03-07T13-02-18Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-07T13-02-18Z.md) | ✅ `success` | `2026-03-07` `16:32:18` |
| 📄 [2026-03-07T06-52-59Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-07T06-52-59Z.md) | ✅ `success` | `2026-03-07` `10:22:59` |
| 📄 [2026-03-07T02-33-01Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-07T02-33-01Z.md) | ✅ `success` | `2026-03-07` `06:03:01` |
| 📄 [2026-03-06T18-57-01Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-06T18-57-01Z.md) | ✅ `success` | `2026-03-06` `22:27:01` |
| 📄 [2026-03-06T13-12-47Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-06T13-12-47Z.md) | ✅ `success` | `2026-03-06` `16:42:47` |

<!-- RUN_TABLE_END -->
