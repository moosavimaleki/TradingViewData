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
| 📄 [2026-03-23T02-53-03Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-23T02-53-03Z.md) | ✅ `success` | `2026-03-23` `06:23:03` |
| 📄 [2026-03-22T18-48-58Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-22T18-48-58Z.md) | ✅ `success` | `2026-03-22` `22:18:58` |
| 📄 [2026-03-22T13-07-19Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-22T13-07-19Z.md) | ✅ `success` | `2026-03-22` `16:37:19` |
| 📄 [2026-03-22T07-00-27Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-22T07-00-27Z.md) | ✅ `success` | `2026-03-22` `10:30:27` |
| 📄 [2026-03-22T02-53-03Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-22T02-53-03Z.md) | ✅ `success` | `2026-03-22` `06:23:03` |
| 📄 [2026-03-21T18-47-34Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-21T18-47-34Z.md) | ✅ `success` | `2026-03-21` `22:17:34` |
| 📄 [2026-03-21T13-05-10Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-21T13-05-10Z.md) | ✅ `success` | `2026-03-21` `16:35:10` |
| 📄 [2026-03-21T06-55-52Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-21T06-55-52Z.md) | ✅ `success` | `2026-03-21` `10:25:52` |
| 📄 [2026-03-21T02-36-31Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-21T02-36-31Z.md) | ✅ `success` | `2026-03-21` `06:06:31` |
| 📄 [2026-03-20T19-00-13Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-20T19-00-13Z.md) | ✅ `success` | `2026-03-20` `22:30:13` |

<!-- RUN_TABLE_END -->
