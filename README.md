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
| 📄 [2026-07-08T19-43-56Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-08T19-43-56Z.md) | ✅ `success` | `2026-07-08` `23:13:56` |
| 📄 [2026-07-08T14-30-25Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-08T14-30-25Z.md) | ✅ `success` | `2026-07-08` `18:00:25` |
| 📄 [2026-07-08T08-38-51Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-08T08-38-51Z.md) | ❌ `failed` | `2026-07-08` `12:08:51` |
| 📄 [2026-07-08T03-29-28Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-08T03-29-28Z.md) | ✅ `success` | `2026-07-08` `06:59:28` |
| 📄 [2026-07-07T20-05-47Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-07T20-05-47Z.md) | ✅ `success` | `2026-07-07` `23:35:47` |
| 📄 [2026-07-07T14-52-37Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-07T14-52-37Z.md) | ✅ `success` | `2026-07-07` `18:22:37` |
| 📄 [2026-07-07T09-53-54Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-07T09-53-54Z.md) | ✅ `success` | `2026-07-07` `13:23:54` |
| 📄 [2026-07-07T04-03-20Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-07T04-03-20Z.md) | ✅ `success` | `2026-07-07` `07:33:20` |
| 📄 [2026-07-06T20-06-47Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-06T20-06-47Z.md) | ✅ `success` | `2026-07-06` `23:36:47` |
| 📄 [2026-07-06T15-48-37Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-07-06T15-48-37Z.md) | ❌ `failed` | `2026-07-06` `19:18:37` |

<!-- RUN_TABLE_END -->
