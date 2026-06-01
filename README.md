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
| 📄 [2026-06-01T21-40-13Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-01T21-40-13Z.md) | ✅ `success` | `2026-06-02` `01:10:13` |
| 📄 [2026-06-01T17-54-56Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-01T17-54-56Z.md) | ✅ `success` | `2026-06-01` `21:24:56` |
| 📄 [2026-06-01T11-49-10Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-01T11-49-10Z.md) | ✅ `success` | `2026-06-01` `15:19:10` |
| 📄 [2026-06-01T05-00-23Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-01T05-00-23Z.md) | ✅ `success` | `2026-06-01` `08:30:23` |
| 📄 [2026-05-31T19-26-13Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-31T19-26-13Z.md) | ✅ `success` | `2026-05-31` `22:56:13` |
| 📄 [2026-05-31T14-00-37Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-31T14-00-37Z.md) | ✅ `success` | `2026-05-31` `17:30:37` |
| 📄 [2026-05-31T08-55-57Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-31T08-55-57Z.md) | ✅ `success` | `2026-05-31` `12:25:57` |
| 📄 [2026-05-31T04-38-53Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-31T04-38-53Z.md) | ✅ `success` | `2026-05-31` `08:08:53` |
| 📄 [2026-05-30T19-36-08Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-30T19-36-08Z.md) | ✅ `success` | `2026-05-30` `23:06:08` |
| 📄 [2026-05-30T13-55-23Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-30T13-55-23Z.md) | ✅ `success` | `2026-05-30` `17:25:23` |

<!-- RUN_TABLE_END -->
