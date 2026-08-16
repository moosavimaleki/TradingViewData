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
| 📄 [2026-08-16T12-51-08Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-16T12-51-08Z.md) | ✅ `success` | `2026-08-16` `16:21:08` |
| 📄 [2026-08-16T06-50-13Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-16T06-50-13Z.md) | ✅ `success` | `2026-08-16` `10:20:13` |
| 📄 [2026-08-16T03-14-47Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-16T03-14-47Z.md) | ✅ `success` | `2026-08-16` `06:44:47` |
| 📄 [2026-08-15T18-37-50Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-15T18-37-50Z.md) | ✅ `success` | `2026-08-15` `22:07:50` |
| 📄 [2026-08-15T12-49-31Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-15T12-49-31Z.md) | ✅ `success` | `2026-08-15` `16:19:31` |
| 📄 [2026-08-15T06-48-30Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-15T06-48-30Z.md) | ✅ `success` | `2026-08-15` `10:18:30` |
| 📄 [2026-08-15T01-38-53Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-15T01-38-53Z.md) | ✅ `success` | `2026-08-15` `05:08:53` |
| 📄 [2026-08-14T19-02-17Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-14T19-02-17Z.md) | ✅ `success` | `2026-08-14` `22:32:17` |
| 📄 [2026-08-14T13-20-17Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-14T13-20-17Z.md) | ✅ `success` | `2026-08-14` `16:50:17` |
| 📄 [2026-08-14T07-40-58Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-14T07-40-58Z.md) | ✅ `success` | `2026-08-14` `11:10:58` |

<!-- RUN_TABLE_END -->
