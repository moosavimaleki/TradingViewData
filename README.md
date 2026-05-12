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
| 📄 [2026-05-12T20-02-33Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-12T20-02-33Z.md) | ✅ `success` | `2026-05-12` `23:32:33` |
| 📄 [2026-05-12T14-40-21Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-12T14-40-21Z.md) | ✅ `success` | `2026-05-12` `18:10:21` |
| 📄 [2026-05-12T08-49-21Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-12T08-49-21Z.md) | ✅ `success` | `2026-05-12` `12:19:21` |
| 📄 [2026-05-12T03-52-36Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-12T03-52-36Z.md) | ✅ `success` | `2026-05-12` `07:22:36` |
| 📄 [2026-05-11T19-57-02Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-11T19-57-02Z.md) | ✅ `success` | `2026-05-11` `23:27:02` |
| 📄 [2026-05-11T15-27-56Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-11T15-27-56Z.md) | ✅ `success` | `2026-05-11` `18:57:56` |
| 📄 [2026-05-11T09-54-10Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-11T09-54-10Z.md) | ✅ `success` | `2026-05-11` `13:24:10` |
| 📄 [2026-05-11T04-08-53Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-11T04-08-53Z.md) | ✅ `success` | `2026-05-11` `07:38:53` |
| 📄 [2026-05-10T19-14-23Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-10T19-14-23Z.md) | ✅ `success` | `2026-05-10` `22:44:23` |
| 📄 [2026-05-10T13-44-07Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-05-10T13-44-07Z.md) | ✅ `success` | `2026-05-10` `17:14:07` |

<!-- RUN_TABLE_END -->
