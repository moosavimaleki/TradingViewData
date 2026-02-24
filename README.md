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
| 📄 [2026-02-24T02-46-52Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-24T02-46-52Z.md) | ✅ `success` | `2026-02-24` `06:16:52` |
| 📄 [2026-02-23T19-15-35Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-23T19-15-35Z.md) | ✅ `success` | `2026-02-23` `22:45:35` |
| 📄 [2026-02-23T13-21-59Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-23T13-21-59Z.md) | ✅ `success` | `2026-02-23` `16:51:59` |
| 📄 [2026-02-23T07-16-01Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-23T07-16-01Z.md) | ✅ `success` | `2026-02-23` `10:46:01` |
| 📄 [2026-02-23T02-49-56Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-23T02-49-56Z.md) | ✅ `success` | `2026-02-23` `06:19:56` |
| 📄 [2026-02-22T19-53-13Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-22T19-53-13Z.md) | ✅ `success` | `2026-02-22` `23:23:13` |
| 📄 [2026-02-22T18-47-39Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-22T18-47-39Z.md) | ✅ `success` | `2026-02-22` `22:17:39` |
| 📄 [2026-02-22T13-05-37Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-22T13-05-37Z.md) | ❌ `failed` | `2026-02-22` `16:35:37` |
| 📄 [2026-02-22T06-58-12Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-22T06-58-12Z.md) | ✅ `success` | `2026-02-22` `10:28:12` |
| 📄 [2026-02-22T02-49-42Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-02-22T02-49-42Z.md) | ✅ `success` | `2026-02-22` `06:19:42` |

<!-- RUN_TABLE_END -->
