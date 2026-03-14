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
| 📄 [2026-03-14T02-40-46Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-14T02-40-46Z.md) | ✅ `success` | `2026-03-14` `06:10:46` |
| 📄 [2026-03-13T18-54-00Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-13T18-54-00Z.md) | ✅ `success` | `2026-03-13` `22:24:00` |
| 📄 [2026-03-13T13-15-59Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-13T13-15-59Z.md) | ✅ `success` | `2026-03-13` `16:45:59` |
| 📄 [2026-03-13T07-04-31Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-13T07-04-31Z.md) | ✅ `success` | `2026-03-13` `10:34:31` |
| 📄 [2026-03-13T02-42-08Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-13T02-42-08Z.md) | ✅ `success` | `2026-03-13` `06:12:08` |
| 📄 [2026-03-12T19-03-27Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-12T19-03-27Z.md) | ✅ `success` | `2026-03-12` `22:33:27` |
| 📄 [2026-03-12T13-18-15Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-12T13-18-15Z.md) | ✅ `success` | `2026-03-12` `16:48:15` |
| 📄 [2026-03-12T07-05-47Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-12T07-05-47Z.md) | ✅ `success` | `2026-03-12` `10:35:47` |
| 📄 [2026-03-12T02-44-16Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-12T02-44-16Z.md) | ✅ `success` | `2026-03-12` `06:14:16` |
| 📄 [2026-03-11T19-02-49Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-11T19-02-49Z.md) | ✅ `success` | `2026-03-11` `22:32:49` |

<!-- RUN_TABLE_END -->
