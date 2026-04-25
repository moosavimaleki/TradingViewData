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
| 📄 [2026-04-25T13-20-35Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-25T13-20-35Z.md) | ✅ `success` | `2026-04-25` `16:50:35` |
| 📄 [2026-04-25T07-39-17Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-25T07-39-17Z.md) | ✅ `success` | `2026-04-25` `11:09:17` |
| 📄 [2026-04-25T03-19-06Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-25T03-19-06Z.md) | ✅ `success` | `2026-04-25` `06:49:06` |
| 📄 [2026-04-24T19-04-13Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-24T19-04-13Z.md) | ✅ `success` | `2026-04-24` `22:34:13` |
| 📄 [2026-04-24T13-54-52Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-24T13-54-52Z.md) | ✅ `success` | `2026-04-24` `17:24:52` |
| 📄 [2026-04-24T08-14-58Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-24T08-14-58Z.md) | ✅ `success` | `2026-04-24` `11:44:58` |
| 📄 [2026-04-24T03-34-25Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-24T03-34-25Z.md) | ✅ `success` | `2026-04-24` `07:04:25` |
| 📄 [2026-04-23T19-23-08Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-23T19-23-08Z.md) | ✅ `success` | `2026-04-23` `22:53:08` |
| 📄 [2026-04-23T14-02-07Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-23T14-02-07Z.md) | ✅ `success` | `2026-04-23` `17:32:06` |
| 📄 [2026-04-23T08-06-03Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-23T08-06-03Z.md) | ✅ `success` | `2026-04-23` `11:36:03` |

<!-- RUN_TABLE_END -->
