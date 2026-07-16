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
| 📄 [2026-07-16T14-08-59Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-16T14-08-59Z.md) | ❌ `failed` | `2026-07-16` `17:38:59` |
| 📄 [2026-07-16T08-24-12Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-16T08-24-12Z.md) | ✅ `success` | `2026-07-16` `11:54:12` |
| 📄 [2026-07-16T03-19-47Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-16T03-19-47Z.md) | ✅ `success` | `2026-07-16` `06:49:47` |
| 📄 [2026-07-15T19-21-32Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-15T19-21-32Z.md) | ✅ `success` | `2026-07-15` `22:51:32` |
| 📄 [2026-07-15T13-56-59Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-15T13-56-59Z.md) | ✅ `success` | `2026-07-15` `17:26:59` |
| 📄 [2026-07-15T08-25-33Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-15T08-25-33Z.md) | ✅ `success` | `2026-07-15` `11:55:33` |
| 📄 [2026-07-15T03-13-03Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-15T03-13-03Z.md) | ✅ `success` | `2026-07-15` `06:43:03` |
| 📄 [2026-07-14T19-36-01Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-14T19-36-01Z.md) | ✅ `success` | `2026-07-14` `23:06:01` |
| 📄 [2026-07-14T14-00-22Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-14T14-00-22Z.md) | ✅ `success` | `2026-07-14` `17:30:22` |
| 📄 [2026-07-14T08-19-36Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-14T08-19-36Z.md) | ✅ `success` | `2026-07-14` `11:49:36` |

<!-- RUN_TABLE_END -->
