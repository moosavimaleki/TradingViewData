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
| 📄 [2026-08-10T13-23-03Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-10T13-23-03Z.md) | ✅ `success` | `2026-08-10` `16:53:03` |
| 📄 [2026-08-10T07-52-58Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-10T07-52-58Z.md) | ✅ `success` | `2026-08-10` `11:22:58` |
| 📄 [2026-08-10T02-20-15Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-10T02-20-15Z.md) | ✅ `success` | `2026-08-10` `05:50:15` |
| 📄 [2026-08-09T18-50-44Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-09T18-50-44Z.md) | ✅ `success` | `2026-08-09` `22:20:44` |
| 📄 [2026-08-09T13-04-07Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-09T13-04-07Z.md) | ✅ `success` | `2026-08-09` `16:34:07` |
| 📄 [2026-08-09T07-05-40Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-09T07-05-40Z.md) | ✅ `success` | `2026-08-09` `10:35:40` |
| 📄 [2026-08-09T02-11-32Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-09T02-11-32Z.md) | ✅ `success` | `2026-08-09` `05:41:32` |
| 📄 [2026-08-08T18-47-36Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-08T18-47-36Z.md) | ✅ `success` | `2026-08-08` `22:17:35` |
| 📄 [2026-08-08T13-01-34Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-08T13-01-34Z.md) | ✅ `success` | `2026-08-08` `16:31:34` |
| 📄 [2026-08-08T07-02-58Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-08T07-02-58Z.md) | ✅ `success` | `2026-08-08` `10:32:58` |

<!-- RUN_TABLE_END -->
