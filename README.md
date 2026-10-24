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
| 📄 [2026-10-24T20-32-53Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-24T20-32-53Z.md) | ❌ `failed` | `2026-10-25` `00:02:53` |
| 📄 [2026-10-24T15-44-49Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-24T15-44-49Z.md) | ❌ `failed` | `2026-10-24` `19:14:49` |
| 📄 [2026-10-24T10-42-11Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-24T10-42-11Z.md) | ✅ `success` | `2026-10-24` `14:12:11` |
| 📄 [2026-10-24T04-13-15Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-24T04-13-15Z.md) | ❌ `failed` | `2026-10-24` `07:43:15` |
| 📄 [2026-10-23T21-15-56Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-23T21-15-56Z.md) | ❌ `failed` | `2026-10-24` `00:45:56` |
| 📄 [2026-10-23T16-52-00Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-23T16-52-00Z.md) | ❌ `failed` | `2026-10-23` `20:22:00` |
| 📄 [2026-10-23T11-23-19Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-23T11-23-19Z.md) | ✅ `success` | `2026-10-23` `14:53:19` |
| 📄 [2026-10-23T04-22-30Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-23T04-22-30Z.md) | ❌ `failed` | `2026-10-23` `07:52:30` |
| 📄 [2026-10-22T21-24-36Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-22T21-24-36Z.md) | ✅ `success` | `2026-10-23` `00:54:36` |
| 📄 [2026-10-22T16-59-27Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-22T16-59-27Z.md) | ✅ `success` | `2026-10-22` `20:29:27` |

<!-- RUN_TABLE_END -->
