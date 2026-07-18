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
| 📄 [2026-07-18T08-02-29Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-18T08-02-29Z.md) | ✅ `success` | `2026-07-18` `11:32:29` |
| 📄 [2026-07-18T03-12-11Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-18T03-12-11Z.md) | ✅ `success` | `2026-07-18` `06:42:11` |
| 📄 [2026-07-17T19-19-57Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-17T19-19-57Z.md) | ✅ `success` | `2026-07-17` `22:49:57` |
| 📄 [2026-07-17T13-52-52Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-17T13-52-52Z.md) | ✅ `success` | `2026-07-17` `17:22:52` |
| 📄 [2026-07-17T08-20-28Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-17T08-20-28Z.md) | ✅ `success` | `2026-07-17` `11:50:28` |
| 📄 [2026-07-17T03-22-46Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-17T03-22-46Z.md) | ✅ `success` | `2026-07-17` `06:52:46` |
| 📄 [2026-07-16T19-21-56Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-16T19-21-56Z.md) | ✅ `success` | `2026-07-16` `22:51:56` |
| 📄 [2026-07-16T14-08-59Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-16T14-08-59Z.md) | ❌ `failed` | `2026-07-16` `17:38:59` |
| 📄 [2026-07-16T08-24-12Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-16T08-24-12Z.md) | ✅ `success` | `2026-07-16` `11:54:12` |
| 📄 [2026-07-16T03-19-47Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-16T03-19-47Z.md) | ✅ `success` | `2026-07-16` `06:49:47` |

<!-- RUN_TABLE_END -->
