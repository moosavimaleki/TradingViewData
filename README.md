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
| 📄 [2026-03-12T19-03-27Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-12T19-03-27Z.md) | ✅ `success` | `2026-03-12` `22:33:27` |
| 📄 [2026-03-12T13-18-15Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-12T13-18-15Z.md) | ✅ `success` | `2026-03-12` `16:48:15` |
| 📄 [2026-03-12T07-05-47Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-12T07-05-47Z.md) | ✅ `success` | `2026-03-12` `10:35:47` |
| 📄 [2026-03-12T02-44-16Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-12T02-44-16Z.md) | ✅ `success` | `2026-03-12` `06:14:16` |
| 📄 [2026-03-11T19-02-49Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-11T19-02-49Z.md) | ✅ `success` | `2026-03-11` `22:32:49` |
| 📄 [2026-03-11T13-17-54Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-11T13-17-54Z.md) | ❌ `failed` | `2026-03-11` `16:47:54` |
| 📄 [2026-03-11T07-04-20Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-11T07-04-20Z.md) | ✅ `success` | `2026-03-11` `10:34:20` |
| 📄 [2026-03-11T02-38-30Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-11T02-38-30Z.md) | ✅ `success` | `2026-03-11` `06:08:30` |
| 📄 [2026-03-10T19-00-11Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-10T19-00-11Z.md) | ✅ `success` | `2026-03-10` `22:30:11` |
| 📄 [2026-03-10T13-18-23Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-03-10T13-18-23Z.md) | ✅ `success` | `2026-03-10` `16:48:23` |

<!-- RUN_TABLE_END -->
