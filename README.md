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
| 📄 [2026-05-30T13-55-23Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-30T13-55-23Z.md) | ✅ `success` | `2026-05-30` `17:25:23` |
| 📄 [2026-05-30T08-35-30Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-30T08-35-30Z.md) | ✅ `success` | `2026-05-30` `12:05:30` |
| 📄 [2026-05-30T04-03-16Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-30T04-03-16Z.md) | ✅ `success` | `2026-05-30` `07:33:16` |
| 📄 [2026-05-29T20-33-58Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-29T20-33-58Z.md) | ✅ `success` | `2026-05-30` `00:03:58` |
| 📄 [2026-05-29T15-58-55Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-29T15-58-55Z.md) | ✅ `success` | `2026-05-29` `19:28:55` |
| 📄 [2026-05-29T10-06-30Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-29T10-06-30Z.md) | ✅ `success` | `2026-05-29` `13:36:30` |
| 📄 [2026-05-29T04-18-27Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-29T04-18-27Z.md) | ✅ `success` | `2026-05-29` `07:48:27` |
| 📄 [2026-05-28T20-32-23Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-28T20-32-23Z.md) | ✅ `success` | `2026-05-29` `00:02:23` |
| 📄 [2026-05-28T16-16-10Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-28T16-16-10Z.md) | ✅ `success` | `2026-05-28` `19:46:10` |
| 📄 [2026-05-28T10-17-32Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-28T10-17-32Z.md) | ❌ `failed` | `2026-05-28` `13:47:32` |

<!-- RUN_TABLE_END -->
