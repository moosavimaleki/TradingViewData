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
| 📄 [2026-04-15T19-37-35Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-15T19-37-35Z.md) | ✅ `success` | `2026-04-15` `23:07:35` |
| 📄 [2026-04-15T13-55-03Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-15T13-55-03Z.md) | ✅ `success` | `2026-04-15` `17:25:03` |
| 📄 [2026-04-15T07-59-13Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-15T07-59-13Z.md) | ❌ `failed` | `2026-04-15` `11:29:13` |
| 📄 [2026-04-15T03-26-33Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-15T03-26-33Z.md) | ✅ `success` | `2026-04-15` `06:56:33` |
| 📄 [2026-04-14T19-26-14Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-14T19-26-14Z.md) | ✅ `success` | `2026-04-14` `22:56:14` |
| 📄 [2026-04-14T14-01-34Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-14T14-01-34Z.md) | ✅ `success` | `2026-04-14` `17:31:34` |
| 📄 [2026-04-14T07-58-13Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-14T07-58-13Z.md) | ✅ `success` | `2026-04-14` `11:28:13` |
| 📄 [2026-04-14T03-27-54Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-14T03-27-54Z.md) | ✅ `success` | `2026-04-14` `06:57:54` |
| 📄 [2026-04-13T19-23-25Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-13T19-23-25Z.md) | ✅ `success` | `2026-04-13` `22:53:25` |
| 📄 [2026-04-13T13-58-03Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-13T13-58-03Z.md) | ✅ `success` | `2026-04-13` `17:28:03` |

<!-- RUN_TABLE_END -->
