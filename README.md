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
| 📄 [2026-02-26T13-23-55Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-26T13-23-55Z.md) | ✅ `success` | `2026-02-26` `16:53:55` |
| 📄 [2026-02-26T07-09-50Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-26T07-09-50Z.md) | ✅ `success` | `2026-02-26` `10:39:50` |
| 📄 [2026-02-26T02-43-00Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-26T02-43-00Z.md) | ✅ `success` | `2026-02-26` `06:13:00` |
| 📄 [2026-02-25T19-37-13Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-25T19-37-13Z.md) | ✅ `success` | `2026-02-25` `23:07:13` |
| 📄 [2026-02-25T19-15-16Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-25T19-15-16Z.md) | ✅ `success` | `2026-02-25` `22:45:16` |
| 📄 [2026-02-25T13-22-55Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-25T13-22-55Z.md) | ✅ `success` | `2026-02-25` `16:52:55` |
| 📄 [2026-02-25T07-11-22Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-25T07-11-22Z.md) | ✅ `success` | `2026-02-25` `10:41:22` |
| 📄 [2026-02-25T02-48-03Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-25T02-48-03Z.md) | ✅ `success` | `2026-02-25` `06:18:03` |
| 📄 [2026-02-24T19-12-11Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-24T19-12-11Z.md) | ✅ `success` | `2026-02-24` `22:42:11` |
| 📄 [2026-02-24T13-23-40Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-24T13-23-40Z.md) | ✅ `success` | `2026-02-24` `16:53:40` |

<!-- RUN_TABLE_END -->
