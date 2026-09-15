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
| 📄 [2026-09-15T16-45-02Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-15T16-45-02Z.md) | ✅ `success` | `2026-09-15` `20:15:02` |
| 📄 [2026-09-15T11-31-37Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-15T11-31-37Z.md) | ❌ `failed` | `2026-09-15` `15:01:37` |
| 📄 [2026-09-15T04-31-37Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-15T04-31-37Z.md) | ✅ `success` | `2026-09-15` `08:01:37` |
| 📄 [2026-09-14T21-42-45Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-14T21-42-45Z.md) | ✅ `success` | `2026-09-15` `01:12:45` |
| 📄 [2026-09-14T12-27-33Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-14T12-27-33Z.md) | ✅ `success` | `2026-09-14` `15:57:33` |
| 📄 [2026-09-14T04-31-41Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-14T04-31-41Z.md) | ✅ `success` | `2026-09-14` `08:01:41` |
| 📄 [2026-09-13T20-37-03Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-13T20-37-03Z.md) | ✅ `success` | `2026-09-14` `00:07:03` |
| 📄 [2026-09-13T16-01-45Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-13T16-01-45Z.md) | ✅ `success` | `2026-09-13` `19:31:45` |
| 📄 [2026-09-13T11-33-30Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-13T11-33-30Z.md) | ✅ `success` | `2026-09-13` `15:03:30` |
| 📄 [2026-09-13T04-25-01Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-13T04-25-01Z.md) | ✅ `success` | `2026-09-13` `07:55:01` |

<!-- RUN_TABLE_END -->
