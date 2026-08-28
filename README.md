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
| 📄 [2026-08-28T22-07-25Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-28T22-07-25Z.md) | ✅ `success` | `2026-08-29` `01:37:25` |
| 📄 [2026-08-28T11-01-21Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-28T11-01-21Z.md) | ✅ `success` | `2026-08-28` `14:31:21` |
| 📄 [2026-08-27T22-08-15Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-27T22-08-15Z.md) | ✅ `success` | `2026-08-28` `01:38:15` |
| 📄 [2026-08-27T08-48-28Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-27T08-48-28Z.md) | ✅ `success` | `2026-08-27` `12:18:28` |
| 📄 [2026-08-26T19-54-42Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-26T19-54-42Z.md) | ✅ `success` | `2026-08-26` `23:24:42` |
| 📄 [2026-08-26T13-04-24Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-26T13-04-24Z.md) | ❌ `failed` | `2026-08-26` `16:34:24` |
| 📄 [2026-08-26T06-58-36Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-26T06-58-36Z.md) | ❌ `failed` | `2026-08-26` `10:28:36` |
| 📄 [2026-08-26T01-45-30Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-26T01-45-30Z.md) | ✅ `success` | `2026-08-26` `05:15:30` |
| 📄 [2026-08-25T18-48-02Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-25T18-48-02Z.md) | ✅ `success` | `2026-08-25` `22:18:02` |
| 📄 [2026-08-25T12-58-38Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-25T12-58-38Z.md) | ✅ `success` | `2026-08-25` `16:28:38` |

<!-- RUN_TABLE_END -->
