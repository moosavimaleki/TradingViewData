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
| 📄 [2026-07-30T19-42-20Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-30T19-42-20Z.md) | ❌ `failed` | `2026-07-30` `23:12:20` |
| 📄 [2026-07-30T14-20-35Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-30T14-20-35Z.md) | ❌ `failed` | `2026-07-30` `17:50:35` |
| 📄 [2026-07-30T08-39-22Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-30T08-39-22Z.md) | ❌ `failed` | `2026-07-30` `12:09:22` |
| 📄 [2026-07-30T02-53-05Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-30T02-53-05Z.md) | ❌ `failed` | `2026-07-30` `06:23:05` |
| 📄 [2026-07-29T19-26-42Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-29T19-26-42Z.md) | ❌ `failed` | `2026-07-29` `22:56:42` |
| 📄 [2026-07-29T14-23-52Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-29T14-23-52Z.md) | ❌ `failed` | `2026-07-29` `17:53:52` |
| 📄 [2026-07-29T08-49-39Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-29T08-49-39Z.md) | ❌ `failed` | `2026-07-29` `12:19:39` |
| 📄 [2026-07-29T03-19-51Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-29T03-19-51Z.md) | ❌ `failed` | `2026-07-29` `06:49:51` |
| 📄 [2026-07-28T19-41-42Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-28T19-41-42Z.md) | ❌ `failed` | `2026-07-28` `23:11:42` |
| 📄 [2026-07-28T14-25-07Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-28T14-25-07Z.md) | ❌ `failed` | `2026-07-28` `17:55:07` |

<!-- RUN_TABLE_END -->
