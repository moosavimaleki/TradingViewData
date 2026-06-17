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
| 📄 [2026-06-17T15-53-10Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-17T15-53-10Z.md) | ✅ `success` | `2026-06-17` `19:23:10` |
| 📄 [2026-06-17T11-09-24Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-17T11-09-24Z.md) | ✅ `success` | `2026-06-17` `14:39:24` |
| 📄 [2026-06-17T04-55-18Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-17T04-55-18Z.md) | ✅ `success` | `2026-06-17` `08:25:18` |
| 📄 [2026-06-16T21-11-52Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-16T21-11-52Z.md) | ✅ `success` | `2026-06-17` `00:41:52` |
| 📄 [2026-06-16T17-09-38Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-16T17-09-38Z.md) | ✅ `success` | `2026-06-16` `20:39:38` |
| 📄 [2026-06-16T11-25-13Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-16T11-25-13Z.md) | ✅ `success` | `2026-06-16` `14:55:13` |
| 📄 [2026-06-16T05-12-55Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-16T05-12-55Z.md) | ✅ `success` | `2026-06-16` `08:42:55` |
| 📄 [2026-06-15T21-12-22Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-15T21-12-22Z.md) | ✅ `success` | `2026-06-16` `00:42:22` |
| 📄 [2026-06-15T12-32-28Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-15T12-32-28Z.md) | ❌ `failed` | `2026-06-15` `16:02:28` |
| 📄 [2026-06-15T05-09-53Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-15T05-09-53Z.md) | ✅ `success` | `2026-06-15` `08:39:53` |

<!-- RUN_TABLE_END -->
