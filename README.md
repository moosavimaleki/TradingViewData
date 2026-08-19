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
| 📄 [2026-08-19T06-54-12Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-19T06-54-12Z.md) | ❌ `failed` | `2026-08-19` `10:24:12` |
| 📄 [2026-08-19T01-40-54Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-19T01-40-54Z.md) | ✅ `success` | `2026-08-19` `05:10:54` |
| 📄 [2026-08-18T12-57-22Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-18T12-57-22Z.md) | ✅ `success` | `2026-08-18` `16:27:22` |
| 📄 [2026-08-18T06-53-55Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-18T06-53-55Z.md) | ✅ `success` | `2026-08-18` `10:23:55` |
| 📄 [2026-08-18T01-39-07Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-18T01-39-07Z.md) | ✅ `success` | `2026-08-18` `05:09:07` |
| 📄 [2026-08-17T18-48-31Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-17T18-48-31Z.md) | ❌ `failed` | `2026-08-17` `22:18:31` |
| 📄 [2026-08-17T12-55-45Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-17T12-55-45Z.md) | ✅ `success` | `2026-08-17` `16:25:45` |
| 📄 [2026-08-17T07-07-04Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-17T07-07-04Z.md) | ✅ `success` | `2026-08-17` `10:37:04` |
| 📄 [2026-08-17T01-43-37Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-17T01-43-37Z.md) | ✅ `success` | `2026-08-17` `05:13:37` |
| 📄 [2026-08-16T18-36-55Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-16T18-36-55Z.md) | ✅ `success` | `2026-08-16` `22:06:55` |

<!-- RUN_TABLE_END -->
