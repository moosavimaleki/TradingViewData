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
| 📄 [2026-10-30T05-23-26Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-30T05-23-26Z.md) | ✅ `success` | `2026-10-30` `08:53:26` |
| 📄 [2026-10-29T22-39-03Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-29T22-39-03Z.md) | ✅ `success` | `2026-10-30` `02:09:03` |
| 📄 [2026-10-29T12-44-15Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-29T12-44-15Z.md) | ❌ `failed` | `2026-10-29` `16:14:15` |
| 📄 [2026-10-29T05-23-43Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-29T05-23-43Z.md) | ✅ `success` | `2026-10-29` `08:53:43` |
| 📄 [2026-10-28T22-26-30Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-28T22-26-30Z.md) | ✅ `success` | `2026-10-29` `01:56:30` |
| 📄 [2026-10-28T12-33-55Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-28T12-33-55Z.md) | ✅ `success` | `2026-10-28` `16:03:55` |
| 📄 [2026-10-28T05-12-28Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-28T05-12-28Z.md) | ✅ `success` | `2026-10-28` `08:42:28` |
| 📄 [2026-10-27T22-02-19Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-27T22-02-19Z.md) | ❌ `failed` | `2026-10-28` `01:32:19` |
| 📄 [2026-10-27T17-52-34Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-27T17-52-34Z.md) | ❌ `failed` | `2026-10-27` `21:22:34` |
| 📄 [2026-10-27T11-56-28Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-27T11-56-28Z.md) | ❌ `failed` | `2026-10-27` `15:26:28` |

<!-- RUN_TABLE_END -->
