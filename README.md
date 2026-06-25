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
| 📄 [2026-06-25T04-11-39Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-25T04-11-39Z.md) | ✅ `success` | `2026-06-25` `07:41:39` |
| 📄 [2026-06-24T19-56-12Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-24T19-56-12Z.md) | ✅ `success` | `2026-06-24` `23:26:12` |
| 📄 [2026-06-24T14-46-21Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-24T14-46-21Z.md) | ✅ `success` | `2026-06-24` `18:16:21` |
| 📄 [2026-06-24T09-43-38Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-24T09-43-38Z.md) | ✅ `success` | `2026-06-24` `13:13:38` |
| 📄 [2026-06-24T04-11-29Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-24T04-11-29Z.md) | ✅ `success` | `2026-06-24` `07:41:29` |
| 📄 [2026-06-23T20-14-38Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-23T20-14-38Z.md) | ✅ `success` | `2026-06-23` `23:44:38` |
| 📄 [2026-06-23T15-15-35Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-23T15-15-35Z.md) | ✅ `success` | `2026-06-23` `18:45:35` |
| 📄 [2026-06-23T09-56-16Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-23T09-56-16Z.md) | ✅ `success` | `2026-06-23` `13:26:16` |
| 📄 [2026-06-23T04-08-15Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-23T04-08-15Z.md) | ✅ `success` | `2026-06-23` `07:38:15` |
| 📄 [2026-06-22T20-57-35Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-22T20-57-35Z.md) | ✅ `success` | `2026-06-23` `00:27:35` |

<!-- RUN_TABLE_END -->
