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
| 📄 [2026-05-21T04-22-04Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-21T04-22-04Z.md) | ✅ `success` | `2026-05-21` `07:52:04` |
| 📄 [2026-05-20T20-26-04Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-20T20-26-04Z.md) | ✅ `success` | `2026-05-20` `23:56:04` |
| 📄 [2026-05-20T15-41-23Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-20T15-41-23Z.md) | ✅ `success` | `2026-05-20` `19:11:23` |
| 📄 [2026-05-20T09-48-41Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-20T09-48-41Z.md) | ✅ `success` | `2026-05-20` `13:18:41` |
| 📄 [2026-05-20T04-13-36Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-20T04-13-36Z.md) | ✅ `success` | `2026-05-20` `07:43:36` |
| 📄 [2026-05-19T19-59-26Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-19T19-59-26Z.md) | ✅ `success` | `2026-05-19` `23:29:26` |
| 📄 [2026-05-19T15-40-05Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-19T15-40-05Z.md) | ✅ `success` | `2026-05-19` `19:10:05` |
| 📄 [2026-05-19T09-58-37Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-19T09-58-37Z.md) | ✅ `success` | `2026-05-19` `13:28:37` |
| 📄 [2026-05-19T04-12-48Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-19T04-12-48Z.md) | ✅ `success` | `2026-05-19` `07:42:48` |
| 📄 [2026-05-18T19-53-55Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-18T19-53-55Z.md) | ✅ `success` | `2026-05-18` `23:23:55` |

<!-- RUN_TABLE_END -->
