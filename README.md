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
| 📄 [2026-04-27T03-46-49Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-27T03-46-49Z.md) | ✅ `success` | `2026-04-27` `07:16:49` |
| 📄 [2026-04-26T19-05-42Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-26T19-05-42Z.md) | ✅ `success` | `2026-04-26` `22:35:42` |
| 📄 [2026-04-26T13-21-31Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-26T13-21-31Z.md) | ✅ `success` | `2026-04-26` `16:51:31` |
| 📄 [2026-04-26T07-48-46Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-26T07-48-46Z.md) | ✅ `success` | `2026-04-26` `11:18:46` |
| 📄 [2026-04-26T03-41-06Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-26T03-41-06Z.md) | ✅ `success` | `2026-04-26` `07:11:06` |
| 📄 [2026-04-25T19-03-59Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-25T19-03-59Z.md) | ✅ `success` | `2026-04-25` `22:33:59` |
| 📄 [2026-04-25T13-20-35Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-25T13-20-35Z.md) | ✅ `success` | `2026-04-25` `16:50:35` |
| 📄 [2026-04-25T07-39-17Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-25T07-39-17Z.md) | ✅ `success` | `2026-04-25` `11:09:17` |
| 📄 [2026-04-25T03-19-06Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-25T03-19-06Z.md) | ✅ `success` | `2026-04-25` `06:49:06` |
| 📄 [2026-04-24T19-04-13Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-24T19-04-13Z.md) | ✅ `success` | `2026-04-24` `22:34:13` |

<!-- RUN_TABLE_END -->
