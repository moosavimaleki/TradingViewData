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
| 📄 [2026-09-11T04-13-39Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-11T04-13-39Z.md) | ✅ `success` | `2026-09-11` `07:43:39` |
| 📄 [2026-09-10T20-43-40Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-10T20-43-40Z.md) | ✅ `success` | `2026-09-11` `00:13:40` |
| 📄 [2026-09-10T16-13-45Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-10T16-13-45Z.md) | ✅ `success` | `2026-09-10` `19:43:45` |
| 📄 [2026-09-10T11-03-03Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-10T11-03-03Z.md) | ✅ `success` | `2026-09-10` `14:33:03` |
| 📄 [2026-09-10T04-14-04Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-10T04-14-04Z.md) | ✅ `success` | `2026-09-10` `07:44:04` |
| 📄 [2026-09-09T20-48-33Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-09T20-48-33Z.md) | ✅ `success` | `2026-09-10` `00:18:33` |
| 📄 [2026-09-09T16-24-09Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-09T16-24-09Z.md) | ✅ `success` | `2026-09-09` `19:54:09` |
| 📄 [2026-09-09T11-06-54Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-09T11-06-54Z.md) | ✅ `success` | `2026-09-09` `14:36:54` |
| 📄 [2026-09-09T04-17-00Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-09T04-17-00Z.md) | ✅ `success` | `2026-09-09` `07:47:00` |
| 📄 [2026-09-08T21-00-14Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-08T21-00-14Z.md) | ✅ `success` | `2026-09-09` `00:30:14` |

<!-- RUN_TABLE_END -->
