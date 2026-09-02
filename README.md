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
| 📄 [2026-09-02T04-04-41Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-02T04-04-41Z.md) | ✅ `success` | `2026-09-02` `07:34:41` |
| 📄 [2026-09-01T20-54-33Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-01T20-54-33Z.md) | ✅ `success` | `2026-09-02` `00:24:33` |
| 📄 [2026-09-01T16-26-19Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-01T16-26-19Z.md) | ✅ `success` | `2026-09-01` `19:56:19` |
| 📄 [2026-09-01T11-29-13Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-01T11-29-13Z.md) | ✅ `success` | `2026-09-01` `14:59:13` |
| 📄 [2026-09-01T04-42-59Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-01T04-42-59Z.md) | ✅ `success` | `2026-09-01` `08:12:59` |
| 📄 [2026-08-31T22-42-59Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-31T22-42-59Z.md) | ✅ `success` | `2026-09-01` `02:12:59` |
| 📄 [2026-08-31T13-22-00Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-31T13-22-00Z.md) | ✅ `success` | `2026-08-31` `16:52:00` |
| 📄 [2026-08-31T05-05-41Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-31T05-05-41Z.md) | ✅ `success` | `2026-08-31` `08:35:41` |
| 📄 [2026-08-30T20-53-15Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-30T20-53-15Z.md) | ✅ `success` | `2026-08-31` `00:23:15` |
| 📄 [2026-08-30T16-30-36Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-30T16-30-36Z.md) | ✅ `success` | `2026-08-30` `20:00:36` |

<!-- RUN_TABLE_END -->
