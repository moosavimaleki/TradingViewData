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
| 📄 [2026-04-09T14-04-24Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-09T14-04-24Z.md) | ✅ `success` | `2026-04-09` `17:34:24` |
| 📄 [2026-04-09T07-48-59Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-09T07-48-59Z.md) | ✅ `success` | `2026-04-09` `11:18:59` |
| 📄 [2026-04-09T02-55-29Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-09T02-55-29Z.md) | ✅ `success` | `2026-04-09` `06:25:29` |
| 📄 [2026-04-08T19-27-22Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-08T19-27-22Z.md) | ✅ `success` | `2026-04-08` `22:57:22` |
| 📄 [2026-04-08T13-49-53Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-08T13-49-53Z.md) | ❌ `failed` | `2026-04-08` `17:19:53` |
| 📄 [2026-04-08T07-46-22Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-08T07-46-22Z.md) | ✅ `success` | `2026-04-08` `11:16:22` |
| 📄 [2026-04-08T03-19-49Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-08T03-19-49Z.md) | ✅ `success` | `2026-04-08` `06:49:49` |
| 📄 [2026-04-07T19-15-06Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-07T19-15-06Z.md) | ✅ `success` | `2026-04-07` `22:45:06` |
| 📄 [2026-04-07T13-47-35Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-07T13-47-35Z.md) | ✅ `success` | `2026-04-07` `17:17:35` |
| 📄 [2026-04-07T07-42-45Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-07T07-42-45Z.md) | ✅ `success` | `2026-04-07` `11:12:45` |

<!-- RUN_TABLE_END -->
