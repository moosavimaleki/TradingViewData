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
| 📄 [2026-08-29T20-48-16Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-29T20-48-16Z.md) | ✅ `success` | `2026-08-30` `00:18:16` |
| 📄 [2026-08-29T16-35-31Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-29T16-35-31Z.md) | ✅ `success` | `2026-08-29` `20:05:31` |
| 📄 [2026-08-29T06-46-17Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-29T06-46-17Z.md) | ✅ `success` | `2026-08-29` `10:16:17` |
| 📄 [2026-08-28T22-07-25Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-28T22-07-25Z.md) | ✅ `success` | `2026-08-29` `01:37:25` |
| 📄 [2026-08-28T11-01-21Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-28T11-01-21Z.md) | ✅ `success` | `2026-08-28` `14:31:21` |
| 📄 [2026-08-27T22-08-15Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-27T22-08-15Z.md) | ✅ `success` | `2026-08-28` `01:38:15` |
| 📄 [2026-08-27T08-48-28Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-27T08-48-28Z.md) | ✅ `success` | `2026-08-27` `12:18:28` |
| 📄 [2026-08-26T19-54-42Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-26T19-54-42Z.md) | ✅ `success` | `2026-08-26` `23:24:42` |
| 📄 [2026-08-26T13-04-24Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-26T13-04-24Z.md) | ❌ `failed` | `2026-08-26` `16:34:24` |
| 📄 [2026-08-26T06-58-36Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-26T06-58-36Z.md) | ❌ `failed` | `2026-08-26` `10:28:36` |

<!-- RUN_TABLE_END -->
