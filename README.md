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
| 📄 [2026-07-14T19-36-01Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-14T19-36-01Z.md) | ✅ `success` | `2026-07-14` `23:06:01` |
| 📄 [2026-07-14T14-00-22Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-14T14-00-22Z.md) | ✅ `success` | `2026-07-14` `17:30:22` |
| 📄 [2026-07-14T08-19-36Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-14T08-19-36Z.md) | ✅ `success` | `2026-07-14` `11:49:36` |
| 📄 [2026-07-14T03-13-44Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-14T03-13-44Z.md) | ❌ `failed` | `2026-07-14` `06:43:44` |
| 📄 [2026-07-13T19-38-19Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-13T19-38-19Z.md) | ✅ `success` | `2026-07-13` `23:08:19` |
| 📄 [2026-07-13T14-50-16Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-13T14-50-16Z.md) | ✅ `success` | `2026-07-13` `18:20:16` |
| 📄 [2026-07-13T09-39-37Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-13T09-39-37Z.md) | ✅ `success` | `2026-07-13` `13:09:37` |
| 📄 [2026-07-13T03-38-31Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-13T03-38-31Z.md) | ✅ `success` | `2026-07-13` `07:08:31` |
| 📄 [2026-07-12T19-14-38Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-12T19-14-38Z.md) | ✅ `success` | `2026-07-12` `22:44:38` |
| 📄 [2026-07-12T13-42-18Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-12T13-42-18Z.md) | ✅ `success` | `2026-07-12` `17:12:18` |

<!-- RUN_TABLE_END -->
