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
| 📄 [2026-05-28T20-32-23Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-28T20-32-23Z.md) | ✅ `success` | `2026-05-29` `00:02:23` |
| 📄 [2026-05-28T16-16-10Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-28T16-16-10Z.md) | ✅ `success` | `2026-05-28` `19:46:10` |
| 📄 [2026-05-28T10-17-32Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-28T10-17-32Z.md) | ❌ `failed` | `2026-05-28` `13:47:32` |
| 📄 [2026-05-28T04-16-15Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-28T04-16-15Z.md) | ✅ `success` | `2026-05-28` `07:46:15` |
| 📄 [2026-05-27T20-25-53Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-27T20-25-53Z.md) | ✅ `success` | `2026-05-27` `23:55:53` |
| 📄 [2026-05-27T16-01-33Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-27T16-01-33Z.md) | ✅ `success` | `2026-05-27` `19:31:33` |
| 📄 [2026-05-27T10-08-25Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-27T10-08-25Z.md) | ❌ `failed` | `2026-05-27` `13:38:25` |
| 📄 [2026-05-27T04-25-58Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-27T04-25-58Z.md) | ✅ `success` | `2026-05-27` `07:55:58` |
| 📄 [2026-05-26T20-21-08Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-26T20-21-08Z.md) | ✅ `success` | `2026-05-26` `23:51:08` |
| 📄 [2026-05-26T15-57-38Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-26T15-57-38Z.md) | ✅ `success` | `2026-05-26` `19:27:38` |

<!-- RUN_TABLE_END -->
