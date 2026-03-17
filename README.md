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
| 📄 [2026-03-17T13-41-04Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-17T13-41-04Z.md) | ✅ `success` | `2026-03-17` `17:11:04` |
| 📄 [2026-03-17T07-14-33Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-17T07-14-33Z.md) | ✅ `success` | `2026-03-17` `10:44:33` |
| 📄 [2026-03-17T02-44-19Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-17T02-44-19Z.md) | ✅ `success` | `2026-03-17` `06:14:19` |
| 📄 [2026-03-16T19-14-22Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-16T19-14-22Z.md) | ✅ `success` | `2026-03-16` `22:44:22` |
| 📄 [2026-03-16T13-43-23Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-16T13-43-23Z.md) | ❌ `failed` | `2026-03-16` `17:13:23` |
| 📄 [2026-03-16T07-41-46Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-16T07-41-46Z.md) | ✅ `success` | `2026-03-16` `11:11:46` |
| 📄 [2026-03-16T03-20-58Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-16T03-20-58Z.md) | ✅ `success` | `2026-03-16` `06:50:58` |
| 📄 [2026-03-15T18-51-48Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-15T18-51-48Z.md) | ✅ `success` | `2026-03-15` `22:21:48` |
| 📄 [2026-03-15T13-09-15Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-15T13-09-15Z.md) | ✅ `success` | `2026-03-15` `16:39:15` |
| 📄 [2026-03-15T07-08-23Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-15T07-08-23Z.md) | ✅ `success` | `2026-03-15` `10:38:23` |

<!-- RUN_TABLE_END -->
