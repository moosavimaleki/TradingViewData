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
| 📄 [2026-03-27T13-22-39Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-27T13-22-39Z.md) | ✅ `success` | `2026-03-27` `16:52:39` |
| 📄 [2026-03-27T07-19-10Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-27T07-19-10Z.md) | ✅ `success` | `2026-03-27` `10:49:10` |
| 📄 [2026-03-27T03-17-56Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-27T03-17-56Z.md) | ✅ `success` | `2026-03-27` `06:47:56` |
| 📄 [2026-03-26T19-18-21Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-26T19-18-21Z.md) | ✅ `success` | `2026-03-26` `22:48:21` |
| 📄 [2026-03-26T13-45-10Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-26T13-45-10Z.md) | ✅ `success` | `2026-03-26` `17:15:10` |
| 📄 [2026-03-26T07-20-24Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-26T07-20-24Z.md) | ✅ `success` | `2026-03-26` `10:50:24` |
| 📄 [2026-03-26T02-56-28Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-26T02-56-28Z.md) | ✅ `success` | `2026-03-26` `06:26:28` |
| 📄 [2026-03-25T19-05-21Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-25T19-05-21Z.md) | ✅ `success` | `2026-03-25` `22:35:21` |
| 📄 [2026-03-25T13-39-54Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-25T13-39-54Z.md) | ✅ `success` | `2026-03-25` `17:09:54` |
| 📄 [2026-03-25T07-12-21Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-25T07-12-21Z.md) | ✅ `success` | `2026-03-25` `10:42:21` |

<!-- RUN_TABLE_END -->
