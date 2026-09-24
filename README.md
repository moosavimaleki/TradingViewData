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
| 📄 [2026-09-24T16-57-23Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-24T16-57-23Z.md) | ✅ `success` | `2026-09-24` `20:27:23` |
| 📄 [2026-09-24T11-30-57Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-24T11-30-57Z.md) | ✅ `success` | `2026-09-24` `15:00:57` |
| 📄 [2026-09-24T04-21-16Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-24T04-21-16Z.md) | ✅ `success` | `2026-09-24` `07:51:16` |
| 📄 [2026-09-23T21-22-43Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-23T21-22-43Z.md) | ✅ `success` | `2026-09-24` `00:52:43` |
| 📄 [2026-09-23T16-40-04Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-23T16-40-04Z.md) | ✅ `success` | `2026-09-23` `20:10:04` |
| 📄 [2026-09-23T11-17-08Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-23T11-17-08Z.md) | ✅ `success` | `2026-09-23` `14:47:08` |
| 📄 [2026-09-23T04-24-24Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-23T04-24-24Z.md) | ✅ `success` | `2026-09-23` `07:54:24` |
| 📄 [2026-09-22T21-08-51Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-22T21-08-51Z.md) | ✅ `success` | `2026-09-23` `00:38:51` |
| 📄 [2026-09-22T16-43-48Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-22T16-43-48Z.md) | ✅ `success` | `2026-09-22` `20:13:48` |
| 📄 [2026-09-22T11-21-34Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-22T11-21-34Z.md) | ✅ `success` | `2026-09-22` `14:51:34` |

<!-- RUN_TABLE_END -->
