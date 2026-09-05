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
| 📄 [2026-09-05T04-02-34Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-05T04-02-34Z.md) | ✅ `success` | `2026-09-05` `07:32:34` |
| 📄 [2026-09-04T20-38-43Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-04T20-38-43Z.md) | ✅ `success` | `2026-09-05` `00:08:43` |
| 📄 [2026-09-04T16-10-09Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-04T16-10-09Z.md) | ✅ `success` | `2026-09-04` `19:40:09` |
| 📄 [2026-09-04T11-02-05Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-04T11-02-05Z.md) | ✅ `success` | `2026-09-04` `14:32:05` |
| 📄 [2026-09-04T04-06-17Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-04T04-06-17Z.md) | ✅ `success` | `2026-09-04` `07:36:17` |
| 📄 [2026-09-03T20-51-57Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-03T20-51-57Z.md) | ✅ `success` | `2026-09-04` `00:21:57` |
| 📄 [2026-09-03T16-14-56Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-03T16-14-56Z.md) | ✅ `success` | `2026-09-03` `19:44:56` |
| 📄 [2026-09-03T11-01-06Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-03T11-01-06Z.md) | ✅ `success` | `2026-09-03` `14:31:06` |
| 📄 [2026-09-03T04-02-30Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-03T04-02-30Z.md) | ✅ `success` | `2026-09-03` `07:32:30` |
| 📄 [2026-09-02T20-53-46Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-02T20-53-46Z.md) | ✅ `success` | `2026-09-03` `00:23:46` |

<!-- RUN_TABLE_END -->
