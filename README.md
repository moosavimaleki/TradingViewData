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
| 📄 [2026-10-09T05-44-19Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-09T05-44-19Z.md) | ✅ `success` | `2026-10-09` `09:14:19` |
| 📄 [2026-10-08T23-11-25Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-08T23-11-25Z.md) | ✅ `success` | `2026-10-09` `02:41:25` |
| 📄 [2026-10-08T13-12-57Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-08T13-12-57Z.md) | ✅ `success` | `2026-10-08` `16:42:57` |
| 📄 [2026-10-08T05-39-57Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-08T05-39-57Z.md) | ✅ `success` | `2026-10-08` `09:09:57` |
| 📄 [2026-10-07T22-57-49Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-07T22-57-49Z.md) | ✅ `success` | `2026-10-08` `02:27:49` |
| 📄 [2026-10-07T13-05-38Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-07T13-05-38Z.md) | ✅ `success` | `2026-10-07` `16:35:38` |
| 📄 [2026-10-07T05-31-38Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-07T05-31-38Z.md) | ✅ `success` | `2026-10-07` `09:01:38` |
| 📄 [2026-10-06T18-13-13Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-06T18-13-13Z.md) | ✅ `success` | `2026-10-06` `21:43:13` |
| 📄 [2026-10-06T06-07-40Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-06T06-07-40Z.md) | ✅ `success` | `2026-10-06` `09:37:40` |
| 📄 [2026-10-05T23-56-42Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-05T23-56-42Z.md) | ✅ `success` | `2026-10-06` `03:26:42` |

<!-- RUN_TABLE_END -->
