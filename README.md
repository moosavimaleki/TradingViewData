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
| 📄 [2026-08-09T13-04-07Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-09T13-04-07Z.md) | ✅ `success` | `2026-08-09` `16:34:07` |
| 📄 [2026-08-09T07-05-40Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-09T07-05-40Z.md) | ✅ `success` | `2026-08-09` `10:35:40` |
| 📄 [2026-08-09T02-11-32Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-09T02-11-32Z.md) | ✅ `success` | `2026-08-09` `05:41:32` |
| 📄 [2026-08-08T18-47-36Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-08T18-47-36Z.md) | ✅ `success` | `2026-08-08` `22:17:35` |
| 📄 [2026-08-08T13-01-34Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-08T13-01-34Z.md) | ✅ `success` | `2026-08-08` `16:31:34` |
| 📄 [2026-08-08T07-02-58Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-08T07-02-58Z.md) | ✅ `success` | `2026-08-08` `10:32:58` |
| 📄 [2026-08-08T02-03-45Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-08T02-03-45Z.md) | ❌ `failed` | `2026-08-08` `05:33:45` |
| 📄 [2026-08-07T19-05-27Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-07T19-05-27Z.md) | ❌ `failed` | `2026-08-07` `22:35:27` |
| 📄 [2026-08-07T13-17-40Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-07T13-17-40Z.md) | ❌ `failed` | `2026-08-07` `16:47:40` |
| 📄 [2026-08-07T07-26-13Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-07T07-26-13Z.md) | ❌ `failed` | `2026-08-07` `10:56:13` |

<!-- RUN_TABLE_END -->
