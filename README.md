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
| 📄 [2026-06-20T19-47-10Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-20T19-47-10Z.md) | ✅ `success` | `2026-06-20` `23:17:10` |
| 📄 [2026-06-20T14-19-54Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-20T14-19-54Z.md) | ✅ `success` | `2026-06-20` `17:49:54` |
| 📄 [2026-06-20T09-29-09Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-20T09-29-09Z.md) | ✅ `success` | `2026-06-20` `12:59:09` |
| 📄 [2026-06-20T04-18-44Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-20T04-18-44Z.md) | ✅ `success` | `2026-06-20` `07:48:44` |
| 📄 [2026-06-19T19-56-50Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-19T19-56-50Z.md) | ✅ `success` | `2026-06-19` `23:26:50` |
| 📄 [2026-06-19T15-34-42Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-19T15-34-42Z.md) | ✅ `success` | `2026-06-19` `19:04:42` |
| 📄 [2026-06-19T10-49-16Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-19T10-49-16Z.md) | ✅ `success` | `2026-06-19` `14:19:16` |
| 📄 [2026-06-19T05-06-00Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-19T05-06-00Z.md) | ✅ `success` | `2026-06-19` `08:36:00` |
| 📄 [2026-06-18T20-33-33Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-18T20-33-33Z.md) | ❌ `failed` | `2026-06-19` `00:03:33` |
| 📄 [2026-06-18T15-41-35Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-18T15-41-35Z.md) | ✅ `success` | `2026-06-18` `19:11:35` |

<!-- RUN_TABLE_END -->
