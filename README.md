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
| 📄 [2026-10-20T16-42-56Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-20T16-42-56Z.md) | ✅ `success` | `2026-10-20` `20:12:56` |
| 📄 [2026-10-20T11-18-16Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-20T11-18-16Z.md) | ✅ `success` | `2026-10-20` `14:48:16` |
| 📄 [2026-10-20T04-27-28Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-20T04-27-28Z.md) | ✅ `success` | `2026-10-20` `07:57:28` |
| 📄 [2026-10-19T22-13-14Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-19T22-13-14Z.md) | ✅ `success` | `2026-10-20` `01:43:14` |
| 📄 [2026-10-19T12-48-20Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-19T12-48-20Z.md) | ✅ `success` | `2026-10-19` `16:18:20` |
| 📄 [2026-10-19T04-16-08Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-19T04-16-08Z.md) | ✅ `success` | `2026-10-19` `07:46:08` |
| 📄 [2026-10-18T20-25-51Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-18T20-25-51Z.md) | ✅ `success` | `2026-10-18` `23:55:51` |
| 📄 [2026-10-18T15-42-57Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-18T15-42-57Z.md) | ✅ `success` | `2026-10-18` `19:12:57` |
| 📄 [2026-10-18T10-47-29Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-18T10-47-29Z.md) | ✅ `success` | `2026-10-18` `14:17:29` |
| 📄 [2026-10-18T04-06-49Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-18T04-06-49Z.md) | ✅ `success` | `2026-10-18` `07:36:49` |

<!-- RUN_TABLE_END -->
