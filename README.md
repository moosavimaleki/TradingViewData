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
| 📄 [2026-06-28T14-04-01Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-28T14-04-01Z.md) | ✅ `success` | `2026-06-28` `17:34:01` |
| 📄 [2026-06-28T09-21-58Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-28T09-21-58Z.md) | ✅ `success` | `2026-06-28` `12:51:58` |
| 📄 [2026-06-28T04-26-35Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-28T04-26-35Z.md) | ✅ `success` | `2026-06-28` `07:56:35` |
| 📄 [2026-06-27T19-38-17Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-27T19-38-17Z.md) | ✅ `success` | `2026-06-27` `23:08:17` |
| 📄 [2026-06-27T13-57-37Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-27T13-57-37Z.md) | ✅ `success` | `2026-06-27` `17:27:37` |
| 📄 [2026-06-27T08-45-17Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-27T08-45-17Z.md) | ✅ `success` | `2026-06-27` `12:15:17` |
| 📄 [2026-06-27T04-04-49Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-27T04-04-49Z.md) | ✅ `success` | `2026-06-27` `07:34:49` |
| 📄 [2026-06-26T19-59-40Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-26T19-59-40Z.md) | ✅ `success` | `2026-06-26` `23:29:40` |
| 📄 [2026-06-26T14-38-24Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-26T14-38-24Z.md) | ✅ `success` | `2026-06-26` `18:08:24` |
| 📄 [2026-06-26T09-40-36Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-26T09-40-36Z.md) | ✅ `success` | `2026-06-26` `13:10:36` |

<!-- RUN_TABLE_END -->
