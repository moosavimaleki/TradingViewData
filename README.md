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
| 📄 [2026-09-23T04-24-24Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-23T04-24-24Z.md) | ✅ `success` | `2026-09-23` `07:54:24` |
| 📄 [2026-09-22T21-08-51Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-22T21-08-51Z.md) | ✅ `success` | `2026-09-23` `00:38:51` |
| 📄 [2026-09-22T16-43-48Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-22T16-43-48Z.md) | ✅ `success` | `2026-09-22` `20:13:48` |
| 📄 [2026-09-22T11-21-34Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-22T11-21-34Z.md) | ✅ `success` | `2026-09-22` `14:51:34` |
| 📄 [2026-09-22T04-27-29Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-22T04-27-29Z.md) | ✅ `success` | `2026-09-22` `07:57:29` |
| 📄 [2026-09-21T21-53-31Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-21T21-53-31Z.md) | ✅ `success` | `2026-09-22` `01:23:31` |
| 📄 [2026-09-21T12-33-53Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-21T12-33-53Z.md) | ✅ `success` | `2026-09-21` `16:03:53` |
| 📄 [2026-09-21T04-31-33Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-21T04-31-33Z.md) | ✅ `success` | `2026-09-21` `08:01:33` |
| 📄 [2026-09-20T20-38-27Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-20T20-38-27Z.md) | ✅ `success` | `2026-09-21` `00:08:27` |
| 📄 [2026-09-20T15-52-41Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-20T15-52-41Z.md) | ✅ `success` | `2026-09-20` `19:22:41` |

<!-- RUN_TABLE_END -->
