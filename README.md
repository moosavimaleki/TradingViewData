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
| 📄 [2026-08-24T07-10-25Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-24T07-10-25Z.md) | ❌ `failed` | `2026-08-24` `10:40:25` |
| 📄 [2026-08-24T01-45-33Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-24T01-45-33Z.md) | ❌ `failed` | `2026-08-24` `05:15:33` |
| 📄 [2026-08-23T18-38-04Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-23T18-38-04Z.md) | ✅ `success` | `2026-08-23` `22:08:04` |
| 📄 [2026-08-23T12-52-05Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-23T12-52-05Z.md) | ✅ `success` | `2026-08-23` `16:22:05` |
| 📄 [2026-08-23T06-51-30Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-23T06-51-30Z.md) | ✅ `success` | `2026-08-23` `10:21:30` |
| 📄 [2026-08-23T01-47-50Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-23T01-47-50Z.md) | ✅ `success` | `2026-08-23` `05:17:50` |
| 📄 [2026-08-22T18-38-35Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-22T18-38-35Z.md) | ✅ `success` | `2026-08-22` `22:08:35` |
| 📄 [2026-08-22T12-50-56Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-22T12-50-56Z.md) | ✅ `success` | `2026-08-22` `16:20:56` |
| 📄 [2026-08-22T06-50-28Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-22T06-50-28Z.md) | ✅ `success` | `2026-08-22` `10:20:28` |
| 📄 [2026-08-22T01-37-59Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-22T01-37-59Z.md) | ✅ `success` | `2026-08-22` `05:07:59` |

<!-- RUN_TABLE_END -->
