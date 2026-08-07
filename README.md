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
| 📄 [2026-08-07T07-26-13Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-07T07-26-13Z.md) | ❌ `failed` | `2026-08-07` `10:56:13` |
| 📄 [2026-08-07T00-08-00Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-07T00-08-00Z.md) | ❌ `failed` | `2026-08-07` `03:38:00` |
| 📄 [2026-08-06T14-27-04Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-06T14-27-04Z.md) | ❌ `failed` | `2026-08-06` `17:57:04` |
| 📄 [2026-08-06T08-47-07Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-06T08-47-07Z.md) | ❌ `failed` | `2026-08-06` `12:17:07` |
| 📄 [2026-08-06T03-18-56Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-06T03-18-56Z.md) | ❌ `failed` | `2026-08-06` `06:48:56` |
| 📄 [2026-08-05T19-44-26Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-05T19-44-26Z.md) | ❌ `failed` | `2026-08-05` `23:14:26` |
| 📄 [2026-08-05T14-23-58Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-05T14-23-58Z.md) | ❌ `failed` | `2026-08-05` `17:53:58` |
| 📄 [2026-08-05T08-45-33Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-05T08-45-33Z.md) | ❌ `failed` | `2026-08-05` `12:15:33` |
| 📄 [2026-08-05T03-16-18Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-05T03-16-18Z.md) | ❌ `failed` | `2026-08-05` `06:46:18` |
| 📄 [2026-08-04T19-45-27Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-08-04T19-45-27Z.md) | ❌ `failed` | `2026-08-04` `23:15:27` |

<!-- RUN_TABLE_END -->
