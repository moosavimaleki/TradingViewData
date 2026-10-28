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
| 📄 [2026-10-28T12-33-55Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-28T12-33-55Z.md) | ✅ `success` | `2026-10-28` `16:03:55` |
| 📄 [2026-10-28T05-12-28Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-28T05-12-28Z.md) | ✅ `success` | `2026-10-28` `08:42:28` |
| 📄 [2026-10-27T22-02-19Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-27T22-02-19Z.md) | ❌ `failed` | `2026-10-28` `01:32:19` |
| 📄 [2026-10-27T17-52-34Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-27T17-52-34Z.md) | ❌ `failed` | `2026-10-27` `21:22:34` |
| 📄 [2026-10-27T11-56-28Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-27T11-56-28Z.md) | ❌ `failed` | `2026-10-27` `15:26:28` |
| 📄 [2026-10-27T04-38-56Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-27T04-38-56Z.md) | ❌ `failed` | `2026-10-27` `08:08:56` |
| 📄 [2026-10-26T22-32-06Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-26T22-32-06Z.md) | ❌ `failed` | `2026-10-27` `02:02:06` |
| 📄 [2026-10-26T12-41-29Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-26T12-41-29Z.md) | ❌ `failed` | `2026-10-26` `16:11:29` |
| 📄 [2026-10-26T04-19-53Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-26T04-19-53Z.md) | ❌ `failed` | `2026-10-26` `07:49:53` |
| 📄 [2026-10-25T20-40-59Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-25T20-40-59Z.md) | ✅ `success` | `2026-10-26` `00:10:59` |

<!-- RUN_TABLE_END -->
