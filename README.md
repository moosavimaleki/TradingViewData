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
| 📄 [2026-03-05T07-02-47Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-05T07-02-47Z.md) | ✅ `success` | `2026-03-05` `10:32:47` |
| 📄 [2026-03-05T02-42-49Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-05T02-42-49Z.md) | ✅ `success` | `2026-03-05` `06:12:49` |
| 📄 [2026-03-04T19-00-53Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-04T19-00-53Z.md) | ✅ `success` | `2026-03-04` `22:30:53` |
| 📄 [2026-03-04T13-13-27Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-04T13-13-27Z.md) | ✅ `success` | `2026-03-04` `16:43:27` |
| 📄 [2026-03-04T06-59-21Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-04T06-59-21Z.md) | ✅ `success` | `2026-03-04` `10:29:21` |
| 📄 [2026-03-04T02-39-57Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-04T02-39-57Z.md) | ✅ `success` | `2026-03-04` `06:09:57` |
| 📄 [2026-03-03T19-01-24Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-03T19-01-24Z.md) | ✅ `success` | `2026-03-03` `22:31:24` |
| 📄 [2026-03-03T13-14-26Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-03T13-14-26Z.md) | ✅ `success` | `2026-03-03` `16:44:26` |
| 📄 [2026-03-03T07-02-40Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-03T07-02-40Z.md) | ❌ `failed` | `2026-03-03` `10:32:40` |
| 📄 [2026-03-03T02-47-03Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-03T02-47-03Z.md) | ✅ `success` | `2026-03-03` `06:17:03` |

<!-- RUN_TABLE_END -->
