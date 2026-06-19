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
| 📄 [2026-06-18T20-33-33Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-18T20-33-33Z.md) | ❌ `failed` | `2026-06-19` `00:03:33` |
| 📄 [2026-06-18T15-41-35Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-18T15-41-35Z.md) | ✅ `success` | `2026-06-18` `19:11:35` |
| 📄 [2026-06-18T10-40-32Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-18T10-40-32Z.md) | ❌ `failed` | `2026-06-18` `14:10:32` |
| 📄 [2026-06-18T04-46-13Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-18T04-46-13Z.md) | ✅ `success` | `2026-06-18` `08:16:13` |
| 📄 [2026-06-17T20-23-16Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-17T20-23-16Z.md) | ✅ `success` | `2026-06-17` `23:53:16` |
| 📄 [2026-06-17T15-53-10Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-17T15-53-10Z.md) | ✅ `success` | `2026-06-17` `19:23:10` |
| 📄 [2026-06-17T11-09-24Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-17T11-09-24Z.md) | ✅ `success` | `2026-06-17` `14:39:24` |
| 📄 [2026-06-17T04-55-18Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-17T04-55-18Z.md) | ✅ `success` | `2026-06-17` `08:25:18` |
| 📄 [2026-06-16T21-11-52Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-16T21-11-52Z.md) | ✅ `success` | `2026-06-17` `00:41:52` |
| 📄 [2026-06-16T17-09-38Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-16T17-09-38Z.md) | ✅ `success` | `2026-06-16` `20:39:38` |

<!-- RUN_TABLE_END -->
