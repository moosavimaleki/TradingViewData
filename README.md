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
| 📄 [2026-07-29T14-23-52Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-29T14-23-52Z.md) | ❌ `failed` | `2026-07-29` `17:53:52` |
| 📄 [2026-07-29T08-49-39Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-29T08-49-39Z.md) | ❌ `failed` | `2026-07-29` `12:19:39` |
| 📄 [2026-07-29T03-19-51Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-29T03-19-51Z.md) | ❌ `failed` | `2026-07-29` `06:49:51` |
| 📄 [2026-07-28T19-41-42Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-28T19-41-42Z.md) | ❌ `failed` | `2026-07-28` `23:11:42` |
| 📄 [2026-07-28T14-25-07Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-28T14-25-07Z.md) | ❌ `failed` | `2026-07-28` `17:55:07` |
| 📄 [2026-07-28T08-45-38Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-28T08-45-38Z.md) | ❌ `failed` | `2026-07-28` `12:15:38` |
| 📄 [2026-07-28T03-17-20Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-28T03-17-20Z.md) | ✅ `success` | `2026-07-28` `06:47:20` |
| 📄 [2026-07-27T19-44-33Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-27T19-44-33Z.md) | ✅ `success` | `2026-07-27` `23:14:33` |
| 📄 [2026-07-27T14-50-53Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-27T14-50-53Z.md) | ✅ `success` | `2026-07-27` `18:20:53` |
| 📄 [2026-07-27T10-02-38Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-27T10-02-38Z.md) | ✅ `success` | `2026-07-27` `13:32:38` |

<!-- RUN_TABLE_END -->
