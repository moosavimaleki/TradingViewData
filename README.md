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
| 📄 [2026-04-02T07-23-57Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-02T07-23-57Z.md) | ✅ `success` | `2026-04-02` `10:53:57` |
| 📄 [2026-04-02T02-54-25Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-02T02-54-25Z.md) | ✅ `success` | `2026-04-02` `06:24:25` |
| 📄 [2026-04-01T19-13-59Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-01T19-13-59Z.md) | ✅ `success` | `2026-04-01` `22:43:59` |
| 📄 [2026-04-01T13-53-38Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-01T13-53-38Z.md) | ✅ `success` | `2026-04-01` `17:23:38` |
| 📄 [2026-04-01T07-44-55Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-01T07-44-55Z.md) | ✅ `success` | `2026-04-01` `11:14:55` |
| 📄 [2026-04-01T03-29-14Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-01T03-29-14Z.md) | ✅ `success` | `2026-04-01` `06:59:14` |
| 📄 [2026-03-31T19-12-25Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-31T19-12-25Z.md) | ✅ `success` | `2026-03-31` `22:42:25` |
| 📄 [2026-03-31T13-50-09Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-31T13-50-09Z.md) | ✅ `success` | `2026-03-31` `17:20:09` |
| 📄 [2026-03-31T07-39-15Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-31T07-39-15Z.md) | ✅ `success` | `2026-03-31` `11:09:15` |
| 📄 [2026-03-31T03-16-45Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-31T03-16-45Z.md) | ✅ `success` | `2026-03-31` `06:46:45` |

<!-- RUN_TABLE_END -->
