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
| 📄 [2026-06-07T14-09-23Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-07T14-09-23Z.md) | ✅ `success` | `2026-06-07` `17:39:23` |
| 📄 [2026-06-07T09-26-44Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-07T09-26-44Z.md) | ✅ `success` | `2026-06-07` `12:56:44` |
| 📄 [2026-06-07T04-43-37Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-07T04-43-37Z.md) | ✅ `success` | `2026-06-07` `08:13:37` |
| 📄 [2026-06-06T19-40-36Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-06T19-40-36Z.md) | ✅ `success` | `2026-06-06` `23:10:36` |
| 📄 [2026-06-06T13-59-00Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-06T13-59-00Z.md) | ✅ `success` | `2026-06-06` `17:29:00` |
| 📄 [2026-06-06T08-41-58Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-06T08-41-58Z.md) | ✅ `success` | `2026-06-06` `12:11:58` |
| 📄 [2026-06-06T04-07-08Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-06T04-07-08Z.md) | ✅ `success` | `2026-06-06` `07:37:08` |
| 📄 [2026-06-05T20-03-02Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-05T20-03-02Z.md) | ✅ `success` | `2026-06-05` `23:33:02` |
| 📄 [2026-06-05T15-19-36Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-05T15-19-36Z.md) | ✅ `success` | `2026-06-05` `18:49:36` |
| 📄 [2026-06-05T10-03-39Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-06-05T10-03-39Z.md) | ✅ `success` | `2026-06-05` `13:33:39` |

<!-- RUN_TABLE_END -->
