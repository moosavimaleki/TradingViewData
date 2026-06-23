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
| 📄 [2026-06-23T04-08-15Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-23T04-08-15Z.md) | ✅ `success` | `2026-06-23` `07:38:15` |
| 📄 [2026-06-22T20-57-35Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-22T20-57-35Z.md) | ✅ `success` | `2026-06-23` `00:27:35` |
| 📄 [2026-06-22T12-18-28Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-22T12-18-28Z.md) | ✅ `success` | `2026-06-22` `15:48:28` |
| 📄 [2026-06-22T05-10-51Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-22T05-10-51Z.md) | ✅ `success` | `2026-06-22` `08:40:51` |
| 📄 [2026-06-21T19-53-36Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-21T19-53-36Z.md) | ✅ `success` | `2026-06-21` `23:23:36` |
| 📄 [2026-06-21T14-25-17Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-21T14-25-17Z.md) | ✅ `success` | `2026-06-21` `17:55:17` |
| 📄 [2026-06-21T09-59-21Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-21T09-59-21Z.md) | ✅ `success` | `2026-06-21` `13:29:21` |
| 📄 [2026-06-21T05-02-26Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-21T05-02-26Z.md) | ✅ `success` | `2026-06-21` `08:32:26` |
| 📄 [2026-06-20T19-47-10Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-20T19-47-10Z.md) | ✅ `success` | `2026-06-20` `23:17:10` |
| 📄 [2026-06-20T14-19-54Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-20T14-19-54Z.md) | ✅ `success` | `2026-06-20` `17:49:54` |

<!-- RUN_TABLE_END -->
