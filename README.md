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
| 📄 [2026-05-26T04-13-06Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-26T04-13-06Z.md) | ✅ `success` | `2026-05-26` `07:43:06` |
| 📄 [2026-05-25T19-50-55Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-25T19-50-55Z.md) | ✅ `success` | `2026-05-25` `23:20:55` |
| 📄 [2026-05-25T15-21-50Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-25T15-21-50Z.md) | ✅ `success` | `2026-05-25` `18:51:50` |
| 📄 [2026-05-25T10-22-40Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-25T10-22-40Z.md) | ❌ `failed` | `2026-05-25` `13:52:40` |
| 📄 [2026-05-25T04-26-50Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-25T04-26-50Z.md) | ✅ `success` | `2026-05-25` `07:56:50` |
| 📄 [2026-05-24T19-24-59Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-24T19-24-59Z.md) | ✅ `success` | `2026-05-24` `22:54:59` |
| 📄 [2026-05-24T13-49-29Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-24T13-49-29Z.md) | ✅ `success` | `2026-05-24` `17:19:29` |
| 📄 [2026-05-24T08-39-25Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-24T08-39-25Z.md) | ✅ `success` | `2026-05-24` `12:09:25` |
| 📄 [2026-05-24T04-16-05Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-24T04-16-05Z.md) | ✅ `success` | `2026-05-24` `07:46:05` |
| 📄 [2026-05-23T19-21-09Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-23T19-21-09Z.md) | ✅ `success` | `2026-05-23` `22:51:09` |

<!-- RUN_TABLE_END -->
