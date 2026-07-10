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
| 📄 [2026-07-10T03-57-38Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-10T03-57-38Z.md) | ✅ `success` | `2026-07-10` `07:27:38` |
| 📄 [2026-07-09T19-55-40Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-09T19-55-40Z.md) | ✅ `success` | `2026-07-09` `23:25:40` |
| 📄 [2026-07-09T15-25-27Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-09T15-25-27Z.md) | ✅ `success` | `2026-07-09` `18:55:27` |
| 📄 [2026-07-09T09-51-30Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-09T09-51-30Z.md) | ✅ `success` | `2026-07-09` `13:21:30` |
| 📄 [2026-07-09T04-02-02Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-09T04-02-02Z.md) | ✅ `success` | `2026-07-09` `07:32:02` |
| 📄 [2026-07-08T19-43-56Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-08T19-43-56Z.md) | ✅ `success` | `2026-07-08` `23:13:56` |
| 📄 [2026-07-08T14-30-25Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-08T14-30-25Z.md) | ✅ `success` | `2026-07-08` `18:00:25` |
| 📄 [2026-07-08T08-38-51Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-08T08-38-51Z.md) | ❌ `failed` | `2026-07-08` `12:08:51` |
| 📄 [2026-07-08T03-29-28Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-08T03-29-28Z.md) | ✅ `success` | `2026-07-08` `06:59:28` |
| 📄 [2026-07-07T20-05-47Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-07T20-05-47Z.md) | ✅ `success` | `2026-07-07` `23:35:47` |

<!-- RUN_TABLE_END -->
