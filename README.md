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
| 📄 [2026-05-15T19-48-01Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-15T19-48-01Z.md) | ✅ `success` | `2026-05-15` `23:18:01` |
| 📄 [2026-05-15T14-24-06Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-15T14-24-06Z.md) | ✅ `success` | `2026-05-15` `17:54:06` |
| 📄 [2026-05-15T09-18-40Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-15T09-18-40Z.md) | ✅ `success` | `2026-05-15` `12:48:40` |
| 📄 [2026-05-15T04-04-53Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-15T04-04-53Z.md) | ✅ `success` | `2026-05-15` `07:34:53` |
| 📄 [2026-05-14T19-55-00Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-14T19-55-00Z.md) | ✅ `success` | `2026-05-14` `23:25:00` |
| 📄 [2026-05-14T14-30-14Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-14T14-30-14Z.md) | ✅ `success` | `2026-05-14` `18:00:14` |
| 📄 [2026-05-14T08-45-57Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-14T08-45-57Z.md) | ✅ `success` | `2026-05-14` `12:15:57` |
| 📄 [2026-05-14T04-00-01Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-14T04-00-01Z.md) | ✅ `success` | `2026-05-14` `07:30:01` |
| 📄 [2026-05-13T20-03-39Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-13T20-03-39Z.md) | ✅ `success` | `2026-05-13` `23:33:39` |
| 📄 [2026-05-13T14-50-31Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-13T14-50-31Z.md) | ✅ `success` | `2026-05-13` `18:20:31` |

<!-- RUN_TABLE_END -->
