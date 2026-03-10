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
| 📄 [2026-03-10T13-18-23Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-10T13-18-23Z.md) | ✅ `success` | `2026-03-10` `16:48:23` |
| 📄 [2026-03-10T07-01-21Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-10T07-01-21Z.md) | ✅ `success` | `2026-03-10` `10:31:21` |
| 📄 [2026-03-10T02-39-26Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-10T02-39-26Z.md) | ✅ `success` | `2026-03-10` `06:09:26` |
| 📄 [2026-03-09T19-02-35Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-09T19-02-35Z.md) | ✅ `success` | `2026-03-09` `22:32:35` |
| 📄 [2026-03-09T13-21-06Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-09T13-21-06Z.md) | ✅ `success` | `2026-03-09` `16:51:06` |
| 📄 [2026-03-09T07-11-50Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-09T07-11-50Z.md) | ✅ `success` | `2026-03-09` `10:41:50` |
| 📄 [2026-03-09T02-48-01Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-09T02-48-01Z.md) | ✅ `success` | `2026-03-09` `06:18:01` |
| 📄 [2026-03-08T18-45-39Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-08T18-45-39Z.md) | ✅ `success` | `2026-03-08` `22:15:39` |
| 📄 [2026-03-08T13-04-04Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-08T13-04-04Z.md) | ✅ `success` | `2026-03-08` `16:34:04` |
| 📄 [2026-03-08T06-54-48Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-08T06-54-48Z.md) | ✅ `success` | `2026-03-08` `10:24:48` |

<!-- RUN_TABLE_END -->
