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
| 📄 [2026-06-16T05-12-55Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-16T05-12-55Z.md) | ✅ `success` | `2026-06-16` `08:42:55` |
| 📄 [2026-06-15T21-12-22Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-15T21-12-22Z.md) | ✅ `success` | `2026-06-16` `00:42:22` |
| 📄 [2026-06-15T12-32-28Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-15T12-32-28Z.md) | ❌ `failed` | `2026-06-15` `16:02:28` |
| 📄 [2026-06-15T05-09-53Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-15T05-09-53Z.md) | ✅ `success` | `2026-06-15` `08:39:53` |
| 📄 [2026-06-14T19-46-30Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-14T19-46-30Z.md) | ✅ `success` | `2026-06-14` `23:16:30` |
| 📄 [2026-06-14T14-19-18Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-14T14-19-18Z.md) | ✅ `success` | `2026-06-14` `17:49:18` |
| 📄 [2026-06-14T09-48-11Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-14T09-48-11Z.md) | ✅ `success` | `2026-06-14` `13:18:11` |
| 📄 [2026-06-14T04-52-54Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-14T04-52-54Z.md) | ✅ `success` | `2026-06-14` `08:22:54` |
| 📄 [2026-06-13T19-45-37Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-13T19-45-37Z.md) | ✅ `success` | `2026-06-13` `23:15:37` |
| 📄 [2026-06-13T14-15-39Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-13T14-15-39Z.md) | ✅ `success` | `2026-06-13` `17:45:39` |

<!-- RUN_TABLE_END -->
