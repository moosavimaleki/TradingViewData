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
| 📄 [2026-09-28T04-57-54Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-28T04-57-54Z.md) | ✅ `success` | `2026-09-28` `08:27:54` |
| 📄 [2026-09-27T21-12-37Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-27T21-12-37Z.md) | ✅ `success` | `2026-09-28` `00:42:37` |
| 📄 [2026-09-27T16-48-12Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-27T16-48-12Z.md) | ✅ `success` | `2026-09-27` `20:18:12` |
| 📄 [2026-09-27T11-49-35Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-27T11-49-35Z.md) | ✅ `success` | `2026-09-27` `15:19:35` |
| 📄 [2026-09-27T04-56-43Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-27T04-56-43Z.md) | ✅ `success` | `2026-09-27` `08:26:43` |
| 📄 [2026-09-26T20-56-04Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-26T20-56-04Z.md) | ✅ `success` | `2026-09-27` `00:26:04` |
| 📄 [2026-09-26T16-12-23Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-26T16-12-23Z.md) | ✅ `success` | `2026-09-26` `19:42:23` |
| 📄 [2026-09-26T11-11-11Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-26T11-11-11Z.md) | ✅ `success` | `2026-09-26` `14:41:11` |
| 📄 [2026-09-26T04-36-33Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-26T04-36-33Z.md) | ✅ `success` | `2026-09-26` `08:06:33` |
| 📄 [2026-09-25T21-24-23Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-25T21-24-23Z.md) | ✅ `success` | `2026-09-26` `00:54:23` |

<!-- RUN_TABLE_END -->
