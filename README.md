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
| 📄 [2026-05-24T08-39-25Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-24T08-39-25Z.md) | ✅ `success` | `2026-05-24` `12:09:25` |
| 📄 [2026-05-24T04-16-05Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-24T04-16-05Z.md) | ✅ `success` | `2026-05-24` `07:46:05` |
| 📄 [2026-05-23T19-21-09Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-23T19-21-09Z.md) | ✅ `success` | `2026-05-23` `22:51:09` |
| 📄 [2026-05-23T13-52-38Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-23T13-52-38Z.md) | ✅ `success` | `2026-05-23` `17:22:38` |
| 📄 [2026-05-23T08-27-35Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-23T08-27-35Z.md) | ✅ `success` | `2026-05-23` `11:57:35` |
| 📄 [2026-05-23T03-55-34Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-23T03-55-34Z.md) | ✅ `success` | `2026-05-23` `07:25:34` |
| 📄 [2026-05-22T19-57-56Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-22T19-57-56Z.md) | ✅ `success` | `2026-05-22` `23:27:56` |
| 📄 [2026-05-22T14-52-46Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-22T14-52-46Z.md) | ✅ `success` | `2026-05-22` `18:22:46` |
| 📄 [2026-05-22T09-40-48Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-22T09-40-48Z.md) | ✅ `success` | `2026-05-22` `13:10:48` |
| 📄 [2026-05-22T04-17-13Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-22T04-17-13Z.md) | ✅ `success` | `2026-05-22` `07:47:13` |

<!-- RUN_TABLE_END -->
