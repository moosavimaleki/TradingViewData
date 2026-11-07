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
| 📄 [2026-11-07T21-40-33Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-07T21-40-33Z.md) | ✅ `success` | `2026-11-08` `01:10:33` |
| 📄 [2026-11-07T12-47-45Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-07T12-47-45Z.md) | ✅ `success` | `2026-11-07` `16:17:45` |
| 📄 [2026-11-07T05-37-40Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-07T05-37-40Z.md) | ✅ `success` | `2026-11-07` `09:07:40` |
| 📄 [2026-11-06T19-11-56Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-06T19-11-56Z.md) | ✅ `success` | `2026-11-06` `22:41:56` |
| 📄 [2026-11-06T06-06-25Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-06T06-06-25Z.md) | ✅ `success` | `2026-11-06` `09:36:25` |
| 📄 [2026-11-05T19-47-10Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-05T19-47-10Z.md) | ❌ `failed` | `2026-11-05` `23:17:10` |
| 📄 [2026-11-05T06-12-26Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-05T06-12-26Z.md) | ❌ `failed` | `2026-11-05` `09:42:26` |
| 📄 [2026-11-04T23-29-12Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-04T23-29-12Z.md) | ✅ `success` | `2026-11-05` `02:59:12` |
| 📄 [2026-11-04T14-12-52Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-04T14-12-52Z.md) | ❌ `failed` | `2026-11-04` `17:42:52` |
| 📄 [2026-11-04T05-52-05Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-11-04T05-52-05Z.md) | ❌ `failed` | `2026-11-04` `09:22:05` |

<!-- RUN_TABLE_END -->
