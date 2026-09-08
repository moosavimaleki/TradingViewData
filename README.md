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
| 📄 [2026-09-08T21-00-14Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-08T21-00-14Z.md) | ✅ `success` | `2026-09-09` `00:30:14` |
| 📄 [2026-09-08T16-27-27Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-08T16-27-27Z.md) | ✅ `success` | `2026-09-08` `19:57:27` |
| 📄 [2026-09-08T11-02-02Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-08T11-02-02Z.md) | ✅ `success` | `2026-09-08` `14:32:02` |
| 📄 [2026-09-08T04-10-34Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-08T04-10-34Z.md) | ✅ `success` | `2026-09-08` `07:40:34` |
| 📄 [2026-09-07T21-23-47Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-07T21-23-47Z.md) | ✅ `success` | `2026-09-08` `00:53:47` |
| 📄 [2026-09-07T12-11-25Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-07T12-11-25Z.md) | ✅ `success` | `2026-09-07` `15:41:25` |
| 📄 [2026-09-07T04-09-15Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-07T04-09-15Z.md) | ❌ `failed` | `2026-09-07` `07:39:15` |
| 📄 [2026-09-06T20-16-37Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-06T20-16-37Z.md) | ✅ `success` | `2026-09-06` `23:46:37` |
| 📄 [2026-09-06T15-19-16Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-06T15-19-16Z.md) | ✅ `success` | `2026-09-06` `18:49:16` |
| 📄 [2026-09-06T10-42-43Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-09-06T10-42-43Z.md) | ✅ `success` | `2026-09-06` `14:12:43` |

<!-- RUN_TABLE_END -->
