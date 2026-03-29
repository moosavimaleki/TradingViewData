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
| 📄 [2026-03-29T13-11-53Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-29T13-11-53Z.md) | ✅ `success` | `2026-03-29` `16:41:53` |
| 📄 [2026-03-29T07-14-31Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-29T07-14-31Z.md) | ✅ `success` | `2026-03-29` `10:44:31` |
| 📄 [2026-03-29T03-22-08Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-29T03-22-08Z.md) | ✅ `success` | `2026-03-29` `06:52:08` |
| 📄 [2026-03-28T18-53-09Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-28T18-53-09Z.md) | ✅ `success` | `2026-03-28` `22:23:09` |
| 📄 [2026-03-28T13-10-56Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-28T13-10-56Z.md) | ✅ `success` | `2026-03-28` `16:40:56` |
| 📄 [2026-03-28T07-07-20Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-28T07-07-20Z.md) | ✅ `success` | `2026-03-28` `10:37:20` |
| 📄 [2026-03-28T02-48-42Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-28T02-48-42Z.md) | ✅ `success` | `2026-03-28` `06:18:42` |
| 📄 [2026-03-27T19-04-46Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-27T19-04-46Z.md) | ✅ `success` | `2026-03-27` `22:34:46` |
| 📄 [2026-03-27T13-22-39Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-27T13-22-39Z.md) | ✅ `success` | `2026-03-27` `16:52:39` |
| 📄 [2026-03-27T07-19-10Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-27T07-19-10Z.md) | ✅ `success` | `2026-03-27` `10:49:10` |

<!-- RUN_TABLE_END -->
