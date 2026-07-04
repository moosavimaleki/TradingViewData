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
| 📄 [2026-07-04T08-46-17Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-04T08-46-17Z.md) | ✅ `success` | `2026-07-04` `12:16:17` |
| 📄 [2026-07-04T03-48-20Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-04T03-48-20Z.md) | ✅ `success` | `2026-07-04` `07:18:20` |
| 📄 [2026-07-03T19-39-12Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-03T19-39-12Z.md) | ✅ `success` | `2026-07-03` `23:09:12` |
| 📄 [2026-07-03T14-24-09Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-03T14-24-09Z.md) | ✅ `success` | `2026-07-03` `17:54:09` |
| 📄 [2026-07-03T09-29-23Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-03T09-29-23Z.md) | ✅ `success` | `2026-07-03` `12:59:23` |
| 📄 [2026-07-03T03-54-49Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-03T03-54-49Z.md) | ✅ `success` | `2026-07-03` `07:24:49` |
| 📄 [2026-07-02T19-42-00Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-02T19-42-00Z.md) | ✅ `success` | `2026-07-02` `23:12:00` |
| 📄 [2026-07-02T14-19-43Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-02T14-19-43Z.md) | ✅ `success` | `2026-07-02` `17:49:43` |
| 📄 [2026-07-02T09-25-13Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-02T09-25-13Z.md) | ✅ `success` | `2026-07-02` `12:55:13` |
| 📄 [2026-07-02T04-08-23Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-02T04-08-23Z.md) | ✅ `success` | `2026-07-02` `07:38:23` |

<!-- RUN_TABLE_END -->
