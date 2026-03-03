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
| 📄 [2026-03-03T19-01-24Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-03T19-01-24Z.md) | ✅ `success` | `2026-03-03` `22:31:24` |
| 📄 [2026-03-03T13-14-26Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-03T13-14-26Z.md) | ✅ `success` | `2026-03-03` `16:44:26` |
| 📄 [2026-03-03T07-02-40Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-03T07-02-40Z.md) | ❌ `failed` | `2026-03-03` `10:32:40` |
| 📄 [2026-03-03T02-47-03Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-03T02-47-03Z.md) | ✅ `success` | `2026-03-03` `06:17:03` |
| 📄 [2026-03-02T18-59-02Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-02T18-59-02Z.md) | ✅ `success` | `2026-03-02` `22:29:02` |
| 📄 [2026-03-02T13-16-00Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-02T13-16-00Z.md) | ✅ `success` | `2026-03-02` `16:46:00` |
| 📄 [2026-03-02T07-08-16Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-02T07-08-16Z.md) | ✅ `success` | `2026-03-02` `10:38:16` |
| 📄 [2026-03-02T02-44-10Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-02T02-44-10Z.md) | ✅ `success` | `2026-03-02` `06:14:10` |
| 📄 [2026-03-01T18-44-16Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-01T18-44-16Z.md) | ✅ `success` | `2026-03-01` `22:14:16` |
| 📄 [2026-03-01T13-03-57Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-01T13-03-57Z.md) | ✅ `success` | `2026-03-01` `16:33:57` |

<!-- RUN_TABLE_END -->
