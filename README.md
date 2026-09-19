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
| 📄 [2026-09-19T20-25-29Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-19T20-25-29Z.md) | ✅ `success` | `2026-09-19` `23:55:29` |
| 📄 [2026-09-19T15-44-54Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-19T15-44-54Z.md) | ✅ `success` | `2026-09-19` `19:14:54` |
| 📄 [2026-09-19T10-43-02Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-19T10-43-02Z.md) | ✅ `success` | `2026-09-19` `14:13:02` |
| 📄 [2026-09-19T04-14-42Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-19T04-14-42Z.md) | ✅ `success` | `2026-09-19` `07:44:42` |
| 📄 [2026-09-18T20-45-06Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-18T20-45-06Z.md) | ✅ `success` | `2026-09-19` `00:15:06` |
| 📄 [2026-09-18T16-13-51Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-18T16-13-51Z.md) | ✅ `success` | `2026-09-18` `19:43:51` |
| 📄 [2026-09-18T10-59-19Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-18T10-59-19Z.md) | ✅ `success` | `2026-09-18` `14:29:19` |
| 📄 [2026-09-18T04-18-09Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-18T04-18-09Z.md) | ✅ `success` | `2026-09-18` `07:48:09` |
| 📄 [2026-09-17T21-11-49Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-17T21-11-49Z.md) | ✅ `success` | `2026-09-18` `00:41:49` |
| 📄 [2026-09-17T16-44-40Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-17T16-44-40Z.md) | ✅ `success` | `2026-09-17` `20:14:40` |

<!-- RUN_TABLE_END -->
