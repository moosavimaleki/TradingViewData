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
| 📄 [2026-04-13T08-15-32Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-13T08-15-32Z.md) | ✅ `success` | `2026-04-13` `11:45:32` |
| 📄 [2026-04-13T03-38-17Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-13T03-38-17Z.md) | ✅ `success` | `2026-04-13` `07:08:17` |
| 📄 [2026-04-12T19-00-44Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-12T19-00-44Z.md) | ✅ `success` | `2026-04-12` `22:30:44` |
| 📄 [2026-04-12T13-16-50Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-12T13-16-50Z.md) | ✅ `success` | `2026-04-12` `16:46:50` |
| 📄 [2026-04-12T07-24-41Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-12T07-24-41Z.md) | ✅ `success` | `2026-04-12` `10:54:41` |
| 📄 [2026-04-12T03-32-01Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-12T03-32-01Z.md) | ✅ `success` | `2026-04-12` `07:02:01` |
| 📄 [2026-04-11T18-56-57Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-11T18-56-57Z.md) | ✅ `success` | `2026-04-11` `22:26:57` |
| 📄 [2026-04-11T13-14-36Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-11T13-14-36Z.md) | ✅ `success` | `2026-04-11` `16:44:36` |
| 📄 [2026-04-11T07-10-35Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-11T07-10-35Z.md) | ✅ `success` | `2026-04-11` `10:40:35` |
| 📄 [2026-04-11T02-51-56Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-11T02-51-56Z.md) | ✅ `success` | `2026-04-11` `06:21:56` |

<!-- RUN_TABLE_END -->
