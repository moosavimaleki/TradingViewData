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
| 📄 [2026-07-12T13-42-18Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-12T13-42-18Z.md) | ✅ `success` | `2026-07-12` `17:12:18` |
| 📄 [2026-07-12T08-26-36Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-12T08-26-36Z.md) | ✅ `success` | `2026-07-12` `11:56:36` |
| 📄 [2026-07-12T03-36-05Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-12T03-36-05Z.md) | ✅ `success` | `2026-07-12` `07:06:05` |
| 📄 [2026-07-11T19-14-12Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-11T19-14-12Z.md) | ✅ `success` | `2026-07-11` `22:44:12` |
| 📄 [2026-07-11T13-41-27Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-11T13-41-27Z.md) | ✅ `success` | `2026-07-11` `17:11:27` |
| 📄 [2026-07-11T08-05-22Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-11T08-05-22Z.md) | ✅ `success` | `2026-07-11` `11:35:22` |
| 📄 [2026-07-11T03-24-20Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-11T03-24-20Z.md) | ✅ `success` | `2026-07-11` `06:54:20` |
| 📄 [2026-07-10T19-42-20Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-10T19-42-20Z.md) | ✅ `success` | `2026-07-10` `23:12:20` |
| 📄 [2026-07-10T14-42-56Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-10T14-42-56Z.md) | ✅ `success` | `2026-07-10` `18:12:56` |
| 📄 [2026-07-10T09-47-35Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-10T09-47-35Z.md) | ✅ `success` | `2026-07-10` `13:17:35` |

<!-- RUN_TABLE_END -->
