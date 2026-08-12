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
| 📄 [2026-08-12T07-41-20Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-12T07-41-20Z.md) | ❌ `failed` | `2026-08-12` `11:11:20` |
| 📄 [2026-08-12T02-28-19Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-12T02-28-19Z.md) | ✅ `success` | `2026-08-12` `05:58:19` |
| 📄 [2026-08-11T19-10-41Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-11T19-10-41Z.md) | ✅ `success` | `2026-08-11` `22:40:41` |
| 📄 [2026-08-11T13-19-41Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-11T13-19-41Z.md) | ✅ `success` | `2026-08-11` `16:49:41` |
| 📄 [2026-08-11T07-17-39Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-11T07-17-39Z.md) | ✅ `success` | `2026-08-11` `10:47:39` |
| 📄 [2026-08-11T02-10-28Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-11T02-10-28Z.md) | ✅ `success` | `2026-08-11` `05:40:28` |
| 📄 [2026-08-10T19-04-49Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-10T19-04-49Z.md) | ✅ `success` | `2026-08-10` `22:34:49` |
| 📄 [2026-08-10T13-23-03Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-10T13-23-03Z.md) | ✅ `success` | `2026-08-10` `16:53:03` |
| 📄 [2026-08-10T07-52-58Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-10T07-52-58Z.md) | ✅ `success` | `2026-08-10` `11:22:58` |
| 📄 [2026-08-10T02-20-15Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-10T02-20-15Z.md) | ✅ `success` | `2026-08-10` `05:50:15` |

<!-- RUN_TABLE_END -->
