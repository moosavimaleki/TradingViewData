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
| 📄 [2026-04-06T13-25-54Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-06T13-25-54Z.md) | ✅ `success` | `2026-04-06` `16:55:54` |
| 📄 [2026-04-06T07-55-45Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-06T07-55-45Z.md) | ✅ `success` | `2026-04-06` `11:25:45` |
| 📄 [2026-04-06T03-27-24Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-06T03-27-24Z.md) | ✅ `success` | `2026-04-06` `06:57:24` |
| 📄 [2026-04-05T18-55-51Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-05T18-55-51Z.md) | ✅ `success` | `2026-04-05` `22:25:51` |
| 📄 [2026-04-05T13-13-36Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-05T13-13-36Z.md) | ✅ `success` | `2026-04-05` `16:43:36` |
| 📄 [2026-04-05T07-17-47Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-05T07-17-47Z.md) | ✅ `success` | `2026-04-05` `10:47:47` |
| 📄 [2026-04-05T03-24-38Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-05T03-24-38Z.md) | ✅ `success` | `2026-04-05` `06:54:38` |
| 📄 [2026-04-04T18-54-12Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-04T18-54-12Z.md) | ✅ `success` | `2026-04-04` `22:24:12` |
| 📄 [2026-04-04T13-11-54Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-04T13-11-54Z.md) | ✅ `success` | `2026-04-04` `16:41:54` |
| 📄 [2026-04-04T07-10-19Z.md](https://github.com/moosavimaleki/TradingViewData/blob/main/artifacts/tvdatafeed/2026-04-04T07-10-19Z.md) | ✅ `success` | `2026-04-04` `10:40:19` |

<!-- RUN_TABLE_END -->
