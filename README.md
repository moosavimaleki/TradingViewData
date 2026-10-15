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
| 📄 [2026-10-15T21-11-57Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-15T21-11-57Z.md) | ✅ `success` | `2026-10-16` `00:41:57` |
| 📄 [2026-10-15T16-45-04Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-15T16-45-04Z.md) | ✅ `success` | `2026-10-15` `20:15:04` |
| 📄 [2026-10-15T11-14-23Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-15T11-14-23Z.md) | ✅ `success` | `2026-10-15` `14:44:23` |
| 📄 [2026-10-15T04-13-46Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-15T04-13-46Z.md) | ✅ `success` | `2026-10-15` `07:43:46` |
| 📄 [2026-10-14T21-30-03Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-14T21-30-03Z.md) | ✅ `success` | `2026-10-15` `01:00:03` |
| 📄 [2026-10-14T16-58-01Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-14T16-58-01Z.md) | ✅ `success` | `2026-10-14` `20:28:01` |
| 📄 [2026-10-14T11-35-32Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-14T11-35-32Z.md) | ✅ `success` | `2026-10-14` `15:05:32` |
| 📄 [2026-10-14T04-31-04Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-14T04-31-04Z.md) | ✅ `success` | `2026-10-14` `08:01:04` |
| 📄 [2026-10-13T22-31-53Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-13T22-31-53Z.md) | ✅ `success` | `2026-10-14` `02:01:53` |
| 📄 [2026-10-13T13-58-57Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-13T13-58-57Z.md) | ✅ `success` | `2026-10-13` `17:28:57` |

<!-- RUN_TABLE_END -->
