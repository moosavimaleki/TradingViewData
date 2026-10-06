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
| 📄 [2026-10-06T18-13-13Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-06T18-13-13Z.md) | ✅ `success` | `2026-10-06` `21:43:13` |
| 📄 [2026-10-06T06-07-40Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-06T06-07-40Z.md) | ✅ `success` | `2026-10-06` `09:37:40` |
| 📄 [2026-10-05T23-56-42Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-05T23-56-42Z.md) | ✅ `success` | `2026-10-06` `03:26:42` |
| 📄 [2026-10-05T14-17-33Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-05T14-17-33Z.md) | ✅ `success` | `2026-10-05` `17:47:33` |
| 📄 [2026-10-05T05-12-15Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-05T05-12-15Z.md) | ✅ `success` | `2026-10-05` `08:42:15` |
| 📄 [2026-10-04T21-10-27Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-04T21-10-27Z.md) | ✅ `success` | `2026-10-05` `00:40:27` |
| 📄 [2026-10-04T12-09-17Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-04T12-09-17Z.md) | ✅ `success` | `2026-10-04` `15:39:17` |
| 📄 [2026-10-04T05-29-01Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-04T05-29-01Z.md) | ✅ `success` | `2026-10-04` `08:59:01` |
| 📄 [2026-10-03T20-54-51Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-03T20-54-51Z.md) | ✅ `success` | `2026-10-04` `00:24:51` |
| 📄 [2026-10-03T16-04-24Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-10-03T16-04-24Z.md) | ✅ `success` | `2026-10-03` `19:34:24` |

<!-- RUN_TABLE_END -->
