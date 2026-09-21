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
| 📄 [2026-09-21T21-53-31Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-21T21-53-31Z.md) | ✅ `success` | `2026-09-22` `01:23:31` |
| 📄 [2026-09-21T12-33-53Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-21T12-33-53Z.md) | ✅ `success` | `2026-09-21` `16:03:53` |
| 📄 [2026-09-21T04-31-33Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-21T04-31-33Z.md) | ✅ `success` | `2026-09-21` `08:01:33` |
| 📄 [2026-09-20T20-38-27Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-20T20-38-27Z.md) | ✅ `success` | `2026-09-21` `00:08:27` |
| 📄 [2026-09-20T15-52-41Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-20T15-52-41Z.md) | ✅ `success` | `2026-09-20` `19:22:41` |
| 📄 [2026-09-20T11-05-40Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-20T11-05-40Z.md) | ✅ `success` | `2026-09-20` `14:35:40` |
| 📄 [2026-09-20T04-33-42Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-20T04-33-42Z.md) | ✅ `success` | `2026-09-20` `08:03:42` |
| 📄 [2026-09-19T20-25-29Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-19T20-25-29Z.md) | ✅ `success` | `2026-09-19` `23:55:29` |
| 📄 [2026-09-19T15-44-54Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-19T15-44-54Z.md) | ✅ `success` | `2026-09-19` `19:14:54` |
| 📄 [2026-09-19T10-43-02Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-19T10-43-02Z.md) | ✅ `success` | `2026-09-19` `14:13:02` |

<!-- RUN_TABLE_END -->
