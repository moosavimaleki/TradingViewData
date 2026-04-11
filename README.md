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
| 📄 [2026-04-11T02-51-56Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-11T02-51-56Z.md) | ✅ `success` | `2026-04-11` `06:21:56` |
| 📄 [2026-04-10T19-04-33Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-10T19-04-33Z.md) | ✅ `success` | `2026-04-10` `22:34:33` |
| 📄 [2026-04-10T13-27-02Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-10T13-27-02Z.md) | ✅ `success` | `2026-04-10` `16:57:02` |
| 📄 [2026-04-10T07-52-26Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-10T07-52-26Z.md) | ✅ `success` | `2026-04-10` `11:22:26` |
| 📄 [2026-04-10T03-28-07Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-10T03-28-07Z.md) | ✅ `success` | `2026-04-10` `06:58:07` |
| 📄 [2026-04-09T19-19-11Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-09T19-19-11Z.md) | ✅ `success` | `2026-04-09` `22:49:11` |
| 📄 [2026-04-09T14-04-24Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-09T14-04-24Z.md) | ✅ `success` | `2026-04-09` `17:34:24` |
| 📄 [2026-04-09T07-48-59Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-09T07-48-59Z.md) | ✅ `success` | `2026-04-09` `11:18:59` |
| 📄 [2026-04-09T02-55-29Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-09T02-55-29Z.md) | ✅ `success` | `2026-04-09` `06:25:29` |
| 📄 [2026-04-08T19-27-22Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-08T19-27-22Z.md) | ✅ `success` | `2026-04-08` `22:57:22` |

<!-- RUN_TABLE_END -->
