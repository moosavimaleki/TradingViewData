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
| 📄 [2026-03-06T13-12-47Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-06T13-12-47Z.md) | ✅ `success` | `2026-03-06` `16:42:47` |
| 📄 [2026-03-06T07-00-49Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-06T07-00-49Z.md) | ✅ `success` | `2026-03-06` `10:30:49` |
| 📄 [2026-03-06T02-40-24Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-06T02-40-24Z.md) | ✅ `success` | `2026-03-06` `06:10:24` |
| 📄 [2026-03-05T19-22-01Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-05T19-22-01Z.md) | ✅ `success` | `2026-03-05` `22:52:01` |
| 📄 [2026-03-05T13-17-08Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-05T13-17-08Z.md) | ✅ `success` | `2026-03-05` `16:47:08` |
| 📄 [2026-03-05T07-02-47Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-05T07-02-47Z.md) | ✅ `success` | `2026-03-05` `10:32:47` |
| 📄 [2026-03-05T02-42-49Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-05T02-42-49Z.md) | ✅ `success` | `2026-03-05` `06:12:49` |
| 📄 [2026-03-04T19-00-53Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-04T19-00-53Z.md) | ✅ `success` | `2026-03-04` `22:30:53` |
| 📄 [2026-03-04T13-13-27Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-04T13-13-27Z.md) | ✅ `success` | `2026-03-04` `16:43:27` |
| 📄 [2026-03-04T06-59-21Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-04T06-59-21Z.md) | ✅ `success` | `2026-03-04` `10:29:21` |

<!-- RUN_TABLE_END -->
