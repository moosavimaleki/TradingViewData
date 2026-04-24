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
| 📄 [2026-04-24T13-54-52Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-24T13-54-52Z.md) | ✅ `success` | `2026-04-24` `17:24:52` |
| 📄 [2026-04-24T08-14-58Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-24T08-14-58Z.md) | ✅ `success` | `2026-04-24` `11:44:58` |
| 📄 [2026-04-24T03-34-25Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-24T03-34-25Z.md) | ✅ `success` | `2026-04-24` `07:04:25` |
| 📄 [2026-04-23T19-23-08Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-23T19-23-08Z.md) | ✅ `success` | `2026-04-23` `22:53:08` |
| 📄 [2026-04-23T14-02-07Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-23T14-02-07Z.md) | ✅ `success` | `2026-04-23` `17:32:06` |
| 📄 [2026-04-23T08-06-03Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-23T08-06-03Z.md) | ✅ `success` | `2026-04-23` `11:36:03` |
| 📄 [2026-04-23T03-32-11Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-23T03-32-11Z.md) | ✅ `success` | `2026-04-23` `07:02:11` |
| 📄 [2026-04-22T19-24-05Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-22T19-24-05Z.md) | ✅ `success` | `2026-04-22` `22:54:05` |
| 📄 [2026-04-22T14-00-24Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-22T14-00-24Z.md) | ❌ `failed` | `2026-04-22` `17:30:24` |
| 📄 [2026-04-22T08-00-26Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-22T08-00-26Z.md) | ✅ `success` | `2026-04-22` `11:30:26` |

<!-- RUN_TABLE_END -->
